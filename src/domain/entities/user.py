from __future__ import annotations

import uuid
from dataclasses import dataclass

from domain.ports.password_hasher import PasswordHasherProtocol
from domain.value_objects.email import Email


@dataclass(frozen=True)
class User:
    id: uuid.UUID
    email: Email
    hashed_password: str
    is_active: bool

    def verify_password(self, raw_password: str, hasher: PasswordHasherProtocol) -> bool:
        return hasher.verify(raw_password, self.hashed_password)

    def mark_active(self) -> User:
        return User(
            id=self.id, email=self.email, hashed_password=self.hashed_password, is_active=True
        )

    def mark_inactive(self) -> User:
        return User(
            id=self.id, email=self.email, hashed_password=self.hashed_password, is_active=False
        )
