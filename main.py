from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.common.configs import logging_conf, settings
from src.common.enums import EnvironmentEnum
from src.common.exceptions import CommonException
from src.common.router import api_router

dictConfig(logging_conf)

openapi_url = (
    f"{settings.api_path}openapi.json"
    if settings.environment != EnvironmentEnum.prod
    else ""
)

app = FastAPI(title=settings.project_name, openapi_url=openapi_url)

app.include_router(api_router)


@app.exception_handler(CommonException)
async def exception_handler(
    request: Request, exc: CommonException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message
            if hasattr(exc, "message")
            else exc.default_message,
            "error_code": exc.error_code,
        },
    )


if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def custom_openapi():
    openapi_schema = get_openapi(
        title=settings.project_name,
        version="0.1.0",
        description=f"{settings.project_name} API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi_schema = custom_openapi()
