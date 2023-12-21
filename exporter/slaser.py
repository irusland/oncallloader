from typing import Type

import requests
from pydantic_settings import BaseSettings
from pydantic import BaseModel

from exporter.metrics_collector import MetricsCollector


class SlaserSettings(BaseSettings):
    prom_query_endpoint: str = 'http://localhost:9090/api/v1/query'

    schedule_indicator_query: str = 'histogram_quantile(0.99, get_team_schedule_requests_bucket)'
    schedule_sla: float = 0.04

    get_metrics_indicator_query: str = '(get_metrics_success_requests_total{} / get_metrics_requests_total{})'
    metrics_sla: float = 0.80

    statuses_indicator_query: str = 'sum(api_request_statuses_total{status="200"}) / sum(api_request_statuses_total{})'
    statuses_sla: float = 0.9


class IndicatorResponseDataResult(BaseModel):
    value: tuple[float, str]


class IndicatorResponseData(BaseModel):
    result: list[IndicatorResponseDataResult]


class IndicatorResponse(BaseModel):
    data: IndicatorResponseData


class Slaser:
    def __init__(self, settings: SlaserSettings, collector: MetricsCollector):
        self._settings = settings
        self._session = requests.Session()
        self._collector = collector

    def update(self):
        self._update_schedule_latency()
        self._update_get_metrics()
        self._update_statuses()

    def _update_schedule_latency(self):
        try:
            model = self._query(query=self._settings.schedule_indicator_query, model=IndicatorResponse)
            _, raw_value = model.data.result[0].value
            current_value = float(raw_value)
        except:
            current_value = self._settings.schedule_sla
        self._collector.sla.labels(indicator='schedule').set(1 if current_value < self._settings.schedule_sla else 0)

    def _update_get_metrics(self):
        try:
            model = self._query(query=self._settings.get_metrics_indicator_query, model=IndicatorResponse)
            _, raw_value = model.data.result[0].value
            current_value = float(raw_value)
        except:
            current_value = self._settings.metrics_sla
        self._collector.sla.labels(indicator='metrics').set(1 if current_value > self._settings.metrics_sla else 0)

    def _update_statuses(self):
        try:
            model = self._query(query=self._settings.statuses_indicator_query, model=IndicatorResponse)
            _, raw_value = model.data.result[0].value
            current_value = float(raw_value)
        except:
            current_value = self._settings.statuses_sla
        self._collector.sla.labels(indicator='statuses').set(1 if current_value > self._settings.statuses_sla else 0)

    def _query(self, query: str, model: Type[BaseModel]) -> BaseModel:
        response = self._session.get(
            self._settings.prom_query_endpoint,
            params={'query': query}
        )
        response.raise_for_status()
        return model.model_validate(
            response.json()
        )
