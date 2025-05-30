from pwdlib import PasswordHash as PWDLibPasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher as PWDLibArgon2Hasher

from domain.value_objects.hashed_secret import HashedSecret


class Argon2Hasher:
    _hasher = PWDLibPasswordHash(
        hashers=[
            PWDLibArgon2Hasher(),
        ]
    )

    def verify(self, raw_secret: str, hashed_secret: HashedSecret) -> bool:
        return self._hasher.verify(password=raw_secret, hash=hashed_secret.as_generic_type())

    def hash(self, raw_secret: str) -> HashedSecret:
        return HashedSecret(self._hasher.hash(password=raw_secret))


class PasswordHasher(Argon2Hasher):
    pass


class TokenHasher(Argon2Hasher):
    pass
