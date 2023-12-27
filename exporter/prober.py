import requests

from exporter.metrics_collector import MetricsCollector
from pydantic_settings import BaseSettings


class ProberSettings(BaseSettings):
    metrics_endpoint: str = 'http://localhost:8888/metrics'

    class Config:
        env_prefix = 'PROBER_SETTINGS_'


class Prober:
    def __init__(self, metrics_collector: MetricsCollector, settings: ProberSettings):
        self._metrics_collector = metrics_collector
        self._settings = settings
        self._session = requests.Session()

    def update(self):
        self._update_metrics_requests()

    def _update_metrics_requests(self):
        try:
            response = self._session.get(self._settings.metrics_endpoint)
            response.raise_for_status()
            self._metrics_collector.get_metrics_success_requests.inc()
        finally:
            self._metrics_collector.get_metrics_requests_total.inc()

