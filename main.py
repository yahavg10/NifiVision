from pydantic import ValidationError

from configurations.developer.models import ParserSystemConfig, DataSourceConfig
from utils.file_utils import read_configuration

config_data = read_configuration("configurations//developer//developer.yml")

def main():
    try:
        parser_config = ParserSystemConfig(**read_configuration("configurations//developer//developer.yml")["parser_system"])
        ds_config = DataSourceConfig(**config_data["data_source"])
        print(parser_config)
        print(ds_config)
    except ValidationError as e:
        print("Validation Error:", e)


if __name__ == "__main__":
    main()