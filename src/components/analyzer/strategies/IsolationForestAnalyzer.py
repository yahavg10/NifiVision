from typing import Any

import numpy as np
from sklearn.metrics import classification_report

from src.components.analyzer.base import Analyzer

from src.utils.annotations import Service


@Service
class IsolationForestAnalyzer(Analyzer):
    def analyze(self, model: Any, X: np.ndarray):
        if not hasattr(model, "predict"):
            raise ValueError("Model must have a predict method")

        print("Analyzing model...")

        # Predict labels (-1 for anomaly, 1 for normal)
        predictions = model.predict(X)

        # Generate a simple classification report (assuming labels exist for demo)
        true_labels = [1 if i % 10 else -1 for i in range(len(X))]  # Example labels
        print("Classification Report:")
        print(classification_report(true_labels, predictions))

        return predictions
