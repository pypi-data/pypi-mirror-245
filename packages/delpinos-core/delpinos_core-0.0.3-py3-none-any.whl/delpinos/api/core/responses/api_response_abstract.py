# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from abc import abstractmethod

from http import HTTPStatus

from typing import Any, Dict
from delpinos.api.core.encoders import Encoder
from delpinos.core.factories.factory_abstract import FactoryAbstract


class ApiResponseAbstract(FactoryAbstract):
    @property
    @abstractmethod
    def encoder(self) -> Encoder:
        raise NotImplementedError()

    @property
    @abstractmethod
    def response(self) -> Any:
        raise NotImplementedError()

    @response.setter
    @abstractmethod
    def response(self, value: Any):
        raise NotImplementedError()

    @property
    @abstractmethod
    def status(self) -> int | str | HTTPStatus | None:
        raise NotImplementedError()

    @status.setter
    def status(self, value: int | str | HTTPStatus | None):
        raise NotImplementedError()

    @property
    @abstractmethod
    def headers(self) -> Dict[str, Any] | None:
        raise NotImplementedError()

    @headers.setter
    @abstractmethod
    def headers(self, value: Dict[str, Any] | None):
        raise NotImplementedError()

    @property
    @abstractmethod
    def mimetype(self) -> str | None:
        raise NotImplementedError()

    @mimetype.setter
    @abstractmethod
    def mimetype(self, value: str | None):
        raise NotImplementedError()

    @property
    @abstractmethod
    def content_type(self) -> str | None:
        raise NotImplementedError()

    @content_type.setter
    @abstractmethod
    def content_type(self, value: str | None):
        raise NotImplementedError()

    @property
    @abstractmethod
    def fmt(self) -> str | None:
        raise NotImplementedError()

    @fmt.setter
    @abstractmethod
    def fmt(self, value: str | None):
        raise NotImplementedError()
