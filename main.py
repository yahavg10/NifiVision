from pydantic import ValidationError

from configurations.developer.models import ParserSystemConfig
from utils.file_utils import read_configuration

config_data = read_configuration("configurations//developer//developer.yml")

def main():
    try:
        parser_config = ParserSystemConfig(**config_data["parser_system"])
        print(parser_config)
    except ValidationError as e:
        print("Validation Error:", e)


if __name__ == "__main__":
    main()