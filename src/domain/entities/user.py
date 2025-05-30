from __future__ import annotations

from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.email import Email
from domain.value_objects.hashed_secret import HashedSecret


@dataclass
class User(BaseEntity):
    email: Email
    hashed_password: HashedSecret
    is_active: bool

    @classmethod
    def create(
        cls: type[User],
        email: Email,
        hashed_password: HashedSecret,
        *,
        is_active: bool = False,
    ) -> User:
        return cls(
            email=email,
            hashed_password=hashed_password,
            is_active=is_active,
        )

    def activate(self) -> None:
        self.is_active = True
        self._update_timestamp()

    def deactivate(self) -> None:
        self.is_active = False
        self._update_timestamp()
