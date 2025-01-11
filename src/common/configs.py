import os

from pydantic_settings import BaseSettings

from src.common.enums import EnvironmentEnum


class DBSettings(BaseSettings):
    db_title: str = "adebohost"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_port: int = 5432
    db_host: str = "127.0.0.1"

    pool_pre_ping: bool = False
    pool_size: int = 5
    pool_recycle: int = -1
    max_overflow: int = 10
    echo: bool = False
    expire_on_commit: bool = False
    autocommit: bool = False

    def _get_url(self) -> str:
        return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_title}"

    def get_url(self) -> str:
        url = self._get_url()
        return f"postgresql://{url}"

    def get_async_url(self) -> str:
        url = self._get_url()
        return f"postgresql+asyncpg://{url}"


class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379

    def get_url(self) -> str:
        return f'redis://{self.redis_host}:{self.redis_port}'


class Settings(BaseSettings):
    project_name: str = "Transactions"

    backend_cors_origins: list[str] = ["*"]

    db: DBSettings = DBSettings()

    redis: RedisSettings = RedisSettings()

    environment: EnvironmentEnum = EnvironmentEnum.dev

    domain_name: str = "http://localhost"

    api_path: str = "/api/"
    api_key: str = "api_key"
    api_key_name: str = "Authorization"


def get_settings() -> Settings:
    return Settings()


settings = Settings()


logging_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": (
                "{name} {levelname} {asctime} {module} "
                "{process:d} {thread:d} {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "handlers": [
                "console",
            ],
            "propagate": True,
        }
    },
}
