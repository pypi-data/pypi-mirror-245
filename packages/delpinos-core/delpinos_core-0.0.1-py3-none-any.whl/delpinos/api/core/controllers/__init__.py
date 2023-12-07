# -*- coding: utf-8 -*-
# pylint: disable=C0103

from typing import Callable, List
from delpinos.api.core.controllers.api_controller import (
    Factory,
    ApiController,
    ApiControllerAbstract,
)
from delpinos.api.core.controllers.api_controller_abstract import (
    ApiControllerAbstract,
    ApiResponseAbstract,
)
from delpinos.api.core.requests.api_request_abstract import ApiRequestAbstract


class Controller(ApiController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_endpoints()

    @classmethod
    def add_factories_controllers(cls, factory: Factory):
        factory.add_factory_impl("api.controllers.api_controller", ApiController)

    @property
    def impl(self) -> ApiControllerAbstract:
        return self.instance("api.controllers.api_controller", ApiControllerAbstract)

    def add_endpoint(
        self,
        endpoint: str,
        callback: Callable[..., ApiResponseAbstract],
        methods: List[str],
    ) -> "ApiControllerAbstract":
        return self.impl.add_endpoint(endpoint, callback, methods)
