from typing import List, Dict, Any

from prometheus_api_client import PrometheusConnect

from configurations.developer.models import PrometheusConfig
from src.utils.annotations import Service


@Service
class PrometheusDataSource:
    def __init__(self, prometheus_config: PrometheusConfig):
        self.prometheus = PrometheusConnect(
            # url=prometheus_config.url, #TODO: fix this (AttributeError: 'HttpUrl' object has no attribute 'decode')
            timeout=prometheus_config.query_timeout,
            disable_ssl=prometheus_config.tls_config.insecure_skip_verify
            if prometheus_config.tls_config
            else True
        )
        self.query = prometheus_config.query

    def get_metrics(self, query: str = None) -> List[Dict[str, Any]]:
        if query:
            self.query = query
        return self.prometheus.custom_query(query=self.query)
