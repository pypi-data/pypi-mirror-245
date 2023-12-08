# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from typing import Any, Callable, Type
from delpinos.core.container_abstract import ContainerAbstract, abstractmethod


class FactoryAbstract(ContainerAbstract):
    @property
    @abstractmethod
    def singleton(self) -> ContainerAbstract:
        raise NotImplementedError()

    @property
    @abstractmethod
    def factories(self) -> ContainerAbstract:
        raise NotImplementedError()

    @abstractmethod
    def build_singleton(self, **kwargs) -> ContainerAbstract:
        raise NotImplementedError()

    @abstractmethod
    def build_factories(self, **kwargs) -> ContainerAbstract:
        raise NotImplementedError()

    @abstractmethod
    def add_factories(self):
        raise NotImplementedError()

    @abstractmethod
    def build_factory_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def build_factory_key(self, key: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def add_factory(self, key: str, factory: Callable[[Any], Any]):
        raise NotImplementedError()

    def add_factory_impl(self, name: str, cls: Type["FactoryAbstract"]):
        raise NotImplementedError()

    @abstractmethod
    def add_factory_context(self, key: str, factory: Callable[[Any], Any]):
        raise NotImplementedError()

    @abstractmethod
    def get_factory(self, key: str) -> Callable[[Any], Any]:
        raise NotImplementedError()

    @abstractmethod
    def get_factory_context(self, key: str) -> Callable[[Any], Any]:
        raise NotImplementedError()

    @abstractmethod
    def instance(self, key: str, tp: type | None = None, **kwargs) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def instance_context(self, key: str, tp: type | None = None, **kwargs) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def factory(self, key: str, tp: type | None = None, **kwargs) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def factory_context(self, key: str, tp: type | None = None, **kwargs) -> Any:
        raise NotImplementedError()
