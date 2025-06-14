from abc import ABC, abstractmethod
from dataclasses import dataclass

from application.dto.email_message import EmailMessageDTO


@dataclass()
class EmailSender(ABC):
    name: str

    @abstractmethod
    async def send_messages(self, *messages: EmailMessageDTO) -> int:
        """
        Sends a sequence of email messages asynchronously.

        :param messages: Sequence of EmailMessage instances to be sent.
        :return: Number of messages successfully sent.
        """
