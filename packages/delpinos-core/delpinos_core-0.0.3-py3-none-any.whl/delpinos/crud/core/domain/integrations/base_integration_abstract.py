# -*- coding: utf-8 -*-
# pylint: disable=C0114

from abc import ABC, abstractmethod

from delpinos.crud.core.domain.entities.trigger_entity import TriggerEntity


class BaseIntegrationAbstract(ABC):
    @abstractmethod
    def integrate_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def integrate_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def integrate_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()
