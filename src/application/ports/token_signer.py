from typing import Protocol, Any

from domain.value_objects.jwt_token import JwtToken, JwtPayload


class TokenSignerProtocol(Protocol):
    def sign(self, payload: JwtPayload) -> JwtToken: ...

    def verify(self, token: JwtToken) -> bool: ...

    def decode(self, token: JwtToken) -> JwtPayload: ...
