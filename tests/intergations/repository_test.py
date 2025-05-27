from core.config import Settings
from domain.value_objects.email import Email
from infrastructure.database.repository.user import UserRepository
from domain.entities.user import User


class TestUserRepository:
    async def test_add(self, settings: Settings, user_repository: UserRepository):
        test_user = User(
            id = "",
            email = Email(
                value="test@mail.ru"
            ),
            hashed_password = "pass",
            is_active = False
        )
        await user_repository.add(test_user)

