# mandl/__init__.py
from .mandl import Mandl, LokiConfig

_mandl_instance = Mandl()


def init(project: str, run: str, loki_config: LokiConfig, config: dict, use_prometheus: bool = False, prometheus_port: int = 9000, metrics_collector_port: int = 8000):
    _mandl_instance.init(project, run, loki_config, config, use_prometheus, prometheus_port, metrics_collector_port)


def log(metrics: dict):
    _mandl_instance.log(metrics)


def finish():
    _mandl_instance.finish()


__all__ = ["init", "log", "finish", "LokiConfig"]
