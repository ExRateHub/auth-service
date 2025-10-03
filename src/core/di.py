from adaptix import Retort
from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from application.use_cases.register_user import RegisterUserUseCase
from core.config import Settings, get_settings
from infrastructure.database.engine import get_async_engine_from_settings
from infrastructure.database.repository.user import UserRepository
from infrastructure.database.session import get_async_session_factory
from infrastructure.mappers.user import UserMapper
from infrastructure.security.hasher import PasswordHasher


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_settings(self) -> Settings:
        return get_settings()

    @provide(scope=Scope.APP)
    async def provide_user_mapper(self) -> UserMapper:
        return UserMapper()

    @provide(scope=Scope.APP)
    async def provide_async_engine(self, settings: Settings) -> AsyncEngine:
        return get_async_engine_from_settings(settings)

    @provide(scope=Scope.REQUEST)
    async def provide_async_session_factory(self, async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return get_async_session_factory(async_engine)

    @provide(scope=Scope.REQUEST)
    async def provide_user_repository(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
        mapper: UserMapper,
    ) -> UserRepository:
        return UserRepository(session_factory=async_session_factory, mapper=mapper)

    @provide(scope=Scope.APP)
    async def provide_password_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.REQUEST)
    async def provide_user_register_use_case(
        self, user_repository: UserRepository, hasher: PasswordHasher
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(user_repository=user_repository, hasher=hasher)