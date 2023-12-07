# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

import json
from typing import Any
from delpinos.api.core.encoders.api_encoder import ApiEncoder


class JsonEncoder(ApiEncoder):
    def encode(self, data: Any) -> Any:
        if isinstance(data, str):
            return data
        return json.dumps(data, default=str)

    def decode(self, data: Any) -> Any:
        return json.loads(data)
