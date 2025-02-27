from prometheus_api_client import PrometheusConnect
from typing import List, Dict, Any
from .base import DataSource


class PrometheusDataSource(DataSource):
    def __init__(self, prometheus_url: str):
        self.prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)

    def get_metrics(self, query: str) -> List[Dict[str, Any]]:
        return self.prometheus.custom_query(query=query)
