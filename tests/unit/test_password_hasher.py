import pytest

from infrastructure.security.password_hasher import PasswordHasher


@pytest.fixture(scope="session")
def password_hasher() -> PasswordHasher:
    return PasswordHasher()


def test_password_hasher(password_hasher: PasswordHasher) -> None:
    raw_password = "Password"

    hashed_password = password_hasher.hash(raw_password)

    assert hashed_password != raw_password
    assert password_hasher.verify(raw_password, hashed_password) is True
