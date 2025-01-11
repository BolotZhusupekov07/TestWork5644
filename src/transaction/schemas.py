from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.transaction.enums import TransactionCurrencyEnum


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: Decimal
    currency: TransactionCurrencyEnum
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionCreate(BaseModel):
    transaction_id: str
    user_id: str
    amount: Decimal
    currency: TransactionCurrencyEnum
    timestamp: datetime


class TopTransaction(BaseModel):
    transaction_id: int
    amount: Decimal


class TransactionStatistics(BaseModel):
    total_transactions: int = 0
    average_transaction_amount: Decimal = 0
    top_transactions: list[Transaction] = []


class TransactionStatisticsOut(BaseModel):
    total_transactions: int
    average_transaction_amount: Decimal
    top_transactions: list[TopTransaction]
