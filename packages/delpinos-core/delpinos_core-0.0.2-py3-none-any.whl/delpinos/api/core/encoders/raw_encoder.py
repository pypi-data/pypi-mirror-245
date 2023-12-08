# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from typing import Any
from delpinos.api.core.encoders.api_encoder import ApiEncoder


class RawEncoder(ApiEncoder):
    def encode(self, data: Any) -> Any:
        return data

    def decode(self, data: Any) -> Any:
        return data
