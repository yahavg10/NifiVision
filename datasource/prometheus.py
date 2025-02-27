import yaml
from typing import List, Dict, Any
from prometheus_api_client import PrometheusConnect

from configurations.developer.models import PrometheusConfig, DataSourceConfig


class PrometheusDataSource:
    def __init__(self, prometheus_config: PrometheusConfig):
        self.prometheus = PrometheusConnect(
            url=prometheus_config.url,
            disable_ssl=prometheus_config.tls_config.insecure_skip_verify
            if prometheus_config.tls_config
            else True
        )
        self.query_timeout = prometheus_config.query_timeout

    def get_metrics(self, query: str) -> List[Dict[str, Any]]:
        return self.prometheus.custom_query(query=query)





