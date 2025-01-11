from datetime import datetime
from decimal import Decimal
from typing import Optional
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from src.transaction.schemas import Transaction

from main import app
from src.common.auth import verify_api_key
from src.common.db.db_base_class import Base
from src.common.db.db_handler import Database, DatabaseSync
from src.transaction.enums import TransactionCurrencyEnum
from src.transaction.model import TransactionDB
from src.tests.dependency_overrides import verify_key_override


@pytest.fixture(scope="function")
async def database() -> Database:
    db = Database()
    await db.drop_all(Base)
    await db.create_all(Base)
    yield db
    await db.drop_all(Base)
    await db.create_all(Base)


@pytest.fixture(scope="function")
def database_sync() -> DatabaseSync:
    db = DatabaseSync()
    db.drop_all(Base)
    db.create_all(Base)
    yield db
    db.drop_all(Base)
    db.create_all(Base)


@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    app.dependency_overrides[verify_api_key] = verify_key_override

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost/"
    ) as ac:
        yield ac

    app.dependency_overrides = {}


@pytest.fixture(scope="function")
async def transaction(database: Database) -> TransactionDB:
    yield await database.insert_one(
        model=TransactionDB,
        returning=TransactionDB,
        transaction_id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        amount=100,
        currency=TransactionCurrencyEnum.USD,
        timestamp=datetime.now()
    )


@pytest.fixture(scope="function")
def transaction_factory(database_sync: DatabaseSync) -> TransactionDB:
    def _transaction_factory(
        transaction_id: Optional[str] = str(uuid.uuid4()),
        user_id: Optional[str] = str(uuid.uuid4()),
        amount: Optional[Decimal] = 100,
        timestamp: Optional[datetime] = datetime.now()
    ) -> TransactionDB:
        return database_sync.insert_one(
            model=TransactionDB,
            returning=TransactionDB,
            transaction_id=transaction_id,
            user_id=user_id,
            amount=amount,
            currency=TransactionCurrencyEnum.USD,
            timestamp=timestamp
        )

    yield _transaction_factory



@pytest.fixture(scope="function")
def transaction_mock() -> Transaction:
    yield Transaction(
        transaction_id='transaction_id',
        user_id='user_id',
        amount=100,
        currency=TransactionCurrencyEnum.USD,
        timestamp=datetime.now()
    )