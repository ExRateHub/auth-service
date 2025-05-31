from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from email.message import EmailMessage

import aiosmtplib

from application.dto.email_message import EmailMessageDTO
from application.ports.email_sender import EmailSender
from core.config import EmailSettings, EmailSMTPConfig


@dataclass
class SMTPEmailSender(EmailSender):
    name: str = field(default="smtp", init=False)

    host: str
    port: int
    username: str
    password: str
    use_tls: bool
    use_ssl: bool

    from_email: str
    from_name: str | None = field(default=None, kw_only=True)

    def __post_init__(self) -> None:
        self._lock = asyncio.Lock()
        self._smtp_client = aiosmtplib.SMTP(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            use_tls=self.use_tls,
        )

    @classmethod
    def from_email_settings(cls, email_settings: EmailSettings) -> SMTPEmailSender:
        if not isinstance(email_settings.config, EmailSMTPConfig):
            raise TypeError("email_settings.config must be an instance of EmailSMTPConfig")

        sender = SMTPEmailSender(
            host=email_settings.config.host,
            port=email_settings.config.port,
            username=email_settings.config.username,
            password=email_settings.config.password,
            use_tls=email_settings.config.use_tls,
            use_ssl=email_settings.config.use_ssl,
            from_email=email_settings.from_email,
            from_name=email_settings.from_name,
        )
        return sender

    async def send_messages(self, *messages: EmailMessageDTO) -> int:

        sent_count = 0
        async with self._lock:
            async with self._smtp_client as client:
                for message in messages:
                    email_message = EmailMessage()
                    email_message["From"] = f"{self.from_name} <{self.from_email}>" if self.from_name else self.from_email
                    email_message["To"] = message.to_email
                    email_message["Subject"] = message.subject
                    maintype, subtype = message.content.type.split("/")
                    email_message.set_content(message.content.body, subtype=subtype)
                    for alternative_content in message.alternative_contents:
                        maintype, subtype = alternative_content.type.split("/")
                        email_message.add_alternative(alternative_content.body, subtype=subtype)
                    try:
                        await client.send_message(email_message)
                    except Exception:
                        continue
                    sent_count += 1

        return sent_count
