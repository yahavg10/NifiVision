from src.utils import app_config
from src.utils.container import IoCContainer
from src.utils.function_utils import initialize_components

container = IoCContainer()

for instance in initialize_components(app_config.datasources.path):
    container.register(type(instance), instance)

for instance in initialize_components(app_config.parsers.path):
    container.register(type(instance), instance)

for instance in initialize_components(app_config.trainers.path):
    container.register(type(instance), instance)

for instance in initialize_components(app_config.analyzers.path):
    container.register(type(instance), instance)
