import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email address: {self.value}")
