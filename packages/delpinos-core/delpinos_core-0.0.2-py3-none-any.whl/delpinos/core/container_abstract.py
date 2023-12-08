# -*- coding: utf-8 -*-
# pylint: disable=C0103

from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from delpinos.core.config_object_abstract import ConfigObjectAbstract


class ContainerAbstract(ConfigObjectAbstract):
    @property
    @abstractmethod
    def config_key(self) -> str:
        return ""

    @property
    @abstractmethod
    def config_class(self) -> Type[ConfigObjectAbstract]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def variables_class(self) -> Type[ConfigObjectAbstract]:
        raise NotImplementedError()
