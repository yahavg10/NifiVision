import logging.config as log
import os
from typing import NoReturn

import yaml


def read_configuration(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {file_path}") from e


def setup_logger() -> NoReturn:
    with open(file=os.environ["LOG_CONFIG_PATH"]) as config_file:
        config = yaml.safe_load(config_file.read())
    log.dictConfig(config)
