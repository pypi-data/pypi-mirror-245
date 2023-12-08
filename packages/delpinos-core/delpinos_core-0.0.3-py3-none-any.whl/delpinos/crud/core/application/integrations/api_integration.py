# -*- coding: utf-8 -*-
# pylint: disable=C0114

import json
from typing import Callable

import requests

from delpinos.core.exceptions.api_integration_exception import (
    ApiIntegrationException,
)
from delpinos.core.exceptions.validate_exception import ValidateException
from delpinos.core.exceptions.notfound_exception import NotFoundException
from delpinos.core.exceptions.badrequest_exception import BadRequestException
from delpinos.core.exceptions.unauthorized_exception import UnauthorizedException
from delpinos.core.exceptions.forbidden_exception import ForbiddenException
from delpinos.core.exceptions.persistence_exception import PersistenceException
from delpinos.crud.core.domain.entities.api_integration_entity import (
    ApiIntegrationEntity,
)
from delpinos.crud.core.domain.enums.exceptions.api_integration_exceptions_enum import (
    ApiIntegrationExceptionMessageEnum,
)
from delpinos.crud.core.domain.integrations.api_integration_abstract import (
    ApiIntegrationAbstract,
)
from delpinos.crud.core.application.integrations.base_integration import BaseIntegration


class ApiIntegration(ApiIntegrationAbstract, BaseIntegration):
    def execute_api(
        self,
        request: Callable[[], requests.Response],
        api_integration: ApiIntegrationEntity,
    ) -> ApiIntegrationEntity:
        exception = None
        try:
            api_integration.exception = ""
            if not isinstance(request, Callable):
                raise ValidateException(
                    ApiIntegrationExceptionMessageEnum.INVALID_API_INTEGRATION_CALLBACK.value
                )
            if not isinstance(api_integration, ApiIntegrationEntity):
                raise ValidateException(
                    ApiIntegrationExceptionMessageEnum.INVALID_API_INTEGRATION.value
                )
            response = request()
            api_integration.status = response.status_code
            try:
                api_integration.response = response.json()
            except Exception:
                api_integration.response = dict(text=response.text)
            if api_integration.status == 0 or api_integration.status >= 400:
                exception = ApiIntegrationException(
                    json.dumps(api_integration.response, default=str)
                )
        except ApiIntegrationException as err:
            exception = err
            api_integration.status = 422
            api_integration.exception = str(err)
        except NotFoundException as err:
            exception = err
            api_integration.status = 404
            api_integration.exception = str(err)
        except BadRequestException as err:
            exception = err
            api_integration.status = 400
            api_integration.exception = str(err)
        except PersistenceException as err:
            exception = err
            api_integration.status = 409
            api_integration.exception = str(err)
        except UnauthorizedException as err:
            exception = err
            api_integration.status = 401
            api_integration.exception = str(err)
        except ForbiddenException as err:
            exception = err
            api_integration.status = 403
            api_integration.exception = str(err)
        except ValidateException as err:
            exception = err
            api_integration.status = 422
            api_integration.exception = str(err)
        except Exception as err:
            exception = err
            api_integration.status = 0
            api_integration.exception = str(err)
        if exception:
            raise exception
        return api_integration
