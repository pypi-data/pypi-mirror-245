# -*- coding: utf-8 -*-
# pylint: disable=C0114

from delpinos.api.core.exceptions.api_exception import ApiException

DEFAULT_MESSAGE = "exception.persistence"


class PersistenceException(ApiException):
    def default_message(self):
        return DEFAULT_MESSAGE
