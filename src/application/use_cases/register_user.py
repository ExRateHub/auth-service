import dataclasses
import typing

from application.use_cases.base import BaseUseCase, BaseCommand
from domain.entities.user import User
from domain.errors import UsernameAlreadyExists
from domain.value_objects.username import Username
from infrastructure.database.repository.user import UserRepository
from infrastructure.security.hasher import PasswordHasher


@dataclasses.dataclass()
class RegisterUserCommand(BaseCommand):
    username: Username
    password: str

@dataclasses.dataclass()
class RegisterUserUseCase(BaseUseCase):
    user_repository: UserRepository
    hasher: PasswordHasher

    async def execute(self, command: RegisterUserCommand) -> User:
        user = await self.user_repository.get_by_username(username=command.username)

        if user is not None:
            raise UsernameAlreadyExists()

        user = User.create(
            username=command.username,
            hashed_password=self.hasher.hash(command.password)
        )
        user = await self.user_repository.add(user)
        return user