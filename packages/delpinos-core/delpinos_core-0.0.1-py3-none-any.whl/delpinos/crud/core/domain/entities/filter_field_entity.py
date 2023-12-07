# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Any
from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity


class FilterFieldEntity(BaseEntity):
    model_config = ConfigDict(title="FilterField")

    field: str = Field(
        ...,
        title="Field for filter",
        description="Field for filter",
        examples=["name"],
        min_length=1,
    )
    op: str = Field(
        default="==",
        title="Operation for filter",
        description="Operation for filter",
        examples=["=="],
        min_length=1,
    )
    value: Any = Field(
        ...,
        title="Value for filter",
        description="Value for filter",
        examples=["Test"],
    )
