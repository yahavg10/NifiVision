from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AbstractParser(ABC):
    @abstractmethod
    def parse(self, raw_data):
        raise NotImplementedError