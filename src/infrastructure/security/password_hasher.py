from domain.ports.password_hasher import PasswordHasherProtocol
from pwdlib import PasswordHash as PWDLibPasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher as PWDLibArgon2Hasher



class Argon2Hasher:
    _hasher = PWDLibPasswordHash(hashers=[PWDLibArgon2Hasher(), ])

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return self._hasher.verify(password=raw_password, hash=hashed_password)

    def hash(self, raw_password: str) -> str:
        return self._hasher.hash(password=raw_password)
