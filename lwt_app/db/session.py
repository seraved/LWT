from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from core.config import settings

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
    class_=AsyncSession
)
