from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from application.ports.token_repository import TokenRepositoryProtocol
from application.use_cases.login_user import LoginUserUseCase
from application.use_cases.logout_user import LogoutUserUseCase
from application.use_cases.register_user import RegisterUserUseCase
from core.config import Settings, get_settings
from infrastructure.orm.engine import get_async_engine_from_settings
from infrastructure.persistence.mappers.auth_token import AuthTokenMapper
from infrastructure.persistence.repository.auth_token import AuthTokenRepository
from infrastructure.persistence.repository.user import UserRepository
from infrastructure.orm.session import get_async_session_factory
from infrastructure.persistence.mappers.user import UserMapper
from infrastructure.security.auth_token_service import AuthTokenService
from infrastructure.security.hasher import PasswordHasher, TokenHasher


class SettingsProvider(Provider):

    @provide(scope=Scope.APP)
    async def provide_settings(self) -> Settings:
        return get_settings()

class PersistenceProvider(Provider):

    @provide(scope=Scope.APP)
    async def provide_async_engine(self, settings: Settings) -> AsyncEngine:
        return get_async_engine_from_settings(settings)

    @provide(scope=Scope.REQUEST)
    async def provide_async_session_factory(self, async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return get_async_session_factory(async_engine)

class RepositoryProvider(Provider):

    @provide(scope=Scope.APP)
    async def provide_user_mapper(self) -> UserMapper:
        return UserMapper()

    @provide(scope=Scope.APP)
    async def provide_auth_token_mapper(self) -> AuthTokenMapper:
        return AuthTokenMapper()

    @provide(scope=Scope.REQUEST)
    async def provide_user_repository(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
        mapper: UserMapper,
    ) -> UserRepository:
        return UserRepository(session_factory=async_session_factory, mapper=mapper)

    @provide(scope=Scope.REQUEST)
    async def provide_auth_token_repository(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
        mapper: AuthTokenMapper,
    ) -> TokenRepositoryProtocol:
        return AuthTokenRepository(session_factory=async_session_factory, mapper=mapper)

class SecurityProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_password_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.APP)
    async def provide_token_hasher(self) -> TokenHasher:
        return TokenHasher()

    @provide(scope=Scope.APP)
    async def provide_auth_token_service(self, hasher: TokenHasher, ) -> AuthTokenService:
        return AuthTokenService(hasher=hasher)


class UseCasesProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def provide_user_register_use_case(
        self,
        user_repository: UserRepository,
        hasher: PasswordHasher,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(user_repository=user_repository, hasher=hasher)

    @provide(scope=Scope.REQUEST)
    async def provide_user_login_use_case(
        self,
        hasher: PasswordHasher,
        token_service: AuthTokenService,
        token_repository: TokenRepositoryProtocol,
        user_repository: UserRepository,

    ) -> LoginUserUseCase:
        use_case = LoginUserUseCase(
            hasher=hasher,
            token_service=token_service,
            token_repository=token_repository,
            user_repository=user_repository,
        )
        return use_case

    @provide(scope=Scope.REQUEST)
    async def provide_logout_user_use_case(
        self,
        hasher: TokenHasher,
        token_service: AuthTokenService,
        token_repository: TokenRepositoryProtocol,
    ) -> LogoutUserUseCase:
        use_case = LogoutUserUseCase(
            hasher=hasher,
            token_service=token_service,
            token_repository=token_repository,
        )
        return use_case
