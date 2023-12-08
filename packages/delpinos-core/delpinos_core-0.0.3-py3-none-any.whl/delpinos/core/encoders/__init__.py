# -*- coding: utf-8 -*-
# pylint: disable=C0103

from typing import Any
from delpinos.core.factories.factory import Factory
from delpinos.core.encoders.raw_encoder import RawEncoder
from delpinos.core.encoders.encoder_abstract import EncoderAbstract
from delpinos.core.encoders.json_encoder import JsonEncoder
from delpinos.core.encoders.raw_encoder import RawEncoder
from delpinos.core.encoders.text_encoder import TextEncoder


class Encoder(RawEncoder):
    def __init__(self, fmt: str = "json", **kwargs):
        self._fmt = fmt
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        factory_key = self.build_factory_key(self._fmt)
        singleton = self.singleton.get(self._fmt)
        factory = self.factories.get(factory_key)
        if not (singleton or factory):
            self._fmt = "raw"

    def add_factories(self):
        Encoder.add_factories_encoders(self)

    @classmethod
    def add_factories_encoders(cls, factory: Factory):
        RawEncoder.add_factories_encoders(factory)
        TextEncoder.add_factories_encoders(factory)
        JsonEncoder.add_factories_encoders(factory)

    @property
    def fmt(self) -> str:
        return self._fmt

    @property
    def impl(self) -> EncoderAbstract:
        return self.instance(f"encoders.{self.fmt}", EncoderAbstract)

    def encode(self, data: Any) -> Any:
        return self.impl.encode(data)

    def decode(self, data: Any) -> Any:
        return self.impl.decode(data)
