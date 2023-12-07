# -*- coding: utf-8 -*-
# pylint: disable=C0103

from typing import List
from delpinos.core.factories.factory import Factory
from delpinos.api.core.controllers.api_controller_abstract import (
    ApiRequestAbstract,
    ApiControllerAbstract,
    ApiResponseAbstract,
    Any,
    Callable,
    Dict,
)


class ApiController(ApiControllerAbstract, Factory):
    @property
    def request(self) -> ApiRequestAbstract:
        return self.instance("api.requests.api_request", ApiRequestAbstract)

    def response(
        self,
        response: Any = None,
        status: int | None = None,
        headers: Dict[str, Any] | None = None,
        mimetype: str | None = None,
        content_type: str | None = None,
        fmt: str | None = None,
        **kwargs,
    ) -> ApiResponseAbstract:
        kwargs = {**self.kwargs(), **kwargs}
        kwargs["response"] = response
        kwargs["status"] = status
        kwargs["headers"] = headers
        kwargs["mimetype"] = mimetype
        kwargs["content_type"] = content_type
        kwargs["fmt"] = fmt
        key = "api.responses.api_response"
        factory = self.get_factory(key)
        value = factory(kwargs)
        self.required_value_isinstance(
            value,
            ApiResponseAbstract,
            f"instance.{key}",
        )
        return value

    def add_endpoint(
        self,
        endpoint: str,
        callback: Callable[..., ApiResponseAbstract],
        methods: List[str],
    ) -> "ApiController":
        raise NotImplementedError()

    def add_endpoints(self):
        raise NotImplementedError()
