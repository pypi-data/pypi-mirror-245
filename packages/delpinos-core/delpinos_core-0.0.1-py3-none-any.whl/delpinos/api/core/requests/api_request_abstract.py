# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from abc import abstractmethod
from typing import Any, Dict, List

from delpinos.core.factories.factory_abstract import FactoryAbstract


class ApiRequestAbstract(FactoryAbstract):
    @property
    @abstractmethod
    def method(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def data(self) -> Dict[str, Any] | List[Dict[str, Any]]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def body(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def query(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def form(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def headers(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def cookies(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def files(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def get_content(
        self,
        encoding: str = "utf-8",
        errors: str = "strict",
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_authorization(self, token_type=None, token: str | None = None) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_basic_authorization(self) -> Dict[str, Any]:
        raise NotImplementedError()
