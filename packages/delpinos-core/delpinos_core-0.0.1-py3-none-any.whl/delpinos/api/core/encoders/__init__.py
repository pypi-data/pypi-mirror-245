# -*- coding: utf-8 -*-
# pylint: disable=C0103

from typing import Any
from delpinos.core.factories.factory import Factory
from delpinos.api.core.encoders.api_encoder import ApiEncoder
from delpinos.api.core.encoders.api_encoder_abstract import ApiEncoderAbstract
from delpinos.api.core.encoders.json_encoder import JsonEncoder
from delpinos.api.core.encoders.raw_encoder import RawEncoder
from delpinos.api.core.encoders.text_encoder import TextEncoder


class Encoder(ApiEncoder):
    def __init__(self, fmt: str = "json", **kwargs):
        self._fmt = fmt
        super().__init__(**kwargs)

    @classmethod
    def add_factories_encoders(cls, factory: Factory):
        factory.add_factory_impl("api.encoders.raw", RawEncoder)
        factory.add_factory_impl("api.encoders.file", RawEncoder)
        factory.add_factory_impl("api.encoders.text", TextEncoder)
        factory.add_factory_impl("api.encoders.json", JsonEncoder)

    @property
    def fmt(self) -> str:
        return self._fmt

    @property
    def impl(self) -> ApiEncoderAbstract:
        return self.instance(f"api.encoders.{self.fmt}", ApiEncoderAbstract)

    def encode(self, data: Any) -> Any:
        return self.impl.encode(data)

    def decode(self, data: Any) -> Any:
        return self.impl.decode(data)
