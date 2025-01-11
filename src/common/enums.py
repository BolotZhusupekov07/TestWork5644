from enum import StrEnum


class EnvironmentEnum(StrEnum):
    dev = "dev"
    staging = "staging"
    prod = "prod"


class DBIntegrityViolation(StrEnum):
    INTEGRITY_CONSTRAINT = "23000"
    RESTRICT = "23001"
    NOT_NULL = "23502"
    FOREIGN_KEY = "23503"
    UNIQUE = "23505"
    CHECK = "23514"
    EXCLUSION = "23P01"
