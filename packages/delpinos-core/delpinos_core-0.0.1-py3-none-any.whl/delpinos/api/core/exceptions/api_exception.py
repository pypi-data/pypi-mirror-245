# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import List


DEFAULT_MESSAGE = "exception.api"


class ApiException(Exception):
    __message: str
    __messages: List[str]

    def __init__(self, *args):
        self.__messages = self.build_messages(*args)
        self.__message = self.__messages[0]
        super().__init__(self.__message)

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

    def default_message(self):
        return DEFAULT_MESSAGE

    @property
    def message(self):
        return self.__message

    @property
    def messages(self) -> List:
        return self.__messages

    def find_messages(self, *args) -> List:
        def filter_messages(message: str):
            for msg in args:
                if msg == message:
                    return True
            return False

        return list(filter(filter_messages, self.messages))
