from fastapi import APIRouter

from src.transaction.router import api_router as transaction_api_router

api_router = APIRouter()

api_router.include_router(transaction_api_router)
