# -*- coding: utf-8 -*-
# pylint: disable=C0114

from enum import Enum


class PersistenceExceptionMessageEnum(Enum):
    PERSISTENCE_VIOLATION = "persistence.violation"
    PERSISTENCE_VIOLATION_UNIQUE = "persistence.violation.unique"
    PERSISTENCE_VIOLATION_CHECK = "persistence.violation.check"
    PERSISTENCE_VIOLATION_FOREIGN_KEY = "persistence.violation.foreign_key"
    PERSISTENCE_VIOLATION_NOT_NULL = "persistence.violationn.not_null"
