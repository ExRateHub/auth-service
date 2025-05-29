import copy
import datetime
import time
import uuid
from dataclasses import dataclass
from typing import Self

import pytest

from domain.entities.base import BaseEntity
from domain.entities.user import User
from domain.value_objects.email import Email
from infrastructure.security.password_hasher import PasswordHasher


@dataclass
class DummyEntity(BaseEntity):
    @classmethod
    def create(cls) -> Self:
        return cls()


class TestBaseEntity:
    def test_create_sets_id_and_timestamps(self) -> None:
        dummy = DummyEntity.create()
        assert isinstance(dummy.id, uuid.UUID)
        assert isinstance(dummy.created_at, datetime.datetime)
        assert isinstance(dummy.updated_at, datetime.datetime)
        assert dummy.created_at == dummy.updated_at

    def test_update_timestamp_bumps_updated_at(self) -> None:
        dummy = DummyEntity.create()
        before = dummy.updated_at
        time.sleep(0.001)
        dummy._update_timestamp()
        assert dummy.updated_at > before

    def test_manual_init_preserves_passed_updated_at(self) -> None:
        now = datetime.datetime(2021, 1, 1, tzinfo=datetime.timezone.utc)
        later = now + datetime.timedelta(hours=3)
        entity = DummyEntity(
            id=uuid.uuid4(),
            created_at=now,
            updated_at=later,
        )
        assert entity.created_at == now
        assert entity.updated_at == later

    def test_equality_and_hash_by_id(self) -> None:
        entity_1 = DummyEntity.create()
        entity_2 = DummyEntity.create()
        assert entity_1 != entity_2
        assert entity_1 == copy.copy(entity_1)
        assert entity_1 is not copy.copy(entity_1)
        with pytest.raises(TypeError):
            hash(entity_1)


class TestUserEntity:
    def test_create_sets_fields(self) -> None:
        email = Email("example@domain.com")
        hashed_password = PasswordHasher().hash("1234")
        user = User.create(email=email, hashed_password=hashed_password)

        assert isinstance(user.id, uuid.UUID) is True
        assert user.email == email
        assert user.hashed_password == hashed_password
        assert user.is_active is False

    def test_activate_user(self) -> None:
        email = Email("example@domain.com")
        hashed_password = PasswordHasher().hash("1234")
        user = User.create(email=email, hashed_password=hashed_password)
        user.activate()

        assert user.is_active is True

    def test_deactivate_user(self) -> None:
        email = Email("example@domain.com")
        hashed_password = PasswordHasher().hash("1234")
        user = User.create(email=email, hashed_password=hashed_password)
        user.deactivate()

        assert user.is_active is False
