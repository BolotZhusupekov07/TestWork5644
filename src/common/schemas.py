from typing import TypeVar

from pydantic import BaseModel, NonNegativeInt

Schema = TypeVar("Schema", bound=BaseModel)


class Pagination(BaseModel):
    skip: NonNegativeInt = 0
    limit: NonNegativeInt = 10
