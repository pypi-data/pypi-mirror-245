# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from http import HTTPStatus
from delpinos.core.factories.factory import Factory
from delpinos.api.core.encoders import Encoder
from delpinos.api.core.encoders.json_encoder import JsonEncoder
from delpinos.api.core.encoders.raw_encoder import RawEncoder
from delpinos.api.core.encoders.text_encoder import TextEncoder
from delpinos.api.core.responses.api_response_abstract import (
    ApiResponseAbstract,
    Any,
    Dict,
)


class ApiResponse(ApiResponseAbstract, Factory):
    def __init__(
        self,
        response: Any = None,
        status: int | None = None,
        headers: Dict[str, Any] | None = None,
        mimetype: str | None = None,
        content_type: str | None = None,
        fmt: str | None = None,
        **kwargs,
    ) -> None:
        self._config = {}
        super().__init__(**kwargs)
        self.status = status
        self.headers = headers
        self.mimetype = mimetype
        self.content_type = content_type
        self.response = response
        self.fmt = fmt

    def add_factories(self):
        self.add_factory("api.encoder.raw", lambda kwargs: RawEncoder(**kwargs))
        self.add_factory("api.encoder.file", lambda kwargs: RawEncoder(**kwargs))
        self.add_factory("api.encoder.text", lambda kwargs: TextEncoder(**kwargs))
        self.add_factory("api.encoder.json", lambda kwargs: JsonEncoder(**kwargs))

    @property
    def encoder(self) -> Encoder:
        fmt = self.fmt
        if not fmt:
            if self.mimetype == "json" or self.content_type == "application/json":
                fmt = "json"
        fmt = fmt or "text"
        return Encoder(fmt=fmt, **self.kwargs())

    @property
    def response(self) -> Any:
        return self._config.get("response")

    @response.setter
    def response(self, value: Any):
        self._config["response"] = self.encoder.encode(value)

    @property
    def status(self) -> int | str | HTTPStatus | None:
        return self._config.get("status")

    @status.setter
    def status(self, value: int | str | HTTPStatus | None):
        if isinstance(value, int):
            self._config["status"] = value
        else:
            self._config["status"] = None

    @property
    def headers(self) -> Dict[str, Any] | None:
        return self._config.get("headers")

    @headers.setter
    def headers(self, value: Dict[str, Any] | None):
        if isinstance(value, dict):
            self._config["headers"] = value
        else:
            self._config["headers"] = None

    @property
    def mimetype(self) -> str | None:
        return self._config.get("mimetype")

    @mimetype.setter
    def mimetype(self, value: str | None):
        if isinstance(value, str):
            self._config["mimetype"] = value
        else:
            self._config["mimetype"] = None

    @property
    def content_type(self) -> str | None:
        return self._config.get("content_type")

    @content_type.setter
    def content_type(self, value: str | None):
        if isinstance(value, str):
            self._config["content_type"] = value
        else:
            self._config["content_type"] = None

    @property
    def fmt(self) -> str | None:
        return self._config.get("fmt")

    @fmt.setter
    def fmt(self, value: str | None):
        if isinstance(value, str):
            self._config["fmt"] = value
        else:
            self._config["fmt"] = None
