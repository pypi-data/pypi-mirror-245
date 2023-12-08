# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Any, Callable, Dict, List
from types import FunctionType
from pydantic import BaseModel, ValidationError

from delpinos.core.exceptions.validate_exception import ValidateException
from delpinos.core.functions.dict_function import dicts_merge
from pydantic_core import ErrorDetails


class BaseEntity(BaseModel):
    def __init__(self, **kwargs):
        _super = super()

        def callback():
            _super.__init__(**kwargs)

        self.execute_create(callback)

    def update(
        self, values: Dict[str, Any] | "BaseEntity", by_alias=False
    ) -> "BaseEntity":
        if not isinstance(values, (dict, BaseEntity)):
            return self
        new_values = self.merge_values(values, by_alias=by_alias)

        def callback():
            for k, v in (
                self.model_validate(new_values)
                .model_dump(exclude_defaults=True)
                .items()
            ):
                setattr(self, k, v)
            return self

        return self.execute_create(callback)

    def merge_values(
        self, values: Dict[str, Any] | "BaseEntity", by_alias=False
    ) -> Dict[str, Any]:
        if isinstance(values, BaseEntity):
            values = values.model_dump(by_alias=by_alias)
        if not isinstance(values, dict):
            return self.model_dump(by_alias=False)
        new_values = {}
        for key, value in self.model_fields.items():
            old_value = getattr(self, key)
            alias = value.alias or key
            new_value = values.get(alias, values.get(key, old_value))
            if isinstance(new_value, dict) and isinstance(old_value, dict):
                new_value = dicts_merge(old_value, new_value)
            new_values[key] = new_value
        return new_values

    def build_pks_filters(self) -> Dict[str, Any] | None:
        filter_value = {}
        for pk in self.get_pks():
            filter_value[pk] = getattr(self, pk) if hasattr(self, pk) else None
        return filter_value

    @classmethod
    def get_pks(cls) -> List[str]:
        return ["id"]

    @classmethod
    def get_field_names(cls, by_alias=False) -> list[str]:
        field_names = []
        for key, value in cls.model_fields.items():
            field_names.append(value.alias or key)
        return field_names

    @classmethod
    def build_exception_type(cls, error: ErrorDetails):
        if error["type"] == "value_error.any_str.min_length":
            return "min_length"
        if error["type"] == "value_error.missing" and "required" in error["msg"]:
            return "required"

    @classmethod
    def build_exception_name(cls, entity_name: str | None = None):
        return (
            str(cls.model_config.get("title") if not entity_name else entity_name)
            .strip()
            .lower()
        )

    @classmethod
    def build_exception_message(
        cls,
        entity_name: str | None = None,
        field: str | None = None,
        error_type: str | None = None,
    ):
        msg = "invalid"
        entity_name = cls.build_exception_name(entity_name)
        if entity_name:
            msg += "." + entity_name
        if field:
            msg += "." + field
        if error_type:
            msg += "." + error_type
        return msg

    @classmethod
    def execute_create(cls, callback: Callable, entity_name=None):
        if not isinstance(callback, FunctionType):
            raise ValidateException("invalid.entity.builder")
        errors = []
        try:
            return callback()
        except ValidationError as exception:
            for error in exception.errors():
                for field in error["loc"]:
                    errors.append(
                        cls.build_exception_message(
                            entity_name=entity_name,
                            field=str(field or ""),
                            error_type=cls.build_exception_type(error),
                        )
                    )
        raise ValidateException(*errors)

    @classmethod
    def build_entity(
        cls, values: Dict[str, Any], pydantic_class: type, entity_name=None
    ):
        if not issubclass(pydantic_class, BaseEntity):
            raise ValidateException("invalid.class")

        def callback():
            return pydantic_class(**values)

        return cls.execute_create(callback=callback, entity_name=entity_name)
