from __future__ import annotations

import datetime
from dataclasses import dataclass

from domain.errors import InvalidTTL
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class TTL(BaseValueObject[datetime.timedelta]):
    def validate(self) -> None:
        if self.value.total_seconds() <= 0:
            raise InvalidTTL("Invalid ttl value: value should be greater than 0")

    def as_generic_type(self) -> datetime.timedelta:
        return self.value

    @classmethod
    def from_seconds(cls, seconds: int) -> TTL:
        return cls(datetime.timedelta(seconds=seconds))
