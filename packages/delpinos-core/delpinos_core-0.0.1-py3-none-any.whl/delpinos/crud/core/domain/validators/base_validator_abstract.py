# -*- coding: utf-8 -*-
# pylint: disable=C0114

from abc import ABC, abstractmethod

from delpinos.crud.core.domain.entities.trigger_entity import TriggerEntity


class BaseValidatorAbstract(ABC):
    @abstractmethod
    def validate_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def validate_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def validate_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()
