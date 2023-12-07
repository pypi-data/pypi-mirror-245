# -*- coding: utf-8 -*-
# pylint: disable=C0114

from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity


class PaginationEntity(BaseEntity):
    model_config = ConfigDict(title="Pagination")

    limit: int = Field(
        default=100,
        title="Limit for results",
        description="Limit for results",
        examples=[100],
    )
    offset: int = Field(
        default=0,
        title="Offset start for  results",
        description="Offset start for results",
        examples=[0],
    )
