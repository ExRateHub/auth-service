import json
from dataclasses import dataclass
from typing import Any

from domain.errors import InvalidJWTToken
from domain.value_objects.base import BaseValueObject
from domain.value_objects.base64_strng import Base64String


@dataclass(frozen=True)
class JwtToken(BaseValueObject[str]):
    @property
    def parts(self) -> tuple[Base64String, Base64String, Base64String]:
        parts = self.value.split(".")
        return tuple(Base64String(part) for part in parts)  # type: ignore[return-value]

    @property
    def header(self) -> Base64String:
        return self.parts[0]

    @property
    def payload(self) -> Base64String:
        return self.parts[1]

    @property
    def signature(self) -> Base64String:
        return self.parts[2]

    @property
    def header_obj(self) -> dict[str, Any]:
        decoded = self.header.decode()
        return json.loads(decoded)

    @property
    def payload_obj(self) -> dict[str, Any]:
        decoded = self.payload.decode()
        return json.loads(decoded)

    def validate(self) -> None:
        try:
            parts = self.parts
        except Exception as e:
            raise InvalidJWTToken(f"Invalid JWT token format: {e}")

        if len(parts) != 3:
            raise InvalidJWTToken(f"Invalid JWT token format: expected exactly 3 parts, got {len(parts)}")

        try:
            _ = self.header_obj
        except json.JSONDecodeError as e:
            raise InvalidJWTToken(f"Invalid JWT token format: invalid JSON in header: {e}")
        except UnicodeDecodeError as e:
            raise InvalidJWTToken(f"Invalid JWT token format: invalid UTF-8 encoding in header: {e}")

        header = self.header_obj
        if "alg" not in header:
            raise InvalidJWTToken("Invalid JWT token format: JWT header missing required field 'alg'")
        if header.get("typ") != "JWT":
            raise InvalidJWTToken("Invalid JWT token format: JWT header 'typ' must be 'JWT'")

        try:
            _ = self.payload_obj
        except json.JSONDecodeError as e:
            raise InvalidJWTToken(f"Invalid JWT token format: invalid JSON in payload: {e}")
        except UnicodeDecodeError as e:
            raise InvalidJWTToken(f"Invalid JWT token format: invalid UTF-8 encoding in payload: {e}")

    def as_generic_type(self) -> str:
        return str(self.value)
