import dataclasses

from domain.errors import InvalidTokenKey
from domain.value_objects.base import BaseValueObject

@dataclasses.dataclass(frozen=True)
class TokenKey(BaseValueObject[str]):

    def validate(self) -> None:
        if len(self.value) != 32:
            raise InvalidTokenKey("The length of the token should be 32 characters. (Now {len (self.value)})")

    def as_generic_type(self) -> str:
        return self.value