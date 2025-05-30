from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

from application.dto.email_message import EmailMessageDTO
from application.ports.template_engine import BaseTemplateEngine


@dataclass()
class EmailSender(ABC):
    name: str
    template_engine: BaseTemplateEngine

    @abstractmethod
    async def send_messages(self, messages: Sequence[EmailMessageDTO]) -> int:
        """
        Sends a sequence of email messages asynchronously.

        :param messages: Sequence of EmailMessage instances to be sent.
        :return: Number of messages successfully sent.
        """
