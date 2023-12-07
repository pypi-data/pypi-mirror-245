# -*- coding: utf-8 -*-
# pylint: disable=C0114

from delpinos.core.exceptions.base_exception import BaseException

DEFAULT_MESSAGE = "exception.not_found"


class NotFoundException(BaseException):
    def default_message(self):
        return DEFAULT_MESSAGE
