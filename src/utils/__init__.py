from configurations.developer.models import AppConfig
from src.utils.file_utils import read_configuration, setup_logger

app_config = AppConfig(**read_configuration("configurations//developer//developer.yml"))
setup_logger()
