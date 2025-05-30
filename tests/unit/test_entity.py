import copy
import datetime
import time
import uuid
from dataclasses import dataclass
from typing import Self

import pytest

from domain.entities.base import BaseEntity, BaseToken
from domain.entities.confirm_token import ConfirmToken
from domain.entities.refresh_token import RefreshToken
from domain.entities.reset_token import ResetToken
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.hashed_secret import HashedSecret
from domain.value_objects.ttl import TTL
from infrastructure.security.hasher import PasswordHasher


@dataclass
class DummyEntity(BaseEntity):
    @classmethod
    def create(cls) -> Self:
        return cls()


@dataclass
class DummyToken(BaseToken):
    @classmethod
    def create(cls, hashed_token: HashedSecret, expires_at: datetime.datetime) -> Self:
        return cls(hashed_token=hashed_token, expires_at=expires_at)


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


class TestBaseToken:
    def setup_method(self):
        self.now = datetime.datetime.now(datetime.UTC)
        self.future = self.now + datetime.timedelta(minutes=10)
        self.past = self.now - datetime.timedelta(minutes=10)
        self.hashed = HashedSecret("$argon2id$v=19$m=102400,t=2,p=8$ZGF0YXNhbHQ$ZGF0YWhhc2g")

    @pytest.mark.parametrize(
        "hashed_secret,expires_at",
        [
            (
                HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"),
                datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=10),
            ),
            (
                HashedSecret("$argon2id$v=19$m=131072,t=2,p=2$Y3VzdG9tc2FsdDI=$aGFzaGRhdGEy"),
                datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
            ),
            (
                HashedSecret("$argon2id$v=19$m=4096,t=1,p=1$c2ltcGxlc2FsdA==$c2ltcGxlZGF0YWhhc2g="),
                datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=5),
            ),
            (
                HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"),
                datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=10),
            ),
        ],
    )
    def test_create_sets(self, hashed_secret, expires_at):
        token = DummyToken.create(
            hashed_token=hashed_secret,
            expires_at=expires_at,
        )
        assert isinstance(token.expires_at, datetime.datetime)
        assert isinstance(token.hashed_token, HashedSecret)
        assert token.is_revoked is False

    @pytest.mark.parametrize(
        "hashed_secret,expires_at",
        [
            (
                HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"),
                datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=10),
            ),
            (
                HashedSecret("$argon2id$v=19$m=131072,t=2,p=2$Y3VzdG9tc2FsdDI=$aGFzaGRhdGEy"),
                datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
            ),
            (
                HashedSecret("$argon2id$v=19$m=4096,t=1,p=1$c2ltcGxlc2FsdA==$c2ltcGxlZGF0YWhhc2g="),
                datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            ),
            (
                HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"),
                datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1000),
            ),
        ],
    )
    def test_token_is_not_expired(self, hashed_secret, expires_at):
        token = DummyToken.create(
            hashed_token=hashed_secret,
            expires_at=expires_at,
        )
        assert not token.is_expired()

    @pytest.mark.parametrize(
        "hashed_secret,expires_at",
        [
            (
                HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"),
                datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=10),
            ),
            (
                HashedSecret("$argon2id$v=19$m=131072,t=2,p=2$Y3VzdG9tc2FsdDI=$aGFzaGRhdGEy"),
                datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=5),
            ),
            (
                HashedSecret("$argon2id$v=19$m=4096,t=1,p=1$c2ltcGxlc2FsdA==$c2ltcGxlZGF0YWhhc2g="),
                datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=60),
            ),
            (
                HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"),
                datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1000),
            ),
        ],
    )
    def test_token_is_expired(self, hashed_secret, expires_at):
        token = DummyToken.create(
            hashed_token=hashed_secret,
            expires_at=expires_at,
        )
        assert token.is_expired()

    @pytest.mark.parametrize(
        "hashed_secret,expires_at",
        [
            (
                HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"),
                datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=10),
            ),
            (
                HashedSecret("$argon2id$v=19$m=131072,t=2,p=2$Y3VzdG9tc2FsdDI=$aGFzaGRhdGEy"),
                datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=5),
            ),
            (
                HashedSecret("$argon2id$v=19$m=4096,t=1,p=1$c2ltcGxlc2FsdA==$c2ltcGxlZGF0YWhhc2g="),
                datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=60),
            ),
            (
                HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"),
                datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1000),
            ),
        ],
    )
    def test_revoke_token(self, hashed_secret, expires_at):
        token = DummyToken.create(
            hashed_token=hashed_secret,
            expires_at=expires_at,
        )
        token.revoke()
        assert token.is_revoked


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


class TestRefreshToken:
    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(10)),
        ],
    )
    def test_create_sets(self, hashed_secret, ttl):
        RefreshToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )

    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(1)),
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(1000)),
        ],
    )
    def test_expired(self, hashed_secret, ttl):
        token = RefreshToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        assert not token.is_expired()
        token.expires_at -= ttl.as_generic_type()
        assert token.is_expired()


class TestConfirmToken:
    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(10)),
        ],
    )
    def test_create_sets(self, hashed_secret, ttl):
        token = ConfirmToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        assert token.is_confirmed is False

    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(1)),
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(1000)),
        ],
    )
    def test_expired(self, hashed_secret, ttl):
        token = ConfirmToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        assert not token.is_expired()
        token.expires_at -= ttl.as_generic_type()
        assert token.is_expired()

    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(10)),
        ],
    )
    def test_is_not_confirmed(self, hashed_secret, ttl):
        token = ConfirmToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        assert not token.is_confirmed

    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(10)),
        ],
    )
    def test_is_confirmed(self, hashed_secret, ttl):
        token = ConfirmToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        token.confirm()
        assert token.is_confirmed


class TestResetToken:
    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(10)),
        ],
    )
    def test_create_sets(self, hashed_secret, ttl):
        token = ResetToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        assert token.is_used is False

    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(1)),
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(1000)),
        ],
    )
    def test_expired(self, hashed_secret, ttl):
        token = ResetToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        assert not token.is_expired()
        token.expires_at -= ttl.as_generic_type()
        assert token.is_expired()

    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(10)),
        ],
    )
    def test_is_not_confirmed(self, hashed_secret, ttl):
        token = ResetToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        assert not token.is_used

    @pytest.mark.parametrize(
        "hashed_secret,ttl",
        [
            (HashedSecret("$argon2id$v=19$m=65536,t=3,p=4$c2FsdGJhc2Ux$ZGF0YWhhc2gx"), TTL.from_seconds(10)),
        ],
    )
    def test_is_confirmed(self, hashed_secret, ttl):
        token = ResetToken.create(
            user_id=uuid.uuid4(),
            hashed_token=hashed_secret,
            ttl=ttl,
        )
        token.mark_as_used()
        assert token.is_used
