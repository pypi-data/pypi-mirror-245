# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

import json
from typing import Any
from delpinos.core.encoders.raw_encoder import Factory, RawEncoder


class JsonEncoder(RawEncoder):
    def add_factories(self):
        JsonEncoder.add_factories_encoders(self)

    @classmethod
    def add_factories_encoders(cls, factory: Factory):
        factory.add_factory_impl("encoders.json", JsonEncoder)

    def encode(self, data: Any) -> Any:
        if isinstance(data, str):
            return data
        return json.dumps(data, default=str)

    def decode(self, data: Any) -> Any:
        return json.loads(data)
