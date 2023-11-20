from exporter.metrics_collector import MetricsCollector
from exporter.metrics_scraper import MetricScraper
from exporter.prober import Prober, ProberSettings
from exporter.settings import ExporterSettings
from exporter.slaser import SlaserSettings, Slaser
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
    container.register(ProberSettings, lambda: ProberSettings(), scope=Scope.singleton)
    container.register(Prober, Prober, scope=Scope.singleton)
    container.register(SlaserSettings, lambda: SlaserSettings(), scope=Scope.singleton)
    container.register(Slaser, Slaser, scope=Scope.singleton)
    return container
