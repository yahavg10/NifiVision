from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class ModelTrainer(ABC):
    @abstractmethod
    def train(self, df: pd.DataFrame):
        raise NotImplementedError