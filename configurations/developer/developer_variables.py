from utils import app_config
from utils.container import IoCContainer
from utils.function_utils import initialize_components

container = IoCContainer()

for instance in initialize_components(app_config.data_sources.path):
    container.register(type(instance), instance)

for instance in initialize_components(app_config.parsers.path):
    container.register(type(instance), instance)