# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from delpinos.api.core.responses.api_response import (
    Factory,
    ApiResponse,
    ApiResponseAbstract,
    Encoder,
    HTTPStatus,
    Any,
    Dict,
)


class Response(ApiResponse):
    @property
    def impl(self) -> ApiResponseAbstract:
        return self.instance("api.responses.api_response", ApiResponseAbstract)

    @classmethod
    def add_factories_responses(cls, factory: Factory):
        factory.add_factory_impl("api.responses.api_response", ApiResponse)

    @property
    def encoder(self) -> Encoder:
        return self.impl.encoder

    @property
    def response(self) -> Any:
        return self.impl.response

    @response.setter
    def response(self, value: Any):
        self.impl.response = value

    @property
    def status(self) -> int | str | HTTPStatus | None:
        return self.impl.status

    @status.setter
    def status(self, value: int | str | HTTPStatus | None):
        self.impl.status = value

    @property
    def headers(self) -> Dict[str, Any] | None:
        return self.impl.headers

    @headers.setter
    def headers(self, value: Dict[str, Any] | None):
        self.impl.headers = value

    @property
    def mimetype(self) -> str | None:
        return self.impl.mimetype

    @mimetype.setter
    def mimetype(self, value: str | None):
        self.impl.mimetype = value

    @property
    def content_type(self) -> str | None:
        return self.impl.content_type

    @content_type.setter
    def content_type(self, value: str | None):
        self.impl.content_type = value
