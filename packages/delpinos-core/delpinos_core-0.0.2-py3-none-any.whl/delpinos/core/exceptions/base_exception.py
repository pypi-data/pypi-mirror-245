# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Any, Dict, List


DEFAULT_MESSAGE = "exception.base"


class BaseException(Exception):
    _properties: Dict[str, Any]
    _message: str
    _messages: List[str]

    def __init__(self, *args, **kwargs):
        self._properties = kwargs
        self._messages = self.build_messages(*args)
        self._message = self._messages[0]
        super().__init__(self._message)

    @property
    def properties(self):
        return self._properties

    @property
    def message(self):
        return self._message

    @property
    def messages(self) -> List:
        return self._messages

    def default_message(self):
        return DEFAULT_MESSAGE

    def build_messages(self, *args):
        messages = []
        for msg in args:
            if isinstance(msg, str):
                messages.append(msg)
            elif isinstance(msg, list):
                messages.append([msg for msg in self.build_messages(*msg)])
        messages = list(set(messages))
        if not messages:
            messages.append(self.default_message())
        return messages

    def find_messages(self, *args) -> List:
        def filter_messages(message: str):
            for msg in args:
                if msg == message:
                    return True
            return False

        return list(filter(filter_messages, self.messages))
