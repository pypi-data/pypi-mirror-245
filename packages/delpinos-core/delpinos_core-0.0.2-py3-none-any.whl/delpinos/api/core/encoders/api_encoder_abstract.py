# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from abc import abstractmethod
from typing import Any
from delpinos.core.factories.factory_abstract import FactoryAbstract


class ApiEncoderAbstract(FactoryAbstract):
    @abstractmethod
    def encode(self, data: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def decode(self, data: Any) -> Any:
        raise NotImplementedError()
