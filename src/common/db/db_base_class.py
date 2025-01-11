import uuid
from datetime import datetime, timezone
from typing import TypeVar
from uuid import UUID

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class IdentifiableBase(Base):
    __abstract__ = True

    guid: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


IdentifiableDB = TypeVar("IdentifiableDB", bound=IdentifiableBase)


class AuditableBase(IdentifiableBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=func.now(),
    )

AuditableDB = TypeVar("AuditableDB", bound=AuditableBase)
