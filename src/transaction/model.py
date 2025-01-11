from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db.db_base_class import AuditableBase
from src.transaction.enums import TransactionCurrencyEnum


class TransactionDB(AuditableBase):
    __tablename__ = "transaction"

    transaction_id: Mapped[str] = mapped_column(
        String(300), nullable=False, unique=True
    )
    user_id: Mapped[str] = mapped_column(
        String(300), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    currency: Mapped[TransactionCurrencyEnum] = mapped_column(
        ENUM(
            TransactionCurrencyEnum,
            name="transaction_currency_enum",
            create_type=False,
        ),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)