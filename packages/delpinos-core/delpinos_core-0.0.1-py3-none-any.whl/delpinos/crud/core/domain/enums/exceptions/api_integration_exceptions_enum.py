# -*- coding: utf-8 -*-
# pylint: disable=C0114

from enum import Enum


class ApiIntegrationExceptionMessageEnum(Enum):
    INVALID_API_INTEGRATION = "invalid.api_integration"
    INVALID_API_INTEGRATION_CALLBACK = "invalid.api_integration.callback"
