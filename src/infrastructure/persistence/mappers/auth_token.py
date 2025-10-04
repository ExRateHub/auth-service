from domain.entities.auth_token import AuthToken
from domain.entities.user import User
from domain.value_objects.hashed_secret import HashedSecret
from domain.value_objects.username import Username
from infrastructure.orm.models import UserModel, AuthTokenModel
from infrastructure.persistence.mappers.base import BaseMapper


class AuthTokenMapper(BaseMapper[AuthToken, AuthTokenModel]):

    def to_entity(self, data: AuthTokenModel) -> AuthToken:
        entity = User(
            username=Username(data.username),
            hashed_password=HashedSecret(data.hashed_password),
            is_active=data.is_active
        )
        return entity

    def to_model(self, data: AuthToken) -> AuthTokenModel:
        model = AuthTokenModel(
            id=data.id,
            hashed_key=data.hashed_key.as_generic_type(),
            expired_at=data.expires_at,
        )
        return model