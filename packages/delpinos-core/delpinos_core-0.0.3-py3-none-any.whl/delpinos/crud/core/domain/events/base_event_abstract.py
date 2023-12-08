# -*- coding: utf-8 -*-
# pylint: disable=C0114

from abc import ABC, abstractmethod

from delpinos.crud.core.domain.validators.base_validator_abstract import (
    BaseValidatorAbstract,
)
from delpinos.crud.core.domain.integrations.base_integration_abstract import (
    BaseIntegrationAbstract,
)
from delpinos.crud.core.domain.entities.trigger_entity import TriggerEntity


class BaseEventAbstract(ABC):
    @property
    @abstractmethod
    def validator(self) -> BaseValidatorAbstract:
        raise NotImplementedError()

    @property
    @abstractmethod
    def integration(self) -> BaseIntegrationAbstract:
        raise NotImplementedError()

    @abstractmethod
    def validate_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def validate_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def validate_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def integrate_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def integrate_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def integrate_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def before_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def before_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def before_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def after_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def after_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()

    @abstractmethod
    def after_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        raise NotImplementedError()
