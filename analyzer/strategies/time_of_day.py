from typing import Dict

from pyod.models.iforest import IForest  # Isolation Forest from pyod
from tslearn.preprocessing import TimeSeriesScalerMinMax

from utils.annotations import Service


@Service
class TimeOfDayTrendAnalyzer:
    def __init__(self, contamination: float = 0.1):
        """
        Initializes the trend analyzer with a PyOD Isolation Forest.
        :param contamination: Expected proportion of anomalies in the data.
        """
        self.anomaly_detector = IForest(contamination=contamination)
        self.scaler = TimeSeriesScalerMinMax()  # Scales time-series data to range [0, 1]

    def train(self, data: Dict[float, float]):
        """
        Train the anomaly detector using historical data.
        :param data: A dictionary where keys are timestamps and values are queue sizes.
        """
        self.features = data
        self.anomaly_detector.fit(self.features)

    def is_anomalous(
            self,
    ) -> Dict[float, bool]:
        predictions = self.anomaly_detector.predict(self.features)  # 1: normal, 0: anomaly
        return {timestamp: pred == 0 for timestamp, pred in zip(data.keys(), predictions)}
