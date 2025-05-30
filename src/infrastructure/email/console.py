import sys
from dataclasses import dataclass, field
from typing import TextIO

from application.dto.email_message import EmailMessageDTO
from application.ports.email_sender import EmailSender


@dataclass()
class ConsoleEmailSender(EmailSender):
    name: str = field(default="console", init=False)
    stream: TextIO = field(default=sys.stdout, kw_only=True)

    async def _write_message(self, message: EmailMessageDTO) -> None:
        msg = (
            "[ConsoleEmailSender] Preparing to send email\n"
            f"To: {message.to_email}\n"
            f"Subject: {message.subject}\n"
            f"Alternative content-types: {[content.type for content in message.alternative_contents]}\n"
            f"Content-Type: {message.content.type}\n"
            f"Content: {message.content.body}\n"
            f"{'=' * 60}\n"
        )
        self.stream.write(msg)

    async def send_messages(self, *messages: EmailMessageDTO) -> int:
        sent_count = 0
        for message in messages:
            await self._write_message(message)
            sent_count += 1
        return sent_count
