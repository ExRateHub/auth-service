import io

import pytest

from application.dto.email_message import EmailMessageContent, EmailMessageDTO
from infrastructure.email.console import ConsoleEmailSender


@pytest.mark.asyncio
class TestConsoleEmailSender:
    @pytest.fixture
    def stream(self) -> io.StringIO:
        return io.StringIO()

    @pytest.fixture
    def sender(self, stream: io.StringIO) -> ConsoleEmailSender:
        return ConsoleEmailSender(stream=stream)

    async def test_send_single(self, sender: ConsoleEmailSender, stream: io.StringIO):
        content = EmailMessageContent(type="text/plain", body="Hello")
        alt = EmailMessageContent(type="text/html", body="<p>Hello</p>")
        msg = EmailMessageDTO(
            to_email="a@b.com",
            subject="Hi",
            content=content,
            alternative_contents=[alt],
        )

        count = await sender.send_messages([msg])
        assert count == 1

        out = stream.getvalue().splitlines()
        assert "[ConsoleEmailSender] Preparing to send email" in out[0]
        assert "To: a@b.com" in out[1]
        assert "Subject: Hi" in out[2]
        assert "Alternative content-types: ['text/html']" in out[3]
        assert "Content-Type: text/plain" in out[4]
        assert "Content: Hello" in out[5]
        assert out[-1] == "=" * 60

    async def test_send_multiple(self, sender: ConsoleEmailSender, stream: io.StringIO):
        msgs = [
            EmailMessageDTO(
                to_email="x@y.com",
                subject="First",
                content=EmailMessageContent(type="text/plain", body="1"),
                alternative_contents=[],
            ),
            EmailMessageDTO(
                to_email="u@v.com",
                subject="Second",
                content=EmailMessageContent(type="text/plain", body="2"),
                alternative_contents=[],
            ),
        ]

        count = await sender.send_messages(msgs)
        assert count == 2

        text = stream.getvalue()
        assert "To: x@y.com" in text
        assert "Subject: First" in text
        assert "Content: 1" in text
        assert "To: u@v.com" in text
        assert "Subject: Second" in text
        assert "Content: 2" in text
        lines = [l for l in text.splitlines() if set(l) == {"="}]
        assert len(lines) == 2
