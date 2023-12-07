# -*- coding: utf-8 -*-
# pylint: disable=C0114

from enum import Enum


class SchemaFieldTypeEnum(Enum):
    VARCHAR = 'VARCHAR'
    INT = 'INT'
    DOUBLE = 'DOUBLE'
    JSON = 'JSON'
    JSONB = 'JSONB'
    STRING = 'STRING'
    TIMESTAMP = 'TIMESTAMP'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
