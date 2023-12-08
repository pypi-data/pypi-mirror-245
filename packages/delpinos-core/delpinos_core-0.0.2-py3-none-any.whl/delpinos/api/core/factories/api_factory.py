from typing import Type, Any, Dict
from delpinos.api.core.controllers.api_controller_abstract import ApiControllerAbstract
from delpinos.core.factories.factory import Factory
from delpinos.api.core.encoders import Encoder
from delpinos.api.core.controllers import Controller
from delpinos.api.core.requests import Request
from delpinos.api.core.responses import Response
from delpinos.api.core.factories.api_factory_abstract import (
    ApiFactoryAbstract,
)


class ApiFactory(ApiFactoryAbstract, Factory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_controllers()

    @property
    def app(self) -> Any:
        raise NotImplementedError()

    @property
    def api_config(self) -> Dict[str, Any]:
        return self.get("api.config", dict)

    @property
    def debug(self) -> bool:
        return self.get("api.debug", bool)

    @property
    def controllers(self) -> Dict[str, Type[ApiControllerAbstract]]:
        return {}

    def add_controllers(self):
        for controller_name, controller_class in self.controllers.items():
            key = f"api.controllers.impl.{controller_name}"
            self.add_factory_impl(key, controller_class)
            self.instance(key, controller_class)

    def add_factories_controllers(self):
        Controller.add_factories_controllers(self)

    def add_factories_encoders(self):
        Encoder.add_factories_encoders(self)

    def add_factories_requests(self):
        Request.add_factories_requests(self)

    def add_factories_responses(self):
        Response.add_factories_responses(self)

    def add_factories(self):
        self.add_factories_controllers()
        self.add_factories_encoders()
        self.add_factories_requests()
        self.add_factories_responses()

    def run(self) -> Any:
        self.server()

    def server(self):
        raise NotImplementedError()
