from typing import Protocol

from domain.value_objects.hashed_password import HashedPassword


class PasswordHasherProtocol(Protocol):
    def verify(self, raw_password: str, hashed_password: HashedPassword) -> bool: ...

    def hash(self, raw_password: str) -> HashedPassword: ...
