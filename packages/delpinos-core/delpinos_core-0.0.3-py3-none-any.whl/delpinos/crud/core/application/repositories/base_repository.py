# -*- coding: utf-8 -*-
# pylint: disable=C0114,C0103,W0622

from typing import Any, Dict, List, Type
from delpinos.core.factories.factory import Factory
from delpinos.core.encoders import EncoderAbstract
from delpinos.core.exceptions.badrequest_exception import BadRequestException
from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.entities.filter_entity import FilterEntity
from delpinos.crud.core.domain.entities.filter_field_entity import FilterFieldEntity
from delpinos.crud.core.domain.entities.pagination_entity import PaginationEntity
from delpinos.crud.core.domain.entities.sort_field_entity import SortFieldEntity
from delpinos.crud.core.domain.repositories.base_repository_abstract import (
    BaseRepositoryAbstract,
)


class BaseRepository(BaseRepositoryAbstract, Factory):
    @property
    def entity(self) -> Type[BaseEntity]:
        raise NotImplementedError()

    @property
    def entity_view(self) -> Type[BaseEntity]:
        return self.entity

    @property
    def encoder(self) -> EncoderAbstract:
        raise NotImplementedError()

    def commit(self):
        raise NotImplementedError()

    def rollback(self):
        raise NotImplementedError()

    def build_entity(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity:
        if isinstance(values, BaseEntity):
            return self.entity(**values.model_dump(by_alias=True))
        if isinstance(values, dict):
            return self.entity(**values)
        raise BadRequestException()

    def build_entity_view(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity:
        if isinstance(values, BaseEntity):
            return self.entity_view(**values.model_dump(by_alias=True))
        if isinstance(values, dict):
            return self.entity_view(**values)
        raise BadRequestException()

    def build_filters(
        self,
        values: Dict[str, Any] | BaseEntity,
        view: bool = False,
    ) -> FilterEntity | None:
        if isinstance(values, FilterEntity):
            return values
        if isinstance(values, BaseEntity):
            values = values.dict(by_alias=True)
        if not isinstance(values, dict):
            raise BadRequestException()
        items = []
        entity = self.entity_view if view else self.entity
        fields = entity.get_field_names(by_alias=True)
        for field, value in values.items():
            if field in fields:
                items.append(FilterFieldEntity(field=field, op="==", value=value))
        if items:
            return FilterEntity(**{"and": items})
        return None

    def build_pks_filters(
        self,
        values: Dict[str, Any] | BaseEntity,
        view: bool = False,
    ) -> Dict[str, Any] | None:
        filter_value = {}
        if isinstance(values, BaseEntity):
            values = values.model_dump(by_alias=True)
        entity = self.entity_view if view else self.entity
        for pk in entity.get_pks():
            filter_value[pk] = values[pk]
        return filter_value

    def find(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ) -> List[BaseEntity]:
        raise NotImplementedError()

    def find_view(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ) -> List[BaseEntity]:
        raise NotImplementedError()

    def find_one(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
    ) -> BaseEntity | None:
        raise NotImplementedError()

    def find_one_view(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
    ) -> BaseEntity | None:
        raise NotImplementedError()

    def find_one_from_values(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity | None:
        if not isinstance(values, (dict, BaseEntity)):
            raise BadRequestException()
        filter_entity = self.build_filters(values, view=False)
        if isinstance(filter_entity, FilterEntity):
            return self.find_one(filter_entity)
        return None

    def find_one_view_from_values(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity | None:
        if not isinstance(values, (dict, BaseEntity)):
            raise BadRequestException()
        filter_entity = self.build_filters(values, view=True)
        if isinstance(filter_entity, FilterEntity):
            return self.find_one_view(filter_entity)
        return None

    def count(
        self,
        filter_entity: FilterEntity | None = None,
    ) -> int:
        raise NotImplementedError()

    def count_view(
        self,
        filter_entity: FilterEntity | None = None,
    ) -> int:
        raise NotImplementedError()

    def insert(self, values: BaseEntity) -> BaseEntity:
        raise NotImplementedError()

    def update(self, filter_entity: FilterEntity, values: BaseEntity) -> BaseEntity:
        raise NotImplementedError()

    def delete(self, filter_entity: FilterEntity) -> BaseEntity:
        raise NotImplementedError()
