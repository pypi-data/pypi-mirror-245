# -*- coding: utf-8 -*-
# pylint: disable=C0114

from delpinos.core.factories.factory import Factory
from delpinos.crud.core.domain.entities.trigger_entity import TriggerEntity
from delpinos.crud.core.domain.validators.base_validator_abstract import (
    BaseValidatorAbstract,
)


class BaseValidator(BaseValidatorAbstract, Factory):
    def validate_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def validate_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def validate_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj
