from src.common.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)


class TransactionAlreadyExistsException(ObjectAlreadyExistsException):
    default_message = "Transaction already exists"
    error_code = "TransactionAlreadyExistsError"


class TransactionNotFoundException(ObjectNotFoundException):
    default_message = "Transaction Not Found"
    error_code = "TransactionNotFound"
