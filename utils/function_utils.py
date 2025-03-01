import importlib.util
import inspect
import logging
import os
from types import ModuleType
from typing import List, Type, Any

from utils import app_config

logger = logging.getLogger(os.getenv("ENV"))


def load_module_from_file(file_path: str) -> ModuleType:
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    if spec and spec.loader:
        spec.loader.exec_module(module)
    return module


def find_classes_in_module(module: ModuleType) -> List[Type]:
    return [
        member
        for _, member in inspect.getmembers(module, inspect.isclass)
        if member.__module__ == module.__name__
    ]


def find_classes_in_directory(directory_path) -> List[Type]:
    classes = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(root, file)
                module = load_module_from_file(file_path)
                classes.extend(find_classes_in_module(module))
    return classes

def has_init_without_params(cls: Type) -> bool:
    init_method = getattr(cls, "__init__", None)
    if init_method is None:
        return True  # Default __init__ exists with no parameters

    signature = inspect.signature(init_method)
    # Exclude 'self' and check parameter requirements
    for name, param in signature.parameters.items():
        if name == "self":
            continue
        # If parameter is positional-only or positional-or-keyword and has no default value, return False
        if (
                param.default is inspect.Parameter.empty
                and param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ):
            return False
        # If parameter is *args or **kwargs, we can always call the constructor without arguments
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            return True
    return True

def create_class_instances(classes: List[Type]) -> List[Any]:
    instances = []
    for cls in classes:
        try:
            if not has_init_without_params(cls):
                instance_config = app_config.data_sources.data_sources.get(cls.__name__)
                instance = cls(instance_config)
            else:
                instance = cls()
            instances.append(instance)
        except TypeError:
            print(f"Skipping {cls.__module__}.{cls.__name__} (no parameterless constructor).")
    return instances


def filter_enabled_instances(instances: List[Any], component_type: bool = False) -> List[Any]:
    if component_type:
        searched_components_configurations = app_config.parsers.parsers
    else:
        searched_components_configurations = app_config.data_sources.data_sources
    enabled_instances = [
        instance for instance in instances
        if searched_components_configurations.get(type(instance).__name__).enabled
    ]
    return enabled_instances


def initialize_components(path):
    all_classes = find_classes_in_directory(directory_path=path)
    instances = create_class_instances(all_classes)
    enabled_instances = filter_enabled_instances(instances, component_type="parsers" in path)
    return enabled_instances
