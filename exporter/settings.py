from datetime import timedelta
from pydantic_settings import BaseSettings


class ExporterSettings(BaseSettings):
    port: int = 8889
    scrape_interval: timedelta = timedelta(seconds=1)

    class Config:
        env_prefix = 'EXPORTER_'
