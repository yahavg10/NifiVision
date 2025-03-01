from typing import Dict

import numpy as np
import pandas as pd

from src.components.parser.base import AbstractParser
from src.utils.annotations import Service


@Service
class TimeSeriesParser(AbstractParser):
    def parse(self, data: Dict[float, float]) -> np.ndarray:
        """
        Preprocess data by scaling and extracting hour-of-day features.
        :param data: A dictionary where keys are timestamps and values are queue sizes.
        :return: Preprocessed feature array for training.
        """
        # Create a DataFrame for easier manipulation
        df = pd.DataFrame.from_dict(data, orient="index", columns=["queue_size"])
        df.index = pd.to_datetime(df.index, unit="s")
        df["hour"] = df.index.hour  # Extract hour of the day

        # Combine hour and queue size as features and scale them
        features = df[["hour", "queue_size"]].to_numpy()
        scaled_features = self.scaler.fit_transform(features)
        return scaled_features
