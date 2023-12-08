# -*- coding: utf-8 -*-
# pylint: disable=C0114

from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.enums.entities.schema_entities_enum import (
    SchemaFieldTypeEnum,
)


class FieldSchemaEntity(BaseEntity):
    model_config = ConfigDict(title="FieldSchema")

    name: str = Field(
        ...,
        title="Field Name",
        description="Field Name",
        examples=["name"],
        min_length=1,
    )
    type: SchemaFieldTypeEnum = Field(
        ...,
        title="Field Type",
        description="Field Type",
        examples=[SchemaFieldTypeEnum.VARCHAR.value],
        min_length=1,
    )
    options: dict = Field(
        default=None,
        title="Field Options",
        description="Field Options",
        examples=["{}"],
    )
