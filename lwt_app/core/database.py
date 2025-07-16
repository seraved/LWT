from datetime import datetime

from core.config import settings
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

async_engine = create_async_engine(
    settings.DB_DSN_async,
    future=True,
    pool_size=10,
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo=settings.DEBUG_MODE,
)
async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


class BaseModel(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
