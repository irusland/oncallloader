import datetime
import logging
import time

from prometheus_client import start_http_server

from exporter.metrics_collector import MetricsCollector
from exporter.settings import ExporterSettings
from oncall_client.client import OncallClient

logger = logging.getLogger(__name__)


class MetricScraper:
    def __init__(
        self,
        exporter_settings: ExporterSettings,
        oncall_client: OncallClient,
        metrics_collector: MetricsCollector
    ):
        self._exporter_settings = exporter_settings
        self._oncall_client = oncall_client
        self._metrics_collector = metrics_collector

    def run_forever(self):
        start_http_server(self._exporter_settings.port)

        while True:
            try:
                self._scrape()
            except:
                logger.exception('Scrape failed')
            time.sleep(self._exporter_settings.scrape_interval.total_seconds())

    def _scrape(self):
        self._scrape_search_teams()
        self._scrape_search_events()

    def _scrape_search_teams(self):
        try:
            teams = self._oncall_client.search_teams(team_name='k8s')
        except:
            logger.exception('Search teams failed')
        else:
            if len(teams) > 0:
                self._metrics_collector.search_teams_requests_success.inc()
        finally:
            self._metrics_collector.search_teams_requests_total.inc()

    def _scrape_search_events(self):
        try:
            start_time = time.monotonic()
            events = self._oncall_client.search_events(
                team='k8s SRE', start_date=datetime.datetime.now()
            )
            end_time = time.monotonic()
        except:
            logger.exception("Search events failed")
        else:
            self._metrics_collector.get_team_schedule_requests.observe(
                end_time-start_time
            )
