import dataclasses
import secrets

from application.ports.hasher import HasherProtocol
from application.ports.token_service import TokenServiceProtocol
from domain.entities.auth_token import AuthToken
from domain.entities.user import User
from domain.value_objects.token_key import TokenKey
from domain.value_objects.ttl import TTL


@dataclasses.dataclass
class AuthTokenService(TokenServiceProtocol[User, AuthToken, TokenKey]):
    hasher: HasherProtocol

    def generate_token(self, payload: User, ttl: TTL) -> tuple[AuthToken, TokenKey]:
        token_key = TokenKey(secrets.token_hex(16))
        auth_token = AuthToken.create(
            hashed_key=self.hasher.hash(token_key.as_generic_type()),
            user_id=payload.id,
            ttl=ttl,
        )
        return auth_token, token_key


    def verify(self, token: AuthToken) -> bool:
        return not token.is_expired and not token.is_revoked
