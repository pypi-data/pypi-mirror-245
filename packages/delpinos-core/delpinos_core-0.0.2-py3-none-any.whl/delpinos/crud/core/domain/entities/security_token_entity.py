# -*- coding: utf-8 -*-
# pylint: disable=C0114

from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.entities.filter_field_entity import FilterFieldEntity


class SecurityTokenEntity(BaseEntity):
    model_config = ConfigDict(title="SecurityToken")

    access_token: str = Field(
        default=None,
        title="Access Token",
        description="Access Token",
        examples=[FilterFieldEntity(field="name", op="like", value="TE%")],
    )
    escope: str = Field(
        default=None,
        title="Escope",
        description="Escope",
        examples=["default"],
    )
    token_type: str = Field(
        default=None,
        title="Token Type",
        description="Token Type",
        examples=["Bearer"],
    )
    expires_in: int = Field(
        default=None,
        title="Expires in Seconds",
        description="Expires in Seconds",
        examples=[86399],
    )
