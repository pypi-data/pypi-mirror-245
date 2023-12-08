# -*- coding: utf-8 -*-
# pylint: disable=C0114

from datetime import datetime
from uuid import uuid4
from pydantic import Field, ConfigDict

from delpinos.crud.core.domain.entities import BaseEntity


class ApiIntegrationEntity(BaseEntity):
    model_config = ConfigDict(title="ApiIntegration")

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        title="ApiIntegration Identification",
        description="ApiIntegration Identification=",
        examples=[str(uuid4())],
        min_length=1,
    )
    app_id: str = Field(
        ...,
        alias="app_id",
        title="App Identification",
        description="App Identification",
        examples=[str(uuid4())],
        min_length=1,
    )
    type: str = Field(
        ...,
        title="ApiIntegration Type Identification",
        description="ApiIntegration Type Identification",
        examples=["test"],
        min_length=1,
    )
    status: int = Field(
        default=0,
        title="ApiIntegration HTTP Response Code",
        description="ApiIntegration HTTP Response Code",
        examples=["200"],
    )
    url: str = Field(
        ...,
        title="ApiIntegration Url",
        description="ApiIntegration Url",
        examples=["https://www.imei.info/"],
        min_length=1,
    )
    endpoint: str = Field(
        default="/",
        title="ApiIntegration Endpoint",
        description="ApiIntegration Endpoint",
        examples=["/api/checkimei/"],
        min_length=1,
    )
    method: str = Field(
        default="POST",
        title="ApiIntegration Method",
        description="ApiIntegration Method",
        examples=["POST"],
        min_length=1,
    )
    exception: str = Field(
        default=None,
        title="ApiIntegration response Exception",
        description="ApiIntegration response Exception",
        examples=[""],
    )
    config: dict = Field(
        default={},
        title="ApiIntegration Config",
        description="ApiIntegration Config",
        examples=[{}],
    )
    request: dict = Field(
        default={},
        title="ApiIntegration Request",
        description="ApiIntegration Request",
        examples=[{}],
    )
    response: dict = Field(
        default={},
        title="ApiIntegration Response",
        description="ApiIntegration Response",
        examples=[{}],
    )
    revision: int = Field(
        default=0,
        title="ApiIntegration System Revision version",
        description="ApiIntegration System Revision version",
        examples=["1532"],
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        title="ApiIntegration System Created at Timestamp",
        description="ApiIntegration System Created at Timestamp",
        examples=["2023-01-01 00:00:00"],
    )
    updated_at: datetime | None = Field(
        default=None,
        title="ApiIntegration System Updated at Timestamp",
        description="ApiIntegration System Updated at Timestamp",
        examples=["2023-01-01 00:00:00"],
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        title="ApiIntegration System Created/Updated at Timestamp",
        description="ApiIntegration System Created/Updated at Timestamp",
        examples=["2023-01-01 00:00:00"],
    )
