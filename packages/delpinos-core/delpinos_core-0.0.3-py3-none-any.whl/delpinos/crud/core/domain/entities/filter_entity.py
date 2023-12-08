# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Dict, List
from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.entities.filter_field_entity import FilterFieldEntity


class FilterEntity(BaseEntity):
    model_config = ConfigDict(title="Filter")

    and_: List[FilterFieldEntity] = Field(
        default=None,
        alias="and",
        title="And Conditions",
        description="And Conditions",
        examples=[[FilterFieldEntity(field="name", op="like", value="TE%")]],
    )
    or_: List[FilterFieldEntity] = Field(
        default=None,
        alias="or",
        title="Or Conditions",
        description="Or Conditions",
        examples=[[FilterFieldEntity(field="name", op="like", value="%TE")]],
    )
    not_: List[FilterFieldEntity] = Field(
        default=None,
        alias="not",
        title="Not Conditions",
        description="Not Conditions",
        examples=[[FilterFieldEntity(field="name", op="like", value="%A%")]],
    )
