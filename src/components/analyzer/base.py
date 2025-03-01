from abc import abstractmethod, ABC
from typing import Any

import numpy as np


class Analyzer(ABC):
    @abstractmethod
    def analyze(self, model: Any, X: np.ndarray):
        raise NotImplementedError
