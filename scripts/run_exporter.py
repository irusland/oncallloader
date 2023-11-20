
from exporter.metrics_scraper import MetricScraper
from oncall_client.deps import get_container
from dotenv import load_dotenv


def main():
    container = get_container()
    metric_scraper = container.resolve(MetricScraper)

    metric_scraper.run_forever()


def run():
    load_dotenv()
    main()


if __name__ == '__main__':
    run()
