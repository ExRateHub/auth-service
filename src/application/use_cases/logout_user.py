import dataclasses

from application.errors import InvalidTokenError
from application.ports.hasher import HasherProtocol
from application.ports.token_repository import TokenRepositoryProtocol
from application.ports.token_service import TokenServiceProtocol
from application.use_cases.base import BaseUseCase, BaseCommand
from domain.errors import InvalidCredentialsError
from domain.value_objects.hashed_secret import HashedSecret
from domain.value_objects.token_key import TokenKey


@dataclasses.dataclass()
class LogoutUserCommand(BaseCommand):
    token_key: TokenKey


@dataclasses.dataclass
class LogoutUserUseCase(BaseUseCase):
    hasher: HasherProtocol
    token_repository: TokenRepositoryProtocol
    token_service: TokenServiceProtocol

    async def execute(self, command: LogoutUserCommand) -> None:
        token_hash = self.hasher.hash(command.token_key.as_generic_type())
        print(token_hash)
        auth_token = await self.token_repository.get_by_hashed_key(token_hash)
        print("token gotten ", auth_token)

        if not auth_token:
            print("not token")
            raise InvalidTokenError()

        await self.token_repository.delete(auth_token)
