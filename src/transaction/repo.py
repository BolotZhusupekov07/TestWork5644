from decimal import Decimal
from pydantic import TypeAdapter
from sqlalchemy import delete, select
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from src.common.repo import BaseRepo
from src.transaction.exceptions import TransactionNotFoundException
from src.transaction.model import TransactionDB
from src.transaction.schemas import Transaction


class TransactionRepo(BaseRepo):
    model = TransactionDB
    schema = Transaction
    not_found_exception_class = TransactionNotFoundException

    def get_top_transactions_sync(
        self, limit: int = 3, session: Session | None = None
    ) -> list[Transaction]:
        stmt = select(self.model).limit(limit).order_by(
            self.model.amount.desc()
        )
        list_db = self.db_sync.execute_stmt(
            stmt=stmt,
            return_scalar=False,
            session=session
        )
        return TypeAdapter(list[self.schema]).validate_python(  # type: ignore
            list_db.scalars().all()
        )

    def get_transactions_amount_avg_sync(
        self, session: Session | None = None
    ) -> Decimal:
        stmt = select(func.avg(self.model.amount))
        return self.db_sync.execute_stmt(
            stmt=stmt,
            return_scalar=True,
            session=session
        )

    def get_transactions_count_sync(
        self, session: Session | None = None
    ) -> int:
        stmt = select(func.count(self.model.guid))
        return self.db_sync.execute_stmt(
            stmt=stmt,
            return_scalar=True,
            session=session
        )

    async def delete_all(self, session: Session | None = None) -> None:
        stmt = delete(self.model)
        await self.db.execute_stmt(stmt=stmt, session=session)
