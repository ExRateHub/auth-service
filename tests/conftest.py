import os
from typing import Generator, Any, AsyncGenerator
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


from core.config import Settings, get_settings, PROJECT_DIR
from infrastructure.database.engine import create_engine_from_settings
from infrastructure.database.mapper import get_mapper
from infrastructure.database.repository.user import UserRepository
from infrastructure.database.session import get_async_session_factory


@pytest.fixture(scope="session")
def settings() -> Generator[Settings, None, None]:
    os.environ["ENV_FILE"] = str(PROJECT_DIR / ".env.test")
    yield get_settings()
    os.environ.pop("ENV_FILE")

@pytest.fixture(scope="session")
def alembic_config(settings: Settings) -> Config:
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", settings.database.get_url())
    return cfg

# @pytest.fixture(scope="session")
# def setup_database(alembic_config: Config) -> Generator:
#     command.upgrade(alembic_config, "head")
#     yield
#     command.downgrade(alembic_config, "base")

@pytest.fixture(scope="session")
async def engine(alembic_config: Config, settings: Settings) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_engine_from_settings(settings)

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: command.upgrade(alembic_config, "head"))

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: command.downgrade(alembic_config, "base"))

    await engine.dispose()

@pytest.fixture()
async def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return get_async_session_factory(engine)

@pytest.fixture(scope="function")
async def user_repository(session_factory: async_sessionmaker[AsyncSession]):
    return UserRepository(session_factory, get_mapper())
