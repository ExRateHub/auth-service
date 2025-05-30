import datetime
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self

from domain.value_objects.hashed_secret import HashedSecret


@dataclass
class BaseEntity(ABC):
    id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC), kw_only=True)
    updated_at: datetime.datetime | None = field(default=None, kw_only=True)

    def __post_init__(self) -> None:
        if self.updated_at is None:
            self.updated_at = self.created_at

    @classmethod
    @abstractmethod
    def create(cls, *args: Any, **kwargs: Any) -> Self:
        """
        Factory method for creating a new entity.
        Must be implemented in subclasses.
        """
        raise NotImplementedError()

    def _update_timestamp(self) -> None:
        """(protected) update the `updated_at` timestamp to now."""
        self.updated_at = datetime.datetime.now(datetime.UTC)


@dataclass
class BaseToken(BaseEntity):
    hashed_token: HashedSecret
    expires_at: datetime.datetime
    is_revoked: bool = field(default=False, kw_only=True)

    @classmethod
    @abstractmethod
    def create(cls, *args: Any, **kwargs: Any) -> Self:
        """
        Factory method for creating a new entity.
        Must be implemented in subclasses.
        """
        raise NotImplementedError()

    def is_expired(self) -> bool:
        return datetime.datetime.now(datetime.UTC) >= self.expires_at

    def revoke(self) -> None:
        self.is_revoked = True
        self._update_timestamp()
