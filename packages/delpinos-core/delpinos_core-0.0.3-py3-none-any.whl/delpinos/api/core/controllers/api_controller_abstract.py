# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from abc import abstractmethod
from typing import Any, Dict, Callable, List
from delpinos.api.core.requests.api_request_abstract import ApiRequestAbstract
from delpinos.api.core.responses.api_response_abstract import ApiResponseAbstract
from delpinos.core.factories.factory_abstract import FactoryAbstract


class ApiControllerAbstract(FactoryAbstract):
    @property
    @abstractmethod
    def request(self) -> ApiRequestAbstract:
        raise NotImplementedError()

    @abstractmethod
    def response(
        self,
        response: Any = None,
        status: int | None = None,
        headers: Dict[str, Any] | None = None,
        mimetype: str | None = None,
        content_type: str | None = None,
        **kwargs,
    ) -> ApiResponseAbstract:
        raise NotImplementedError()

    @abstractmethod
    def add_endpoint(
        self,
        endpoint: str,
        callback: Callable[..., ApiResponseAbstract],
        methods: List[str],
    ) -> "ApiControllerAbstract":
        raise NotImplementedError()

    @abstractmethod
    def add_endpoints(self):
        raise NotImplementedError()
