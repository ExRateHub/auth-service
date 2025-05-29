import datetime
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self


@dataclass()
class BaseEntity(ABC):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    updated_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return type(self) is type(other) and self.id == other.id

    def __hash__(self) -> int:
        return hash((type(self), self.id))
