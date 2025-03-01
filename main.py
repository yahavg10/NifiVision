import logging
import os

from configurations.developer.developer_variables import container
from src.utils.function_utils import print_model_details

logger = logging.getLogger(os.getenv("ENV"))


def main():
    ds = container.get_service("DataSource")
    parser = container.get_service("Parser")
    trainer = container.get_service("Trainer")
    analyzer = container.get_service("Analyzer")

    # raw_metrics = ds.get_metrics()
    raw_metrics = [
    {
        'metric': {
            '__name__': 'nifi_connection_queued_flowfiles',
            'connection_id': '1234-5678-90ab-cdef',
            'connection_name': 'From ProcessorA to ProcessorB'
        },
        'values': [
            (1672531200, 10),  # Timestamp in Unix time and the queue size value
            (1672534800, 15),
            (1672538400, 5)
        ]
    },
    {
        'metric': {
            '__name__': 'nifi_connection_queued_flowfiles',
            'connection_id': '1234-5678-90ab-cdef',
            'connection_name': 'From ProcessorA to ProcessorB'
        },
        'values': [
            (1672531200, 45), 
            (1672534800, 32),
            (1672538400, 5)
        ]
    },
    {
        'metric': {
            '__name__': 'nifi_connection_queued_flowfiles',
            'connection_id': '1234-5678-90ab-cdef',
            'connection_name': 'From ProcessorA to ProcessorB'
        },
        'values': [
            (1672531200, 14),
            (1672534800, 75),
            (1672538400, 90)
        ]
    },
    {
        'metric': {
            '__name__': 'nifi_connection_queued_flowfiles',
            'connection_id': '5678-1234-90ab-cdef',
            'connection_name': 'From ProcessorB to ProcessorC'
        },
        'values': [
            (1672531200, 20),
            (1672534800, 25),
            (1672538400, 30)
        ]
    }
]

    parsed_metrics = parser.parse(raw_metrics)
    trained_model = trainer.train(parsed_metrics)
    df = analyzer.analyze(trained_model, df=parsed_metrics)
    print(df)

if __name__ == "__main__":
    main()