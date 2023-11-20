from exporter.metrics_collector import MetricsCollector
from exporter.metrics_scraper import MetricScraper
from exporter.settings import ExporterSettings
from oncall_client.client import OncallClient
from oncall_client.settings import OncallSettings
from punq import Container, Scope


def get_container() -> Container:
    container = Container()
    container.register(OncallSettings, lambda: OncallSettings(), scope=Scope.singleton)
    container.register(OncallClient, OncallClient, scope=Scope.singleton)
    container.register(ExporterSettings, lambda: ExporterSettings(), scope=Scope.singleton)
    container.register(MetricsCollector, MetricsCollector, scope=Scope.singleton)
    container.register(MetricScraper, MetricScraper, scope=Scope.singleton)
    return container
