
from datetime import datetime
from typing import List, Callable, Union
import numpy as np
from sklearn.ensemble import IsolationForest
from analyzer.base import TrendAnalyzer


class TimeOfDayTrendAnalyzer(TrendAnalyzer):
    def __init__(self, contamination: float = 0.1):
        # Initialize the anomaly detector using IsolationForest
        # `contamination` defines the proportion of anomalies in the data (default: 10%)
        # `random_state=42` ensures reproducibility of the results
        self.anomaly_detector = IsolationForest(contamination=contamination, random_state=42)

    def is_anomalous(
            self,
            timestamps: List[float],
            values: List[float],
            additional_data_extractor: Callable[[float, float], Union[float, int]] = None,
    ) -> bool:
        if len(values) < 2:
            return False

        features = [
            (datetime.fromtimestamp(ts).hour, val)
            for ts, val in zip(timestamps, values)
        ]

        # If an additional data extractor is provided,
        # use it to compute extra features alongside (hour, value)
        if additional_data_extractor:
            features = [
                (hour, value, additional_data_extractor(hour, value))  # Add third feature if needed
                for hour, value in features
            ]

        # Convert the feature list to a NumPy array for compatibility with IsolationForest
        features_array = np.array(features)

        # Fit the IsolationForest model to the features
        # This trains the anomaly detector to identify patterns and outliers
        self.anomaly_detector.fit(features_array)

        # Use the trained model to predict whether each point is normal (1) or anomalous (-1)
        predictions = self.anomaly_detector.predict(features_array)

        # Check the predictions to see if there are any anomalies (-1)
        return any(pred == -1 for pred in predictions)
