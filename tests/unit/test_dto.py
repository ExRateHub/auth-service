from typing import Sequence

from application.dto.email_message import EmailMessageContent, EmailMessageDTO


class TestEmailMessageContentDTO:
    def test_email_message_content_creation(self) -> None:
        content = EmailMessageContent(type="text/plain", body="Hello")
        assert content.type == "text/plain"
        assert content.body == "Hello"


class TestEmailMessageDTO:
    def test_email_message_creation(self) -> None:
        main_content = EmailMessageContent(type="text/plain", body="Main body")
        alt_content1 = EmailMessageContent(type="text/html", body="<p>Alt1</p>")
        alt_content2 = EmailMessageContent(type="text/plain", body="Alt2")

        email = EmailMessageDTO(
            to_email="user@example.com",
            subject="Test Subject",
            content=main_content,
            alternative_contents=[alt_content1, alt_content2],
        )

        assert email.to_email == "user@example.com"
        assert email.subject == "Test Subject"
        assert email.content == main_content
        assert isinstance(email.alternative_contents, Sequence)
        assert len(email.alternative_contents) == 2
        assert email.alternative_contents[0].type == "text/html"

    def test_email_message_content_type_validation(self) -> None:
        # Since type is a Literal, static type checkers enforce it,
        # but runtime does not raise error automatically.
        # This test demonstrates that invalid types are accepted at runtime,
        # so validation should be done elsewhere if needed.
        content = EmailMessageContent(type="invalid/type", body="Body")
        assert content.type == "invalid/type"
