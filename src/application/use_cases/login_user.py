import dataclasses
import typing

from application.ports.hasher import HasherProtocol
from application.ports.token_repository import TokenRepositoryProtocol
from application.ports.token_service import TokenServiceProtocol
from application.use_cases.base import BaseUseCase, BaseCommand
from domain.entities.auth_token import AuthToken
from domain.entities.user import User
from domain.errors import InvalidCredentialsError
from domain.value_objects.token_key import TokenKey
from domain.value_objects.ttl import TTL
from domain.value_objects.username import Username
from infrastructure.database.repository.user import UserRepository
from infrastructure.security.hasher import PasswordHasher



@dataclasses.dataclass()
class LoginUserCommand(BaseCommand):
    login: Username
    password: str

@dataclasses.dataclass()
class LoginUserUseCase(BaseUseCase):
    hasher: HasherProtocol
    user_repository: UserRepository
    token_repository: TokenRepositoryProtocol[AuthToken]
    token_service: TokenServiceProtocol


    async def execute(self, command: LoginUserCommand) -> tuple[User, AuthToken, TokenKey]:
        user = await self.user_repository.get_by_username(username=command.login)

        if user is None:
            raise InvalidCredentialsError("Invalid login.")

        if not self.hasher.verify(raw_secret=command.password, hashed_secret=user.hashed_password):
            raise InvalidCredentialsError("Invalid password")

        auth_token, token_key = self.token_service.generate_token(user, ttl=TTL.from_seconds(60*60*24*7))

        auth_token = await self.token_repository.add(auth_token)
        return user, auth_token, token_key