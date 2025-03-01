from configurations.developer.models import AppConfig
from utils.file_utils import read_configuration

app_config = AppConfig(**read_configuration("configurations//developer//developer.yml"))
