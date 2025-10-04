import typing

from domain.value_objects.hashed_secret import HashedSecret


class TokenRepositoryProtocol[TToken](typing.Protocol):
    """Token repository protocol."""

    async def get_by_hashed_key(self, hashed_key: HashedSecret) -> TToken | None:
        """Return token by hashed token key."""

    async def add(self, token: TToken) -> TToken:
        """Save token."""

    async def delete(self, token: TToken) -> None:
        """Delete token."""