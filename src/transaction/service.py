
import json
from uuid import UUID
from fastapi import Depends

from src.common.cache.repo import CacheRepo
from src.transaction.constants import STATISTICS_CACHE_KEY
from src.transaction.repo import TransactionRepo
from src.transaction.schemas import (
    TransactionCreate,
    TransactionStatistics,
)
from src.transaction.celery_tasks import manage_statistics


class TransactionService:
    def __init__(
        self,
        repo: TransactionRepo = Depends(),
        cache_repo: CacheRepo = Depends()
    ):
        self._repo = repo
        self._cache_repo = cache_repo

    async def create(self, schema: TransactionCreate) -> UUID:
        await self._repo.create(schema.model_dump())
        task = manage_statistics.delay()
        return task.id

    async def delete_all(self) -> None:
        await self._repo.delete_all()
        await self._cache_repo.delete(STATISTICS_CACHE_KEY)

    async def get_statistics(self) -> TransactionStatistics:
        stats = await self._cache_repo.get(STATISTICS_CACHE_KEY)
        if stats:
            return TransactionStatistics(**json.loads(stats))
        return TransactionStatistics()
