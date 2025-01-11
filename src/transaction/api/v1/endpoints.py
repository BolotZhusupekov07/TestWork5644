from fastapi import APIRouter, Depends, status

from src.common.auth import verify_api_key
from src.transaction.api.v1.schemas import (
    TransactionCreateIn,
    TransactionCreateOut,
)
from src.transaction.schemas import (
    TransactionCreate,
    TransactionStatisticsOut,
)
from src.transaction.service import TransactionService

router = APIRouter()


@router.post(
    "/api/v1/transactions/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a transaction",
    response_model=TransactionCreateOut,
    dependencies=[Depends(verify_api_key)]
)
async def create(
    schema_in: TransactionCreateIn, service: TransactionService = Depends()
):
    schema = TransactionCreate(**schema_in.model_dump())
    task_id = await service.create(schema)
    return TransactionCreateOut(
        message= "Transaction received",
        task_id=str(task_id)
    )

@router.delete(
    "/api/v1/transactions/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete all transactions",
    dependencies=[Depends(verify_api_key)]
)
async def delete(service: TransactionService = Depends()):
    await service.delete_all()


@router.get(
    "/api/v1/statistics/",
    status_code=status.HTTP_200_OK,
    summary="Get transaction statistics",
    response_model=TransactionStatisticsOut,
    dependencies=[Depends(verify_api_key)]
)
async def get_stats(service: TransactionService = Depends()):
    return await service.get_statistics()
