from typing import Optional

from src.common.enums import DBIntegrityViolation


class CommonException(Exception):
    default_message = "Something went wrong"
    error_code = "ErrorCodeNotDefined"
    status_code = 500

    def __init__(
        self,
        message: Optional[str] = None,
        format_fields: Optional[dict] = None,
    ):
        self.message = message if message else self.default_message
        self.format_fields = format_fields


class DBIntegrityError(CommonException):
    default_message = "Database Integrity Error"
    error_code = "DBIntegrityError"

    def __init__(self, message: str, violation: DBIntegrityViolation) -> None:
        self.message = message
        self.violation = violation


class ObjectNotFoundException(CommonException):
    default_message = "Object not found"
    error_code = "ObjectNotFound"
    status_code = 404

    def __init__(self, obj_title: Optional[str] = None) -> None:
        if not obj_title:
            return

        self.message = f"{obj_title} not found"
        self.error_code = f"{obj_title}NotFound"


class ObjectAlreadyExistsException(CommonException):
    default_message = "Object already exists"
    error_code = "ObjectAlreadyExistsError"
    status_code = 400

    def __init__(
        self,
        obj_title: Optional[str] = None,
        field_title: Optional[str] = None,
        unique_value: Optional[str] = None,
    ) -> None:
        if obj_title and field_title and unique_value:
            self.message = f"{obj_title} with {field_title}: {unique_value} already exists."
            self.error_code = f'{obj_title.replace(" ", "")}AlreadyExistsError'
