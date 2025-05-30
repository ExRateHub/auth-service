from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass

from domain.entities.base import BaseToken
from domain.value_objects.hashed_secret import HashedSecret
from domain.value_objects.ttl import TTL


@dataclass
class RefreshToken(BaseToken):
    @classmethod
    def create(
        cls: type[RefreshToken],
        user_id: uuid.UUID,
        hashed_token: HashedSecret,
        ttl: TTL,
    ) -> RefreshToken:
        return cls(
            id=user_id,
            hashed_token=hashed_token,
            expires_at=datetime.datetime.now(datetime.UTC) + ttl.as_generic_type(),
        )
