# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Any, Dict, List

from delpinos.core.functions.dict_function import dicts_merge
from delpinos.core.factories.factory import Factory
from delpinos.core.exceptions.badrequest_exception import BadRequestException
from delpinos.core.exceptions.notfound_exception import NotFoundException
from delpinos.core.exceptions.persistence_exception import PersistenceException
from delpinos.crud.core.domain.events.base_event_abstract import BaseEventAbstract
from delpinos.crud.core.domain.repositories.base_repository_abstract import (
    BaseRepositoryAbstract,
)
from delpinos.crud.core.domain.enums.exceptions.persistence_exceptions_enum import (
    PersistenceExceptionMessageEnum,
)
from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.entities.filter_entity import FilterEntity
from delpinos.crud.core.domain.entities.pagination_entity import PaginationEntity
from delpinos.crud.core.domain.entities.sort_field_entity import SortFieldEntity
from delpinos.crud.core.domain.entities.trigger_entity import TriggerEntity
from delpinos.crud.core.domain.services.base_service_abstract import BaseServiceAbstract


class BaseService(BaseServiceAbstract, Factory):
    @property
    def repository(self) -> BaseRepositoryAbstract:
        raise NotImplementedError()

    @property
    def event(self) -> BaseEventAbstract:
        raise NotImplementedError()

    def commit(self):
        self.repository.commit()

    def rollback(self):
        self.repository.rollback()

    def find(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ) -> List[BaseEntity]:
        return self.repository.find(filter_entity, sorting, pagination)

    def find_view(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ) -> List[BaseEntity]:
        return self.repository.find_view(filter_entity, sorting, pagination)

    def find_one(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
    ) -> BaseEntity | None:
        return self.repository.find_one(filter_entity, sorting)

    def find_one_view(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
    ) -> BaseEntity | None:
        return self.repository.find_one_view(filter_entity, sorting)

    def find_one_from_values(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity | None:
        return self.repository.find_one_from_values(values)

    def find_one_view_from_values(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity | None:
        return self.repository.find_one_view_from_values(values)

    def count(
        self,
        filter_entity: FilterEntity | None = None,
    ) -> int:
        return self.repository.count(filter_entity)

    def count_view(
        self,
        filter_entity: FilterEntity | None = None,
    ) -> int:
        return self.repository.count_view(filter_entity)

    def insert(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity:
        if not isinstance(values, (dict, BaseEntity)):
            raise BadRequestException()
        new_value = self.repository.build_entity(values)
        filter_values = new_value.build_pks_filters()
        if filter_values:
            old_value = self.find_one_from_values(filter_values)
            if old_value:
                raise PersistenceException(
                    PersistenceExceptionMessageEnum.PERSISTENCE_VIOLATION_UNIQUE.value
                )
        trigger_obj = TriggerEntity(
            old_value=None, new_value=self.repository.build_entity(values)
        )
        trigger_obj = self.event.validate_insert(trigger_obj)
        trigger_obj = self.event.integrate_insert(trigger_obj)
        trigger_obj = self.event.before_insert(trigger_obj)
        trigger_obj = self.execute_insert(trigger_obj)
        trigger_obj = self.event.after_insert(trigger_obj)
        return trigger_obj.new_value or new_value

    def update(
        self,
        values: Dict[str, Any] | BaseEntity,
        old_value: BaseEntity | None = None,
    ) -> BaseEntity:
        if not isinstance(values, (dict, BaseEntity)):
            raise BadRequestException()
        if not isinstance(old_value, BaseEntity):
            filter_values = self.repository.build_pks_filters(values)
            if filter_values:
                old_value = self.find_one_from_values(filter_values)
        if not isinstance(old_value, BaseEntity):
            raise NotFoundException()
        new_value = self.repository.build_entity(old_value.merge_values(values))
        trigger_obj = TriggerEntity(old_value=old_value, new_value=new_value)
        trigger_obj = self.event.validate_update(trigger_obj)
        trigger_obj = self.event.integrate_update(trigger_obj)
        trigger_obj = self.event.before_update(trigger_obj)
        trigger_obj = self.execute_update(trigger_obj)
        trigger_obj = self.event.after_update(trigger_obj)
        return trigger_obj.new_value or new_value

    def delete(
        self,
        values: Dict[str, Any] | BaseEntity,
        old_value: BaseEntity | None = None,
    ) -> BaseEntity:
        if not isinstance(values, (dict, BaseEntity)):
            raise BadRequestException()
        if not isinstance(old_value, BaseEntity):
            filter_values = self.repository.build_pks_filters(values)
            if filter_values:
                old_value = self.find_one_from_values(filter_values)
        if not isinstance(old_value, BaseEntity):
            raise NotFoundException()
        trigger_obj = TriggerEntity(old_value=old_value, new_value=None)
        trigger_obj = self.event.validate_delete(trigger_obj)
        trigger_obj = self.event.integrate_delete(trigger_obj)
        trigger_obj = self.event.before_delete(trigger_obj)
        trigger_obj = self.execute_delete(trigger_obj)
        trigger_obj = self.event.after_delete(trigger_obj)
        return trigger_obj.old_value or BaseEntity()

    def execute_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        new_value = trigger_obj.new_value
        if isinstance(new_value, BaseEntity):
            trigger_obj.new_value = self.repository.insert(new_value)
        return trigger_obj

    def execute_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        old_value = trigger_obj.old_value
        new_value = trigger_obj.new_value
        if not isinstance(old_value, (dict, BaseEntity)):
            raise NotFoundException()
        if not isinstance(new_value, (dict, BaseEntity)):
            raise BadRequestException()
        trigger_obj.new_value = self.repository.update(
            self.build_pks_filter(new_value, old_value),
            new_value,
        )
        return trigger_obj

    def execute_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        old_value = trigger_obj.old_value
        if not isinstance(old_value, (dict, BaseEntity)):
            raise NotFoundException()
        old_value_filters = self.repository.build_pks_filters(old_value, view=False)
        filter_entity = self.repository.build_filters(
            old_value_filters or {},
            view=False,
        )
        if not isinstance(filter_entity, FilterEntity):
            raise BadRequestException()
        trigger_obj.new_value = self.repository.delete(filter_entity)
        return trigger_obj

    def build_pks_filter(
        self,
        new_value: BaseEntity,
        old_value: BaseEntity,
    ) -> FilterEntity:
        if not isinstance(old_value, (dict, BaseEntity)):
            raise NotFoundException()
        if not isinstance(new_value, (dict, BaseEntity)):
            raise BadRequestException()
        old_value_filters = self.repository.build_pks_filters(old_value, view=False)
        new_value_filters = self.repository.build_pks_filters(new_value, view=False)
        filter_entity = self.repository.build_filters(
            dicts_merge(new_value_filters, old_value_filters),
            view=False,
        )
        if not isinstance(filter_entity, FilterEntity):
            raise BadRequestException()
        return filter_entity
