# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from typing import Any
from delpinos.core.factories.factory import Factory
from delpinos.core.encoders.encoder_abstract import EncoderAbstract


class RawEncoder(EncoderAbstract, Factory):
    def add_factories(self):
        RawEncoder.add_factories_encoders(self)

    @classmethod
    def add_factories_encoders(cls, factory: Factory):
        factory.add_factory_impl("encoders.raw", RawEncoder)

    def encode(self, data: Any) -> Any:
        return data

    def decode(self, data: Any) -> Any:
        return data
