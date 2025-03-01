import inspect
from functools import wraps
from typing import NoReturn, Any, List

from src.components.parser.parser import Parser


class IoCContainer:
    def __init__(self):
        self.services = {}

    def register(self, cls, service_instance, **kwargs) -> NoReturn:
        if getattr(cls, "_is_service", False):
            service_name = cls.__name__

            for attr_name in dir(service_instance):
                method = getattr(service_instance, attr_name)

                if callable(method) and getattr(method, '_is_inject', False):
                    wrapped_method = self._inject_dependencies(method)
                    setattr(service_instance, attr_name, wrapped_method)

            self.services[service_name] = service_instance

    def get_service(self, service_name: str) -> Any:
        if "Parser" not in service_name:
            for service in self.services.keys():
                if service_name in service:
                    return self.services.get(service)
        if "Parser" in service_name:
            parser = Parser()
            parser.register_parsers([self.services.get(service) for service in self.services.keys() if service_name in service])
            return parser

    def get_services(self, *service_names) -> List[Any]:
        services = [self.get_service(name) for name in service_names]
        return [service for service in services if service is not None]

    def _inject_dependencies(self, func):
        dependencies = func._dependencies

        @wraps(func)
        def wrapper(*args, **kwargs):
            injected_args = [self.get_service(dep) for dep in dependencies]
            return func(*injected_args, *args, **kwargs)

        return wrapper

    def register_functions_in_module(self, module) -> NoReturn:
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if hasattr(func, "_is_inject") and getattr(func, "_is_inject"):
                self.register_function(func)

    def register_function(self, func) -> NoReturn:
        if getattr(func, "_is_inject", False):
            wrapped_func = self._inject_dependencies(func)
            self.services[func.__name__] = wrapped_func