import importlib.util
import inspect
import logging
import os
from types import ModuleType
from typing import List, Type, Any

from src.utils import app_config

logger = logging.getLogger(os.getenv("ENV"))


def load_module_from_file(file_path: str) -> ModuleType:
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    module_spec = importlib.util.spec_from_file_location(module_name, file_path)
    module_object = importlib.util.module_from_spec(module_spec)
    if module_spec and module_spec.loader:
        logger.debug(f"Loading module: {module_name} from file: {file_path}")
        module_spec.loader.exec_module(module_object)
    return module_object


def find_classes_in_module(module: ModuleType) -> List[Type]:
    return [
        class_member
        for _, class_member in inspect.getmembers(module, inspect.isclass)
        if class_member.__module__ == module.__name__
    ]


def find_classes_in_directory(directory_path) -> List[Type]:
    discovered_classes = []
    for root_dir, _, files_in_dir in os.walk(directory_path):
        for file_name in files_in_dir:
            if file_name.endswith(".py") and not file_name.startswith("__"):
                full_file_path = os.path.join(root_dir, file_name)
                loaded_module = load_module_from_file(full_file_path)
                classes_in_current_module = find_classes_in_module(loaded_module)
                discovered_classes.extend(classes_in_current_module)
    return discovered_classes


def has_init_without_params(cls: Type) -> bool:
    class_init_method = getattr(cls, "__init__", None)
    if class_init_method is None:
        return True  # Default __init__ exists with no parameters

    init_signature = inspect.signature(class_init_method)
    # Exclude 'self' and check parameter requirements
    for param_name, param_details in init_signature.parameters.items():
        if param_name == "self":
            continue
        # If parameter is positional-only or positional-or-keyword and has no default value, return False
        if (
                param_details.default is inspect.Parameter.empty
                and param_details.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ):
            return False
        # If parameter is *args or **kwargs, we can always call the constructor without arguments
        if param_details.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            return True
    return True


def create_class_instances(classes: List[Type]) -> List[Any]:
    class_instances = []
    for class_type in classes:
        try:
            if not has_init_without_params(class_type):
                class_config = app_config.datasources.datasources.get(class_type.__name__)
                instance = class_type(class_config)
            else:
                instance = class_type()
            class_instances.append(instance)
        except TypeError as error:
            logger.warning(f"Skipping {class_type.__module__}.{class_type.__name__} due to error: {error}")
    return class_instances


def filter_enabled_instances(instances: List[Any], component_type: str) -> List[Any]:
    component_config = get_component_config_object(component_type)
    component_settings = get_component_configurations(component_config)
    max_instances = get_instances_limit(component_type)
    enabled_component_instances = get_enabled_instances(instances, component_settings, max_instances)
    return enabled_component_instances


def get_component_config_object(component_type: str) -> Any:
    component_config_attribute = f"{component_type}s"
    component_configuration = getattr(app_config, component_config_attribute, None)
    if not component_configuration:
        logger.error(f"No configuration found for component type: {component_type}s")
        raise AttributeError(f"No configuration found for component type: {component_type}s")
    return component_configuration


def get_component_configurations(component_config_object: Any) -> Any:
    configuration_attributes = ["datasources", "parsers", "analyzers", "trainers"]
    for config_attr in configuration_attributes:
        if hasattr(component_config_object, config_attr):
            return getattr(component_config_object, config_attr)
    logger.debug("No matching configuration attribute found in component config object")
    return None


def get_instances_limit(component_type: str) -> int:
    limit_per_component = 1 if component_type != "parsers" else 100
    return limit_per_component


def get_enabled_instances(instances: List[Any], component_configurations: Any, instances_limit: int) -> List[Any]:
    if component_configurations is None:
        logger.debug("No component configurations found, returning empty list of enabled instances")
        return []
    enabled_instances_list = [
        instance for instance in instances
        if component_configurations.get(type(instance).__name__, {}).enabled
    ]
    return enabled_instances_list[:instances_limit]


def initialize_components(path: str) -> List[Any]:
    discovered_classes = find_classes_in_directory(directory_path=path)

    class_instances = create_class_instances(classes=discovered_classes)

    component_type_name = os.path.basename(os.path.dirname(path))

    enabled_instances_list = filter_enabled_instances(instances=class_instances, component_type=component_type_name)
    logger.info(f"Initialization complete: {len(enabled_instances_list)} enabled instances ready for use")
    return enabled_instances_list
