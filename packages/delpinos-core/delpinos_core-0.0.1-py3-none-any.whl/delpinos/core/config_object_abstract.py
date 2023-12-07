# -*- coding: utf-8 -*-
# pylint: disable=C0103

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class ConfigObjectAbstract(ABC):
    @abstractmethod
    def build(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def setup(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def validate(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def values(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def get(
        self,
        key: str,
        default: Any = None,
        **kwargs,
    ) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def set(
        self,
        key: str,
        value: Any = None,
        **kwargs,
    ):
        raise NotImplementedError()

    @abstractmethod
    def find_key(
        self,
        *args,
        **kwargs,
    ) -> str | None:
        raise NotImplementedError()

    @abstractmethod
    def find_value(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def required_value_isinstance(
        self, value: Any, tp: type | None = None, name: str = "value"
    ):
        raise NotImplementedError()
