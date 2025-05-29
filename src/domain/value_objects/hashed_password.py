from dataclasses import dataclass

from domain.errors import InvalidHashedPassword
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class HashedPassword(BaseValueObject):
    """
    Value object for hashed passwords.
    Ensures the hashed password follows the Modular Crypt Format (MCF):
    $<algorithm>$<options>$<salt>$<hash>

    Properties:
        algorithm: str -- the hashing algorithm identifier

        options: str -- the algorithm parameters (costs, memory, etc.)

        salt: str -- the salt used for hashing

        hash: str -- the resulting hash
    """

    value: str

    @property
    def algorithm(self) -> str:
        """Return the hashing algorithm identifier."""
        return self.value.split("$")[1]

    @property
    def options(self) -> str:
        """Return the algorithm parameters string."""
        return "$".join(self.value.split("$")[2:-2])

    @property
    def salt(self) -> str:
        """Return the salt portion of the MCF string."""
        return self.value.split("$")[-2]

    @property
    def hash(self) -> str:
        """Return the hash portion of the MCF string."""
        return self.value.split("$")[-1]

    def validate(self) -> None:
        parts = self.value.split("$")
        if len(parts) < 5 or not parts[1] or not parts[-2] or not parts[-1]:
            raise InvalidHashedPassword(f"Invalid MCF format: expected at least 4 fields, got {len(parts)-1}")

    def as_generic_type(self) -> str:
        return str(self.value)
