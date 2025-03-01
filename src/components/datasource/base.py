from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DataSource(ABC):
    @abstractmethod
    def get_metrics(self, query: str) -> List[Dict[str, Any]]:
        raise NotImplementedError
