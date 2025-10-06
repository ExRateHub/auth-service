from domain.entities.auth_token import AuthToken
from domain.value_objects.hashed_secret import HashedSecret
from infrastructure.orm.models import AuthTokenModel
from infrastructure.persistence.mappers.base import BaseMapper


class AuthTokenMapper(BaseMapper[AuthToken, AuthTokenModel]):

    def to_entity(self, data: AuthTokenModel) -> AuthToken:
        entity = AuthToken(
            hashed_key=HashedSecret(data.hashed_key),
            expires_at=data.expired_at,
            id=data.id,
            user_id=data.user_id,
        )
        return entity

    def to_model(self, data: AuthToken) -> AuthTokenModel:
        model = AuthTokenModel(
            id=data.id,
            user_id=data.user_id,
            hashed_key=data.hashed_key.as_generic_type(),
            expired_at=data.expires_at,
        )
        return model