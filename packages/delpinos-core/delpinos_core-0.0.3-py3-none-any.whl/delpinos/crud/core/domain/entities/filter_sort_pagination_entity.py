# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import List
from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.entities.filter_entity import FilterEntity
from delpinos.crud.core.domain.entities.filter_field_entity import FilterFieldEntity
from delpinos.crud.core.domain.entities.pagination_entity import PaginationEntity
from delpinos.crud.core.domain.entities.sort_field_entity import SortFieldEntity

from delpinos.crud.core.domain.entities import BaseEntity


class FilterSortPaginationEntity(BaseEntity):
    model_config = ConfigDict(title="FilterSortPagination")

    fields: List[str] = Field(
        default=None,
        title="Fields",
        description="Fields",
        examples=[["*"]],
    )
    filter: FilterEntity | List[FilterEntity | FilterFieldEntity] = Field(
        default=None,
        title="Filter",
        description="Filter",
        examples=[[FilterFieldEntity(field="name", op="like", value="TE%")]],
    )
    sort: List[SortFieldEntity] = Field(
        default=None,
        title="Sort",
        description="Sort",
        examples=[[SortFieldEntity(field="name", direction="asc")]],
    )
    pagination: PaginationEntity = Field(
        default=None,
        title="Pagination",
        description="Pagination",
        examples=[PaginationEntity(limit=100, offset=0)],
    )
