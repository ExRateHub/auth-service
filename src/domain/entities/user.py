from __future__ import annotations

from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.hashed_secret import HashedSecret
from domain.value_objects.username import Username


@dataclass
class User(BaseEntity):
    username: Username
    hashed_password: HashedSecret
    is_active: bool

    @classmethod
    def create(
        cls: type[User],
        username: Username,
        hashed_password: HashedSecret,
        *,
        is_active: bool = False,
    ) -> User:
        return cls(
            username=username,
            hashed_password=hashed_password,
            is_active=is_active,
        )

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
