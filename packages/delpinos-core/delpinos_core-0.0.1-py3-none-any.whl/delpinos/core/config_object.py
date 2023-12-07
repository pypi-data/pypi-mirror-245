# -*- coding: utf-8 -*-
# pylint: disable=C0103

from typing import Any, Dict, List
from delpinos.core.config_object_abstract import ConfigObjectAbstract


class ConfigObject(ConfigObjectAbstract):
    __: Dict[str, Any]

    def __init__(self, **kwargs):
        self.__ = kwargs
        self.setup(**kwargs)
        self.validate(**kwargs)

    def build(self, **kwargs):
        return

    def setup(self, **kwargs):
        return

    def validate(self, **kwargs):
        return

    def values(self) -> Dict[str, Any]:
        return self.__

    def get(
        self,
        key: str,
        default: Any = None,
        response: Dict[str, Any] | None = None,
        **kwargs,
    ) -> Any:
        prefixes = kwargs.get("prefixes") or []
        prefixes = {k: k for k in [*prefixes, ""]}.keys()
        tp = kwargs.get("tp")
        value = default
        set_value = bool(kwargs.get("set_value", True))
        response = response if isinstance(response, dict) else {}
        for prefix in prefixes:
            new_key = f"{prefix}{key}"
            value = self.__getval(new_key)
            if value is not None:
                response["key"] = new_key
                if set_value:
                    self.set(new_key, value, tp=tp)
                return value
        value = default if value is None else value
        if tp:
            self.required_value_isinstance(value, tp, key)
        return value

    def set(
        self,
        key: str,
        value: Any = None,
        **kwargs,
    ):
        self.required_value_isinstance(value, kwargs.get("tp"), str(key))
        self.__[key] = value
        return self

    def find_key(
        self,
        *args,
        **kwargs,
    ) -> str | None:
        response = {}
        default = kwargs.pop("default", None)
        for key in args:
            self.get(
                key,
                None,
                response=response,
                set_value=False,
                **kwargs,
            )
            new_key = response.get("key")
            if new_key:
                return new_key
        return default

    def find_value(
        self,
        *args,
        **kwargs,
    ) -> Any:
        tp = kwargs.pop("tp", None)
        set_value = bool(kwargs.pop("set_value", False))
        default = kwargs.pop("default", None)
        response = {}
        for key in args:
            value = self.get(
                key,
                None,
                response=response,
                set_value=False,
                **kwargs,
            )
            new_key = response.get("key")
            if new_key:
                if set_value:
                    self.set(new_key, value, tp=tp)
                return value
        return default

    def required_value_isinstance(
        self, value: Any, tp: type | None = None, name: str = "value"
    ):
        if tp and isinstance(tp, type) and not isinstance(value, tp):
            raise TypeError(
                f"{name} is required valid instance of {tp.__module__}.{tp.__name__}"
            )

    def __getval(self, key: str, default: Any = None) -> Any:
        if key in self.__:
            return self.__.get(key)
        value = self.__get_from_keys(keys=key.split("."), default=default)
        return value

    def __get_from_keys(self, keys: List[str], default: Any = None) -> Any:
        def check_get(value) -> Any:
            return hasattr(value, "get") and callable(getattr(value, "get"))

        if not keys:
            return default
        value = self.__
        for key in keys:
            if check_get(value):
                try:
                    if not check_get(value):
                        return default
                    value = getattr(value, "get")(key)
                except Exception:
                    return default
        return value
