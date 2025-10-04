import dataclasses

from application.ports.token_repository import TokenRepositoryProtocol
from domain.entities.auth_token import AuthToken
from domain.value_objects.hashed_secret import HashedSecret


@dataclasses.dataclass
class AuthTokenRepositoryMemStorage(TokenRepositoryProtocol[AuthToken]):
    _storage: dict[HashedSecret, AuthToken] = dataclasses.field(default_factory=dict)

    async def get_by_hashed_key(self, hashed_key: HashedSecret) -> AuthToken | None:
        return self._storage.get(hashed_key, None)

    async def add(self, token: AuthToken) -> AuthToken:
        self._storage[token.hashed_key] = token
        return token

    async def delete(self, token: AuthToken) -> None:
        self._storage.pop(token.hashed_key, None)

