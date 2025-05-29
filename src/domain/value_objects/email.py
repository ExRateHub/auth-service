import re
from dataclasses import dataclass

from domain.errors import InvalidEmail
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class Email(BaseValueObject[str]):
    def validate(self) -> None:
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, self.value):
            raise InvalidEmail(f"Invalid email address: {self.value}")

    def as_generic_type(self) -> str:
        return str(self.value)
