from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence


@dataclass(frozen=True)
class EmailMessageContent:
    type: Literal["text/plain", "text/html"]
    body: str


@dataclass(frozen=True)
class EmailMessageDTO:
    to_email: str
    subject: str
    content: EmailMessageContent
    alternative_contents: Sequence[EmailMessageContent]
