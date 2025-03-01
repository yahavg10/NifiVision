import numpy as np

from src.components.trainer.base import ModelTrainer

from src.utils.annotations import Service


@Service
class IsolationForestTrainer(ModelTrainer):
    def __init__(self, contamination: float = 0.1, n_estimators: int = 100, random_state: int = 42):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = None

    def train(self, X: np.ndarray):
        from sklearn.ensemble import IsolationForest

        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=self.n_estimators,
            random_state=self.random_state,
        )
        self.model.fit(X)
        print("Model trained successfully")
        return self.model
