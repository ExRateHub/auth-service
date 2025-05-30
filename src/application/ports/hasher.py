from typing import Protocol

from domain.value_objects.hashed_secret import HashedSecret


class HasherProtocol(Protocol):
    def verify(self, raw_secret: str, hashed_secret: HashedSecret) -> bool: ...

    def hash(self, raw_secret: str) -> HashedSecret: ...
