import base64
from dataclasses import dataclass

from domain.errors import InvalidBase64Encoding
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class Base64String(BaseValueObject[str]):
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise InvalidBase64Encoding("Invalid base64 encoding: value must be a string")

        if not self.value:
            raise InvalidBase64Encoding("Invalid base64 encoding: empty string is not valid Base64")

        try:
            self.value.encode("ascii")
        except UnicodeEncodeError:
            raise InvalidBase64Encoding("Invalid base64 encoding: contains non-ASCII characters")

        try:
            padding = "=" * (-len(self.value) % 4)
            base64.urlsafe_b64decode(self.value + padding)
        except Exception as e:
            raise InvalidBase64Encoding(f"Invalid base64 encoding: {e}")

    def as_generic_type(self) -> str:
        return self.value

    def decode(self, encoding="utf-8") -> str:
        try:
            padding = "=" * (-len(self.value) % 4)
            return base64.urlsafe_b64decode(self.value + padding).decode(encoding)
        except Exception as e:
            raise InvalidBase64Encoding(f"Invalid base64 encoding: decoding failed: {e}")
