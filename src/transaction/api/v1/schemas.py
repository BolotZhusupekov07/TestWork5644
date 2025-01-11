from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.transaction.enums import TransactionCurrencyEnum


class TransactionCreateIn(BaseModel):
    transaction_id: str = Field(min_length=1, max_length=300)
    user_id: str = Field(min_length=1, max_length=300)
    amount: Decimal = Field(ge=0, decimal_places=2)
    currency: TransactionCurrencyEnum
    timestamp: datetime


class TransactionCreateOut(BaseModel):
    message: str
    task_id: str