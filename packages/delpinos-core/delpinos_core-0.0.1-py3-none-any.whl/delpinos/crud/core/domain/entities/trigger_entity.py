# -*- coding: utf-8 -*-
# pylint: disable=C0114

from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity


class TriggerEntity(BaseEntity):
    model_config = ConfigDict(title="Trigger")

    old_value: BaseEntity | None = Field(
        default=None,
        title="Old Value",
        description="Old Value",
    )
    new_value: BaseEntity | None = Field(
        default=None,
        title="New Value",
        description="New Value",
    )
