from pwdlib import PasswordHash as PWDLibPasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher as PWDLibArgon2Hasher

from domain.value_objects.hashed_password import HashedPassword


class Argon2Hasher:
    _hasher = PWDLibPasswordHash(
        hashers=[
            PWDLibArgon2Hasher(),
        ]
    )

    def verify(self, raw_password: str, hashed_password: HashedPassword) -> bool:
        return self._hasher.verify(password=raw_password, hash=hashed_password.as_generic_type())

    def hash(self, raw_password: str) -> HashedPassword:
        return HashedPassword(self._hasher.hash(password=raw_password))


class PasswordHasher(Argon2Hasher):
    pass
