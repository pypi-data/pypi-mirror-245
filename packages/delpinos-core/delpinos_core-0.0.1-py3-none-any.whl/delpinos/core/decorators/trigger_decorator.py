# -*- coding: utf-8 -*-
# pylint: disable=C0114,C0116,E1101,R0911,R0912

import functools
import logging

from types import FunctionType


LOGGER = logging.getLogger(__name__)
DEFAULT_CONTENT_TYPE = 'application/json'


class TriggerDecorator:
    @classmethod
    def before(cls, callback: FunctionType, kwargs_response_key: str = '__response__'):
        def decorator(wrapped):
            def wrapper(*args, **kwargs):
                kwargs[kwargs_response_key] = callback(*args, **kwargs)
                return wrapped(*args, **kwargs)
            return functools.update_wrapper(wrapper, wrapped)
        return decorator

    @classmethod
    def after(cls, callback: FunctionType, kwargs_response_key: str = '__response__'):
        def decorator(wrapped):
            def wrapper(*args, **kwargs):
                kwargs[kwargs_response_key] = wrapped(*args, **kwargs)
                return callback(*args, **kwargs)
            return functools.update_wrapper(wrapper, wrapped)
        return decorator
