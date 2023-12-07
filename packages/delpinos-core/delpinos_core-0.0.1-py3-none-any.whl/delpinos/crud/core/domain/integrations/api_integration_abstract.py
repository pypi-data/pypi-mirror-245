# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Callable

import requests
from delpinos.crud.core.domain.entities.api_integration_entity import (
    ApiIntegrationEntity,
)
from delpinos.crud.core.domain.integrations.base_integration_abstract import (
    abstractmethod,
    BaseIntegrationAbstract,
)


class ApiIntegrationAbstract(BaseIntegrationAbstract):
    @abstractmethod
    def execute_api(
        self,
        request: Callable[[], requests.Response],
        api_integration: ApiIntegrationEntity,
    ) -> ApiIntegrationEntity:
        raise NotImplementedError()
