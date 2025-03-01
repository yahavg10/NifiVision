from abc import ABC, abstractmethod
from typing import List, Callable, Union


class TrendAnalyzer(ABC):
    @abstractmethod
    def train(self, timestamps: List[float], values: List[float]):
        raise NotImplementedError

    def is_anomalous(
        self,
        timestamps: List[float],
        values: List[float],
        additional_data_extractor: Callable[[float, float], Union[float, int]] = None,
   ) -> bool:
        raise NotImplementedError
