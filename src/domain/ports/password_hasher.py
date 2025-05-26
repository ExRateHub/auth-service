from typing import Protocol


class PasswordHasherProtocol(Protocol):
    def verify(self, raw_password: str, hashed_password: str) -> bool: ...

    def hash(self, raw_password: str) -> str: ...
