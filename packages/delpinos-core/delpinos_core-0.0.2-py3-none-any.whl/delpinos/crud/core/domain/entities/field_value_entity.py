# -*- coding: utf-8 -*-
# pylint: disable=C0114

from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity


class FieldValueEntity(BaseEntity):
    model_config = ConfigDict(title="FieldValue")

    field: str = Field(
        ...,
        title="Field",
        description="Field",
        examples=["name"],
        min_length=1,
    )
    value: str = Field(
        ...,
        title="Value",
        description="Value",
        examples=["Test"],
        min_length=1,
    )
