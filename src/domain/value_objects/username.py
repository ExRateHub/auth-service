import re
from dataclasses import dataclass

from domain.errors import InvalidEmail, InvalidUsername
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class Username(BaseValueObject[str]):
    def validate(self) -> None:
        first_letter_pattern = r"^[A-Za-z]"
        permissible_symbols_pattern = r"[A-Za-z0-9_]*$"

        if len(self.value) > 32:
            raise InvalidUsername(f"Username is longer than 32 characters. (Current length {len (self.value)}).")
        elif len(self.value) < 4:
            raise InvalidUsername(f"Username is short than 4 characters. (Current length {len (self.value)}).")
        elif not re.match(first_letter_pattern, self.value):
            raise InvalidUsername(f"Username begins with an unacceptable symbol. Username should only begin with the Latin letter.")
        elif not re.match(permissible_symbols_pattern, self.value):
            raise InvalidUsername(f"Username contains unacceptable characters. Use only Latin letters, numbers and _.")

    def as_generic_type(self) -> str:
        return str(self.value)
