from __future__ import annotations
import dataclasses
import datetime
import uuid

from domain.entities.base import BaseToken
from domain.value_objects.hashed_secret import HashedSecret
from domain.value_objects.ttl import TTL


@dataclasses.dataclass
class AuthToken(BaseToken):
    user_id: uuid.UUID
    @classmethod
    def create(
        cls: type[AuthToken],
        user_id: uuid.UUID,
        hashed_key: HashedSecret,
        ttl: TTL,
    ) -> AuthToken:
        return cls(
            user_id=user_id,
            hashed_key=hashed_key,
            expires_at=datetime.datetime.now(datetime.UTC) + ttl.as_generic_type(),
        )

