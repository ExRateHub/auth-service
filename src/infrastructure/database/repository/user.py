from dataclasses import dataclass

from domain.entities.user import User
from infrastructure.database.models import UserModel
from infrastructure.database.repository.base import BaseSQLAlchemyRepository


@dataclass
class UserRepository(BaseSQLAlchemyRepository[UserModel, User]):
    model_type = UserModel
    entity_type = User
