# -*- coding: utf-8 -*-
# pylint: disable=C0114

from delpinos.core.exceptions.base_exception import BaseException

DEFAULT_MESSAGE = "exception.validate"


class ValidateException(BaseException):
    def default_message(self):
        return DEFAULT_MESSAGE
