import logging
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from src.components.trainer.base import ModelTrainer

from src.utils.annotations import Service
logger = logging.getLogger(os.getenv("ENV"))


@Service
class IsolationForestTrainer(ModelTrainer):
    def __init__(self, contamination: float = 0.1, n_estimators: int = 100, random_state: int = 42):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = None

    def train(self, df: pd.DataFrame):
        X = df[['value']].values

        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=self.n_estimators,
            random_state=self.random_state,
        )
        self.model.fit(X)
        logger.debug("Model trained successfully")
        return self.model
