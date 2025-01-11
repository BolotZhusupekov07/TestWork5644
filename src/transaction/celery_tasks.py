from src.common.cache.repo import CacheRepo
from src.common.celery import app
from src.common.db.db_handler import DatabaseSync
from src.transaction.constants import STATISTICS_CACHE_KEY
from src.transaction.repo import TransactionRepo
from src.transaction.schemas import TransactionStatistics


@app.task
def manage_statistics():
    db_sync = DatabaseSync()
    repo = TransactionRepo(db=None, db_sync=db_sync)

    with db_sync.session_maker() as session, session.begin():
        total_transactions = repo.get_transactions_count_sync(session)
        avg_transaction_amount = repo.get_transactions_amount_avg_sync(session)
        top_transactions = repo.get_top_transactions_sync(session=session)

    statistics = TransactionStatistics(
        total_transactions=total_transactions,
        average_transaction_amount=avg_transaction_amount,
        top_transactions=top_transactions
    )

    cache_repo = CacheRepo()
    cache_repo.set_sync(STATISTICS_CACHE_KEY, statistics.model_dump_json())
