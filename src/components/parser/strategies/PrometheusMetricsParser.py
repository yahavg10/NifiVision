from typing import List, Dict

import pandas as pd

from src.utils.annotations import Service


@Service
class PrometheusMetricsParser:
    def parse(self, metrics: List[Dict]) -> Dict[pd.Timestamp, float]:
        data = []

        for metric in metrics:
            for timestamp, value in metric.get('values', []):
                timestamp = pd.to_datetime(timestamp, unit='s')
                data.append((timestamp, float(value)))

        df = pd.DataFrame(data, columns=['timestamp', 'value'])
        df.set_index('timestamp', inplace=True)

        return df
