import logging
from dataclasses import dataclass
from typing import Any, Dict
import json
import subprocess
import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server, ProcessCollector
import psutil
import logging_loki
import os
from string import Template
import dotenv
import atexit

@dataclass
class LokiConfig:
    url: str

class ProcessMetricsCollector(object):
    def __init__(self, project: str, run: str):
        self.project = project
        self.run = run
        self.process = psutil.Process()

    def collect(self):
        # Process CPU metrics
        cpu_usage = GaugeMetricFamily(
            'process_cpu_usage_percent',
            'CPU usage by the process in percent',
            labels=['project', 'run']
        )
        cpu_usage.add_metric([self.project, self.run], self.process.cpu_percent())
        yield cpu_usage

        # Process memory metrics
        mem_info = self.process.memory_info()
        mem_usage = GaugeMetricFamily(
            'process_memory_usage_bytes',
            'Memory usage by the process in bytes',
            labels=['type', 'project', 'run']
        )
        mem_usage.add_metric(['rss', self.project, self.run], mem_info.rss)  # Resident Set Size
        mem_usage.add_metric(['vms', self.project, self.run], mem_info.vms)  # Virtual Memory Size
        yield mem_usage

        # Process IO metrics (if available)
        if hasattr(self.process, 'io_counters'):
            io_counters = self.process.io_counters()
            io_read_bytes = GaugeMetricFamily(
                'process_io_read_bytes',
                'Number of bytes read by the process'
            )
            io_read_bytes.add_metric([], io_counters.read_bytes)
            yield io_read_bytes

            io_write_bytes = GaugeMetricFamily(
                'process_io_write_bytes',
                'Number of bytes written by the process'
            )
            io_write_bytes.add_metric([], io_counters.write_bytes)
            yield io_write_bytes

        # Disk I/O Counters
        if hasattr(self.process, 'io_counters'):
            io_counters = self.process.io_counters()
            io_read_count = GaugeMetricFamily(
                'process_io_read_count',
                'Number of read operations by the process',
                labels=['project', 'run']
            )
            io_read_count.add_metric([self.project, self.run], io_counters.read_count)
            yield io_read_count

            io_write_count = GaugeMetricFamily(
                'process_io_write_count',
                'Number of write operations by the process',
                labels=['project', 'run']
            )
            io_write_count.add_metric([self.project, self.run], io_counters.write_count)
            yield io_write_count

        # CPU Times
        cpu_times = self.process.cpu_times()
        for time_type in ['user', 'system', 'children_user', 'children_system']:
            cpu_time = GaugeMetricFamily(
                f'process_cpu_time_seconds_{time_type}',
                f'Total CPU time in seconds spent by the process in {time_type} mode',
                labels=['project', 'run']
            )
            cpu_time.add_metric([self.project, self.run], getattr(cpu_times, time_type, 0))
            yield cpu_time

        # Context Switches
        if hasattr(self.process, 'num_ctx_switches'):
            ctx_switches = self.process.num_ctx_switches()
            voluntary_ctx_switches = GaugeMetricFamily(
                'process_voluntary_context_switches',
                'Number of voluntary context switches',
                labels=['project', 'run']
            )
            voluntary_ctx_switches.add_metric([self.project, self.run], ctx_switches.voluntary)
            yield voluntary_ctx_switches

            involuntary_ctx_switches = GaugeMetricFamily(
                'process_involuntary_context_switches',
                'Number of involuntary context switches',
                labels=['project', 'run']
            )
            involuntary_ctx_switches.add_metric([self.project, self.run], ctx_switches.involuntary)
            yield involuntary_ctx_switches

        # Thread Count
        thread_count = GaugeMetricFamily(
            'process_thread_count',
            'Number of threads in use by the process',
            labels=['project', 'run']
        )
        thread_count.add_metric([self.project, self.run], self.process.num_threads())
        yield thread_count

        # File Descriptors
        if hasattr(self.process, 'num_fds'):
            file_descriptors = GaugeMetricFamily(
                'process_open_file_descriptors',
                'Number of open file descriptors',
                labels=['project', 'run']
            )
            file_descriptors.add_metric([self.project, self.run], self.process.num_fds())
            yield file_descriptors

class Mandl:
    def __init__(self):
        self._loki_config = None
        self._logger = None
        self.prometheus_port = 9000  # Default Prometheus port
        self.metrics_collector_port = 8000  # Default metrics collector port
        self._counter = 0
        self.seen_user_metrics = set()
        self._has_finished = False


    def init(
        self, project: str, run: str, loki_config: LokiConfig, metadata: Dict[str, Any], use_prometheus: bool = False, prometheus_port: int = 9000, metrics_collector_port: int = 8000
    ):
        self.project = project
        self.run = run
        self.metadata = metadata
        self._loki_config = loki_config
        self.use_prometheus = use_prometheus
        self.prometheus_port = prometheus_port
        self.metrics_collector_port = metrics_collector_port
        self._initialize_system_metrics_server()
        if self.use_prometheus:
            self._initialize_prometheus()
        self._logger = self._setup_loki_logger(loki_config, project, run, metadata)
    
    def _initialize_system_metrics_server(self):
        collector = ProcessMetricsCollector(self.project, self.run)
        REGISTRY.register(collector)
        start_http_server(self.metrics_collector_port)

    def _initialize_prometheus(self):
        mandl_dir = os.path.dirname(os.path.realpath(__file__))
        prometheus_template_path = os.path.join(mandl_dir, 'prometheus.yml.template')
        prometheus_executable = 'prometheus'

        try:
            result = subprocess.run(
                ["lsof", "-i", f":{self.prometheus_port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            prometheus_running = "LISTEN" in str(result.stdout)
        except Exception as e:
            logging.error(f"Error checking for Prometheus: {e}")
            prometheus_running = False

        if not prometheus_running:
            try:
                if not os.path.isfile(prometheus_template_path):
                    raise FileNotFoundError(f"Prometheus configuration file not found at {prometheus_template_path}")
                
                dotenv.load_dotenv()

                prometheus_user = os.environ.get("PROMETHEUS_USER")
                prometheus_token = os.environ.get("PROMETHEUS_TOKEN")

                with open(prometheus_template_path, 'r') as file:
                    template = Template(file.read())
                    config = template.substitute(PROMETHEUS_USER=prometheus_user, PROMETHEUS_TOKEN=prometheus_token)

                prometheus_config_path = os.path.join(mandl_dir, 'prometheus.yml')

                with open(prometheus_config_path, 'w') as file:
                    file.write(config)

                subprocess.Popen(
                    [prometheus_executable, f"--config.file={prometheus_config_path}", f"--web.listen-address=:{self.prometheus_port}"]
                )
                time.sleep(2)  # Give Prometheus some time to start
            except Exception as e:
                logging.error(f"Error starting Prometheus: {e}")
                raise

        self.prometheus_url = f"http://localhost:{self.prometheus_port}/metrics"

    def _setup_loki_logger(self, loki_config: LokiConfig, project: str, run: str, metadata: Dict[str, Any]):
        if not loki_config.url:
            raise ValueError("Loki URL not set.")

        handler = logging_loki.LokiHandler(
            url=loki_config.url,
            tags={
                "project": project,
                "run": run,
                **metadata
            },
            version="1",
        )
        # This is the one you query via
        logger = logging.getLogger(f"mandl")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        atexit.register(self.finish)
        return logger

    def log(self, metrics: Dict[str, float]):
        # Log to Loki
        try:
            self._logger.info(json.dumps({**metrics, "counter": self._counter}), extra={"tags": {"message_type": "metric"}})
            self._counter += 1
            self.seen_user_metrics.update(metrics.keys())
        except Exception as e:
            print(f"Error logging metrics: {e}")

    def __del__(self):
        pass

    # You should only need to call finish explicitly in jupyter notebooks
    def finish(self):
        if self._has_finished:
           print("Finish function called multiple times. Ignoring.")
           return 
        self._has_finished = True
        try:
            self._logger.info({"used_metrics:": list(self.seen_user_metrics)}, extra={"tags": {"message_type": "finish"}})
            result = subprocess.run(
                ["lsof", "-ti", f":{self.prometheus_port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            pids = result.stdout.decode().strip().split('\n')
            for pid in pids:
                if pid:
                    subprocess.run(["kill", "-9", pid])
        except Exception as e:
            logging.error(f"Error stopping Prometheus: {e}")
