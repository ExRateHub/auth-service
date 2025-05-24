import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.core.config import Settings


def create_engine_from_settings(settings: Settings) -> AsyncEngine:
    engine = create_async_engine(
        url=settings.database.get_url(),
        poolclass=sa.NullPool,
        future=True,
    )
    return engine
