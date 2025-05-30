from __future__ import annotations

import datetime
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal

from domain.errors import InvalidJwtToken, InvalidJwtHeader, InvalidJwtPayload
from domain.value_objects.base import BaseValueObject
from domain.value_objects.base64_strng import Base64String


@dataclass(frozen=True)
class JwtPart(ABC):
    """Abstract base class for JWT parts (header/payload)."""

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None: ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> JwtPart: ...

    @abstractmethod
    def as_generic_type(self) -> str: ...

    def __str__(self) -> str:
        return self.as_generic_type()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict()})"


@dataclass(frozen=True)
class JwtHeader(JwtPart):
    alg: str
    typ: Literal["JWT"] = field(default="JWT", kw_only=True)

    def validate(self) -> None:
        if not isinstance(self.alg, str) or not isinstance(self.typ, str):
            raise InvalidJwtHeader("Invalid JWT header: header field 'alg' and 'typ must be 'str'")
        if self.alg.strip() == "":
            raise InvalidJwtHeader("Invalid JWT header: header field 'alg' is required")
        if self.typ != "JWT":
            raise InvalidJwtHeader("Invalid JWT header: header field 'typ' must be 'JWT'")

    def to_dict(self) -> dict[str, Any]:
        result = {
            "alg": self.alg,
            "typ": self.typ,
        }
        return result

    def as_generic_type(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JwtHeader:
        return cls(
            alg=data.get("alg", ""),
        )


@dataclass(frozen=True)
class JwtPayload(JwtPart):
    sub: str
    scope: str
    iat: datetime.datetime | None
    exp: datetime.datetime | None

    def validate(self) -> None:
        if not isinstance(self.sub, str) or not isinstance(self.scope, str):
            raise InvalidJwtPayload("Invalid JWT payload: 'sub' and 'scope' must be 'srt")
        if self.sub.strip() == "":
            raise InvalidJwtPayload("Invalid JWT payload: sub is required")
        if not isinstance(self.iat, datetime.datetime) or not isinstance(self.exp, datetime.datetime):
            raise InvalidJwtPayload("Invalid JWT payload: iat and exp must be datetime")
        if (self.exp - self.iat).total_seconds() <= 0:
            raise InvalidJwtPayload("Invalid JWT payload: iat must be before exp")

    def to_dict(self) -> dict[str, Any]:
        return {
            "sub": self.sub,
            "scope": self.scope,
            "iat": self.iat,
            "exp": self.exp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JwtPayload:
        iat_ts = data.get("iat")
        exp_ts = data.get("exp")

        iat_dt = datetime.datetime.fromtimestamp(iat_ts, tz=datetime.timezone.utc) if iat_ts is not None else None
        exp_dt = datetime.datetime.fromtimestamp(exp_ts, tz=datetime.timezone.utc) if exp_ts is not None else None

        return cls(sub=data.get("sub", ""), scope=data.get("scope", ""), iat=iat_dt, exp=exp_dt)

    def as_generic_type(self) -> str:
        return json.dumps(self.to_dict())


@dataclass(frozen=True)
class JwtToken(BaseValueObject[str]):
    @property
    def parts(self) -> tuple[Base64String, Base64String, Base64String]:
        parts = self.value.split(".")

        if len(parts) != 3:
            raise InvalidJwtToken(f"Invalid JWT token format: expected exactly 3 parts, got {len(parts)}")

        base64_parts = []
        for i, part in enumerate(parts):
            try:
                base64_parts.append(Base64String(part))
            except Exception as e:
                raise InvalidJwtToken(f"Invalid JWT token: Invalid Base64 encoding in JWT part {i + 1}: {e}")
        return tuple(base64_parts)  # type: ignore[return-value]

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
    def header_obj(self) -> JwtHeader:
        try:
            decoded = self.header.decode()
            data = json.loads(decoded)
            return JwtHeader.from_dict(data)
        except Exception as e:
            raise InvalidJwtToken(f"Invalid JWT header: {e}")

    @property
    def payload_obj(self) -> JwtPayload:
        try:
            decoded = self.payload.decode()
            data = json.loads(decoded)
            return JwtPayload.from_dict(data)
        except Exception as e:
            raise InvalidJwtToken(f"Invalid JWT payload: {e}")

    def validate(self) -> None:
        try:
            parts = self.parts
        except Exception as e:
            raise e

        try:
            _ = self.header_obj
        except json.JSONDecodeError as e:
            raise InvalidJwtToken(f"Invalid JWT token format: invalid JSON in header: {e}")
        except UnicodeDecodeError as e:
            raise InvalidJwtToken(f"Invalid JWT token format: invalid UTF-8 encoding in header: {e}")
        except Exception as e:
            raise e

        try:
            _ = self.payload_obj
        except json.JSONDecodeError as e:
            raise InvalidJwtToken(f"Invalid JWT token format: invalid JSON in payload: {e}")
        except UnicodeDecodeError as e:
            raise InvalidJwtToken(f"Invalid JWT token format: invalid UTF-8 encoding in payload: {e}")
        except Exception as e:
            raise e

    def as_generic_type(self) -> str:
        return str(self.value)
