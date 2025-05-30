import sys
from dataclasses import dataclass, field
from typing import Sequence

from application.dto.email_message import EmailMessage
from application.ports.email_sender import EmailSender


@dataclass()
class ConsoleEmailSender(EmailSender):
    name: str = field(default="console", init=False)
    def __post_init__(self) -> None:
        self._stream = sys.stdin

    async def _write_message(self, message: EmailMessage) -> None:
        msg = (
            "[ConsoleEmailSender] Preparing to send email\n"
            f"To: {message.to_email}\n"
            f"Subject: {message.subject}\n"
            f"Body: {message.body}\n"
            f"=" * 60 + "\n"
        )
        self._stream.write(msg)

    async def send_messages(self, messages: Sequence[EmailMessage]) -> int:
        sent_count = 0
        for message in messages:
            await self._write_message(message)
            sent_count += 1
        return sent_count




