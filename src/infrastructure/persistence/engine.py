import sqlalchemy as sa
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from core.config import Settings


def get_async_engine_from_settings(settings: Settings) -> AsyncEngine:
    engine = create_async_engine(
        url=settings.database.get_url(),
        poolclass=sa.NullPool,
        future=True,
    )
    return engine
