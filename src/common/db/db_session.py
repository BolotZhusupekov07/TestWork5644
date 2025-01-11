import functools
import json
import logging
from datetime import datetime

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, Session
from src.common.configs import Settings

logger = logging.getLogger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def get_async_db_engine(settings: Settings) -> AsyncEngine:
    db = settings.db
    return create_async_engine(
        url=db.get_async_url(),
        pool_pre_ping=db.pool_pre_ping,
        pool_size=db.pool_size,
        pool_recycle=db.pool_recycle,
        max_overflow=db.max_overflow,
        echo=db.echo,
        json_serializer=functools.partial(json.dumps, cls=DateTimeEncoder),
    )


def get_db_engine(settings: Settings) -> Engine:
    db = settings.db
    return create_engine(
        url=db.get_url(),
        pool_pre_ping=db.pool_pre_ping,
        pool_size=db.pool_size,
        pool_recycle=db.pool_recycle,
        max_overflow=db.max_overflow,
        echo=db.echo,
        json_serializer=functools.partial(json.dumps, cls=DateTimeEncoder),
    )


def get_async_session_maker(
    db_engine: AsyncEngine, settings: Settings
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=db_engine,
        expire_on_commit=settings.db.expire_on_commit,
    )


def get_session_maker(
    db_engine: Engine, settings: Settings,
) -> sessionmaker[Session]:
    return sessionmaker(
        bind=db_engine,
        expire_on_commit=settings.db.expire_on_commit,
    )
