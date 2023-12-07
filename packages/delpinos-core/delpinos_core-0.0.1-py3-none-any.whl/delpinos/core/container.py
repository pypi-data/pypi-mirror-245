# -*- coding: utf-8 -*-
# pylint: disable=C0103

from typing import Type
from delpinos.core.config_object import ConfigObject
from delpinos.core.config_object_abstract import ConfigObjectAbstract

from delpinos.core.container_abstract import ContainerAbstract


class Container(ContainerAbstract, ConfigObject):
    config: ConfigObjectAbstract
    variables: ConfigObjectAbstract

    def __init__(self, **kwargs):
        config = (
            ConfigObject(**kwargs).get(self.config_key) if self.config_key else kwargs
        )
        config = config if isinstance(config, dict) else {}
        self.config = self.config_class(**config)
        self.variables = self.variables_class()
        super().__init__(**kwargs)

    @property
    def config_key(self) -> str:
        return ""

    @property
    def config_class(self) -> Type[ConfigObjectAbstract]:
        return ConfigObject

    @property
    def variables_class(self) -> Type[ConfigObjectAbstract]:
        return ConfigObject
