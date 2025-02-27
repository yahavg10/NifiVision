from typing import List, Dict, Any

from parsers.base import AbstractParser


class TemplateParser(AbstractParser):
    @staticmethod
    def parse(raw_data: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        parsed_data = []

        for metric in raw_data:
            try:
                route = metric.get("metric", {}).get("route", "unknown")
                values = metric.get("values", [])
                timestamps = [float(value[0]) for value in values]
                metrics_values = [float(value[1]) for value in values]

                if not timestamps or not metrics_values:
                    raise ValueError("Timestamps or metric values are missing")

                parsed_data.append({
                    "route": route,
                    "timestamps": timestamps,
                    "values": metrics_values,
                })

            except (ValueError, TypeError) as e:
                raise e

        return parsed_data
