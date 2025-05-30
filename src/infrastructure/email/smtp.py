from typing import Sequence

from application.dto.email_message import EmailMessageDTO
from application.ports.email_sender import EmailSender


class SMTPEmailSender(EmailSender):
    name = "smtp"

    async def send_messages(self, messages: Sequence[EmailMessageDTO]) -> int: ...
