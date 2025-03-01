import logging
from typing import Any

import pandas as pd

from src.components.analyzer.base import Analyzer
from src.utils.annotations import Service

logger = logging.getLogger(__name__)


@Service
class IsolationForestAnalyzer(Analyzer):
    def analyze(self, model: Any, df: pd.DataFrame) -> pd.DataFrame:
        # Prepare data for prediction
        X = df[['value']].values

        # Predict anomalies (-1 for anomaly, 1 for normal)
        predictions = model.predict(X)

        # Add predictions to the DataFrame
        df['anomaly'] = predictions == -1  # Convert -1 to True for anomaly

        num_anomalies = df['anomaly'].sum()
        logger.info(f"Analysis completed. Total anomalies detected: {num_anomalies}")

        return df
