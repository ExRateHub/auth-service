from dataclasses import dataclass
from typing import Any, Literal, Sequence

from application.dto.email_message import EmailMessageContent, EmailMessageDTO
from application.factory.base import BaseFactory
from application.ports.template_engine import BaseTemplateEngine


def _get_message_content_type(template_name: str) -> Literal["text/plain", "text/html"]:
    """
    Determine the content type based on the template file extension.

    :param template_name: The name of the template file.
    :return: The content type string, either "text/plain" or "text/html".
    :raises ValueError: If the template name does not end with "txt" or "html".
    """
    if template_name.endswith("txt"):
        return "text/plain"
    elif template_name.endswith("html"):
        return "text/html"
    raise ValueError("Failed to get Content Type")


@dataclass
class TemplateEmailMessageFactory(BaseFactory[EmailMessageDTO]):
    """
    Factory class to build EmailMessage instances using templates.

    :param template_engine: An instance of TemplateEngine used to render templates.
    """

    template_engine: BaseTemplateEngine

    def build(
        self,
        to_email: str,
        subject: str,
        template_names: Sequence[str],
        context: dict[str, Any],
    ) -> EmailMessageDTO:
        """
        Build an EmailMessage from one or more templates and context.

        :param to_email: Recipient email address.
        :param subject: Subject of the email.
        :param template_names: Sequence of template filenames to render.
        :param context: Context dictionary for template rendering.
        :return: An EmailMessage object with rendered content and alternatives.
        :raises ValueError: If template_names is empty.
        """
        if not template_names:
            raise ValueError("Template Names should contain at least one element")

        email_message_contents = []
        for template_name in template_names:
            body = self.template_engine.render(template_name, context)
            content_type = _get_message_content_type(template_name)
            email_message_contents.append(EmailMessageContent(type=content_type, body=body))

        content, *alternative_contents = email_message_contents
        message = EmailMessageDTO(
            to_email=to_email,
            subject=subject,
            content=content,
            alternative_contents=alternative_contents,
        )
        return message
