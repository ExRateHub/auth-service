from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@dataclass
class BaseSQLAlchemyRepository:
    session_factory: async_sessionmaker[AsyncSession]
