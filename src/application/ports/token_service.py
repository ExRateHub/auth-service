from typing import Protocol

from domain.value_objects.ttl import TTL


class TokenServiceProtocol[TPayload, TToken, TTokenKey](Protocol):
    """Token service protocol."""
    def generate_token(self, payload: TPayload, ttl: TTL) -> tuple[TToken, TTokenKey]:
        """Generate a token and return token and token key"""

    def verify(self, token: TToken) -> bool:
        """Check the token for validity."""
