from abc import ABC, abstractmethod

import numpy as np


class ModelTrainer(ABC):
    @abstractmethod
    def train(self, X: np.ndarray):
        raise NotImplementedError