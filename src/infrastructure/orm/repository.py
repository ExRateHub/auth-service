from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@dataclass
class BaseSQLAlchemyRepository:
    session_factory: async_sessionmaker[AsyncSession]
