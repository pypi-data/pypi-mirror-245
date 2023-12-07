# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from types import FunctionType
from typing import Any, Callable, Type
from delpinos.core.container import Container
from delpinos.core.container_abstract import ContainerAbstract
from delpinos.core.functions.dict_function import dict_merge
from delpinos.core.factories.factory_abstract import FactoryAbstract


class Factory(FactoryAbstract, Container):
    __factories__: ContainerAbstract
    __singleton__: ContainerAbstract

    def __init__(self, **kwargs):
        self.__factories__ = self.build_singleton(**kwargs)
        self.__singleton__ = self.build_factories(**kwargs)
        super().__init__(**kwargs)
        self.set(
            "__factories__",
            self.get("__factories__") or self.build_singleton(**kwargs),
            tp=ContainerAbstract,
        )
        self.set(
            "__singleton__",
            self.get("__singleton__") or self.build_factories(**kwargs),
            tp=ContainerAbstract,
        )
        singleton_name = self.build_factory_name()
        if not self.singleton.get(singleton_name):
            self.singleton.set(singleton_name, self)
        self.add_factories()

    def build_singleton(self, **kwargs) -> ContainerAbstract:
        return Container()

    def build_factories(self, **kwargs) -> ContainerAbstract:
        return Container()

    @property
    def singleton(self) -> ContainerAbstract:
        return self.get("__singleton__", ContainerAbstract)

    @property
    def factories(self) -> ContainerAbstract:
        return self.get("__factories__", ContainerAbstract)

    def add_factories(self):
        return

    def build_factory_name(self) -> str:
        return "factory"

    def build_factory_key(self, key: str) -> str:
        return key

    def add_factory(self, key: str, factory: Callable[[Any], Any]):
        factory_key = self.build_factory_key(key)
        self.factories.set(factory_key, factory, tp=FunctionType)

    def add_factory_impl(self, key: str, cls: Type[FactoryAbstract]):
        factory_key = self.build_factory_key(key)
        self.add_factory(factory_key, lambda kwargs: cls(**kwargs))

    def add_factory_context(self, key: str, factory: Callable[[Any], Any]):
        factory_key = self.build_factory_key(key)
        self.__factories__.set(factory_key, factory, tp=FunctionType)

    def get_factory(self, key: str) -> Callable[[Any], Any]:
        factory_key = self.build_factory_key(key)
        return self.factories.get(factory_key, FunctionType)

    def get_factory_context(self, key: str) -> Callable[[Any], Any]:
        factory_key = self.build_factory_key(key)
        factory = self.__factories__.get(factory_key)
        if isinstance(factory, FunctionType):
            return factory
        return self.get_factory(key)

    def instance(self, key: str, tp: type | None = None, **kwargs) -> Any:
        value = self.singleton.get(key)
        if tp and isinstance(value, tp):
            return value
        value = self.factory(key, tp, **kwargs)
        self.singleton.set(key, value, tp=tp)
        return value

    def instance_context(self, key: str, tp: type | None = None, **kwargs) -> Any:
        value = self.__singleton__.get(key)
        if tp and isinstance(value, tp):
            return value
        value = self.factory_context(key, tp, **kwargs)
        self.__singleton__.set(key, value, tp=tp)
        return value

    def factory(self, key: str, tp: type | None = None, **kwargs) -> Any:
        kwargs = dict_merge(self.values(), kwargs)
        factory = self.get_factory(key)
        value = factory(kwargs)
        self.required_value_isinstance(value, tp, f"instance.{key}")
        if isinstance(value, ContainerAbstract):
            value.set(self.build_factory_name(), self)
        return value

    def factory_context(self, key: str, tp: type | None = None, **kwargs) -> Any:
        kwargs = dict_merge(self.values(), kwargs)
        factory = self.get_factory_context(key)
        value = factory(kwargs)
        self.required_value_isinstance(value, tp, f"instance_context.{key}")
        if isinstance(value, ContainerAbstract):
            value.set(self.build_factory_name(), self)
        return value
