from typing import Any, Dict, Type
from abc import abstractmethod
from delpinos.api.core.controllers.api_controller_abstract import ApiControllerAbstract
from delpinos.core.factories.factory_abstract import FactoryAbstract


class ApiFactoryAbstract:
    @property
    @abstractmethod
    def app(self) -> Any:
        raise NotImplementedError()

    @property
    @abstractmethod
    def api_config(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def debug(self) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def controllers(self) -> Dict[str, ApiControllerAbstract]:
        raise NotImplementedError()

    @abstractmethod
    def add_factories_controllers(self):
        raise NotImplementedError()

    @abstractmethod
    def add_factories_encoders(self):
        raise NotImplementedError()

    @abstractmethod
    def add_factories_requests(self):
        raise NotImplementedError()

    @abstractmethod
    def add_factories_responses(self):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    @abstractmethod
    def server(self):
        raise NotImplementedError()
