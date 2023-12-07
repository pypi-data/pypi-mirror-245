# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from typing import Any
from delpinos.core.encoders.raw_encoder import Factory, RawEncoder


class TextEncoder(RawEncoder):
    def add_factories(self):
        TextEncoder.add_factories_encoders(self)

    @classmethod
    def add_factories_encoders(cls, factory: Factory):
        factory.add_factory_impl("encoders.text", TextEncoder)

    def encode(self, data: Any) -> Any:
        return str(data)

    def decode(self, data: Any) -> Any:
        return str(data)
