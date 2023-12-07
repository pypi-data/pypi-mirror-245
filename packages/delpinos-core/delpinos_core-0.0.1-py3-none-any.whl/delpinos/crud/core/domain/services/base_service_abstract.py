# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Any, Dict, List
from abc import ABC, abstractmethod

from delpinos.crud.core.domain.events.base_event_abstract import BaseEventAbstract
from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.entities.filter_entity import FilterEntity
from delpinos.crud.core.domain.entities.pagination_entity import PaginationEntity
from delpinos.crud.core.domain.entities.sort_field_entity import SortFieldEntity
from delpinos.crud.core.domain.entities.trigger_entity import TriggerEntity
from delpinos.crud.core.domain.repositories.base_repository_abstract import (
    BaseRepositoryAbstract,
)


class BaseServiceAbstract(ABC):
    @property
    @abstractmethod
    def repository(self) -> BaseRepositoryAbstract:
        raise NotImplementedError()

    @property
    @abstractmethod
    def event(self) -> BaseEventAbstract:
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
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
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity | None:
        raise NotImplementedError()

    @abstractmethod
    def find_one_view_from_values(
        self,
        values: Dict[str, Any] | BaseEntity,
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
    def insert(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    def update(
        self,
        values: Dict[str, Any] | BaseEntity,
        old_value: BaseEntity | None = None,
    ) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    def delete(
        self,
        values: Dict[str, Any] | BaseEntity,
        old_value: BaseEntity | None = None,
    ) -> BaseEntity:
        raise NotImplementedError()

    @abstractmethod
    def execute_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def execute_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def execute_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def build_pks_filter(
        self,
        new_value: BaseEntity,
        old_value: BaseEntity,
    ) -> FilterEntity:
        raise NotImplementedError()
