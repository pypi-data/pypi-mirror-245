# -*- coding: utf-8 -*-
# pylint: disable=C0114,C0103,W0622

from typing import Any, Dict, List, Type
from abc import ABC, abstractmethod
from delpinos.core.encoders import EncoderAbstract
from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.entities.filter_entity import FilterEntity
from delpinos.crud.core.domain.entities.pagination_entity import PaginationEntity
from delpinos.crud.core.domain.entities.sort_field_entity import SortFieldEntity


class BaseRepositoryAbstract(ABC):
    @property
    @abstractmethod
    def entity(self) -> Type[BaseEntity]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def entity_view(self) -> Type[BaseEntity]:
        raise NotImplementedError()

    @property
    def encoder(self) -> EncoderAbstract:
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    def build_entity(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    def build_entity_view(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    def build_filters(
        self,
        values: Dict[str, Any] | BaseEntity,
        view: bool = False,
    ) -> FilterEntity | None:
        raise NotImplementedError()

    def build_pks_filters(
        self,
        values: Dict[str, Any] | BaseEntity,
        view: bool = False,
    ) -> Dict[str, Any] | None:
        raise NotImplementedError()

    @abstractmethod
    def find(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ) -> List[BaseEntity]:
        raise NotImplementedError()

    @abstractmethod
    def find_view(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ) -> List[BaseEntity]:
        raise NotImplementedError()

    @abstractmethod
    def find_one(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
    ) -> BaseEntity | None:
        raise NotImplementedError()

    @abstractmethod
    def find_one_view(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
    ) -> BaseEntity | None:
        raise NotImplementedError()

    @abstractmethod
    def find_one_from_values(
        self, values: Dict[str, Any] | BaseEntity
    ) -> BaseEntity | None:
        raise NotImplementedError()

    @abstractmethod
    def find_one_view_from_values(
        self, values: Dict[str, Any] | BaseEntity
    ) -> BaseEntity | None:
        raise NotImplementedError()

    @abstractmethod
    def count(
        self,
        filter_entity: FilterEntity | None = None,
    ) -> int:
        raise NotImplementedError()

    @abstractmethod
    def count_view(
        self,
        filter_entity: FilterEntity | None = None,
    ) -> int:
        raise NotImplementedError()

    @abstractmethod
    def insert(self, values: BaseEntity) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    def update(
        self,
        filter_entity: FilterEntity,
        values: BaseEntity,
    ) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, filter_entity: FilterEntity) -> BaseEntity:
        raise NotImplementedError()
