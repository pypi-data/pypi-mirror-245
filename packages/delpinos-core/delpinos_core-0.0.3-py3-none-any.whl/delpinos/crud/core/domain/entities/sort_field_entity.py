# -*- coding: utf-8 -*-
# pylint: disable=C0114

from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity


class SortFieldEntity(BaseEntity):
    model_config = ConfigDict(title="FilterField")

    field: str = Field(
        ...,
        title="Field for filter",
        description="Field for filter",
        examples=["name"],
        min_length=1,
    )
    direction: str = Field(
        default="asc",
        title="Direction for sorting",
        description="Direction for sorting",
        examples=["asc"],
        min_length=1,
    )
    nullsfirst: bool = Field(
        default=None,
        title="Nulls first",
        description="Nulls first",
        examples=[True],
    )
    nullslast: bool = Field(
        default=None,
        title="Nulls last",
        description="Nulls last",
        examples=[True],
    )
