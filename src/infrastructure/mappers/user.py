from domain.entities.user import User
from domain.value_objects.hashed_secret import HashedSecret
from domain.value_objects.username import Username
from infrastructure.orm.models import UserModel
from infrastructure.mappers.base import BaseMapper


class UserMapper(BaseMapper[User, UserModel]):

    def to_entity(self, data: UserModel) -> User:
        entity = User(
            username=Username(data.username),
            hashed_password=HashedSecret(data.hashed_password),
            is_active=data.is_active
        )
        return entity

    def to_model(self, data: User) -> UserModel:
        entity = UserModel(
            id=data.id,
            username=data.username.as_generic_type(),
            hashed_password=data.hashed_password.as_generic_type(),
            is_active=data.is_active
        )
        return entity