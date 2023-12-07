# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from typing import Any
from delpinos.core.factories.factory import Factory
from delpinos.api.core.encoders.api_encoder_abstract import ApiEncoderAbstract


class ApiEncoder(ApiEncoderAbstract, Factory):
    def encode(self, data: Any) -> Any:
        return data

    def decode(self, data: Any) -> Any:
        return data
