from typing import Callable, Dict, Any
from datasource.base import DataSource
from analyzer.base import TrendAnalyzer
from parsers.parser import Parser


class Orchestrator:
    def __init__(
        self,
        data_source: DataSource,
        trend_analyzer: TrendAnalyzer,
    ):
        self.data_source = data_source
        self.trend_analyzer = trend_analyzer

    def monitor(self, query: str):
        raw_metrics = self.data_source.get_metrics(query)

        for metric in raw_metrics:
            route = metric["route"]
            timestamps = metric["timestamps"]
            values = metric["values"]

            parsed_data = Parser().parse(raw_data=values)

            if self.trend_analyzer.is_anomalous(timestamps, parsed_data):
                print(f"Anomaly detected for route: {route}")
