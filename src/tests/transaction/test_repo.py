
from datetime import datetime
import uuid
import pytest
from src.common.exceptions import ObjectAlreadyExistsException
from src.transaction.enums import TransactionCurrencyEnum
from src.transaction.repo import TransactionRepo
from src.transaction.schemas import TransactionCreate


def test_get_top_transactions(
    database_sync, transaction_factory
):
    transaction_factory(transaction_id=str(uuid.uuid4()), amount=100)
    transaction_2 = transaction_factory(transaction_id=str(uuid.uuid4()),amount=200)
    transaction_3 = transaction_factory(transaction_id=str(uuid.uuid4()),amount=300)
    transaction_4 = transaction_factory(transaction_id=str(uuid.uuid4()),amount=400)

    repo = TransactionRepo(db=None, db_sync=database_sync)

    with database_sync.session_maker() as session:
        result = repo.get_top_transactions_sync(session=session)

    assert len(result) == 3
    assert result[0].transaction_id == transaction_4.transaction_id
    assert result[1].transaction_id == transaction_3.transaction_id
    assert result[2].transaction_id == transaction_2.transaction_id


def test_get_transactions_count(
    database_sync, transaction_factory
):
    transaction_factory(transaction_id=str(uuid.uuid4()), amount=100)
    transaction_factory(transaction_id=str(uuid.uuid4()),amount=200)
    transaction_factory(transaction_id=str(uuid.uuid4()),amount=300)
    transaction_factory(transaction_id=str(uuid.uuid4()),amount=400)

    repo = TransactionRepo(db=None, db_sync=database_sync)

    with database_sync.session_maker() as session:
        result = repo.get_transactions_count_sync(session=session)

    assert result == 4


def test_get_transactions_average(
    database_sync, transaction_factory
):
    transaction_factory(transaction_id=str(uuid.uuid4()), amount=100)
    transaction_factory(transaction_id=str(uuid.uuid4()),amount=200)
    transaction_factory(transaction_id=str(uuid.uuid4()),amount=300)
    transaction_factory(transaction_id=str(uuid.uuid4()),amount=400)

    repo = TransactionRepo(db=None, db_sync=database_sync)

    with database_sync.session_maker() as session:
        result = repo.get_transactions_amount_avg_sync(session=session)

    assert result == 250


@pytest.mark.asyncio
async def test_create__success(database):
    repo = TransactionRepo(db=database, db_sync=None)

    schema = TransactionCreate(
        transaction_id="1",
        user_id="2",
        currency=TransactionCurrencyEnum.USD,
        amount=100,
        timestamp=datetime.now()
    )
    result = await repo.create(schema.model_dump())

    assert result.transaction_id == schema.transaction_id
    assert result.user_id == schema.user_id
    assert result.currency == schema.currency
    assert result.amount == schema.amount


@pytest.mark.asyncio
async def test_create__raises_error__when_already_exists_by_transaction_id(
    database, transaction
):
    repo = TransactionRepo(db=database, db_sync=None)

    schema = TransactionCreate(
        transaction_id=transaction.transaction_id,
        user_id="2",
        currency=TransactionCurrencyEnum.USD,
        amount=100,
        timestamp=datetime.now()
    )
    with pytest.raises(ObjectAlreadyExistsException):
        await repo.create(schema.model_dump())
