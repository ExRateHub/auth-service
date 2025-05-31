from typing import Any

import pytest

from application.factory.email_message import TemplateEmailMessageFactory
from application.ports.template_engine import BaseTemplateEngine


class TestTemplateEmailMessageFactory:
    @pytest.fixture
    def template_engine(self) -> BaseTemplateEngine:
        class DummyTemplateEngine(BaseTemplateEngine):
            def render(self, template_name: str, context: dict[str, Any]) -> str:
                return f"Rendered {template_name} with {context}"

        return DummyTemplateEngine()

    def test_build_single_template(self, template_engine: BaseTemplateEngine) -> None:
        factory = TemplateEmailMessageFactory(template_engine=template_engine)

        to_email = "test@example.com"
        subject = "Hello"
        templates = ["welcome.txt"]
        context = {"user": "Alice"}

        message = factory.build(to_email, subject, templates, context)

        assert message.to_email == to_email
        assert message.subject == subject
        assert message.content.type == "text/plain"
        assert "Rendered welcome.txt" in message.content.body
        assert message.alternative_contents == []

    def test_build_multiple_templates(self, template_engine: BaseTemplateEngine) -> None:
        factory = TemplateEmailMessageFactory(template_engine=template_engine)

        to_email = "test@example.com"
        subject = "Greetings"
        templates = ["main.html", "alt.txt"]
        context = {"name": "Bob"}

        message = factory.build(to_email, subject, templates, context)

        assert message.to_email == to_email
        assert message.subject == subject

        # First content corresponds to main.html
        assert message.content.type == "text/html"
        assert "Rendered main.html" in message.content.body

        # Alternative contents include alt.txt
        assert len(message.alternative_contents) == 1
        alt = message.alternative_contents[0]
        assert alt.type == "text/plain"
        assert "Rendered alt.txt" in alt.body

    def test_build_empty_template_names_raises(self, template_engine: BaseTemplateEngine) -> None:
        factory = TemplateEmailMessageFactory(template_engine=template_engine)

        with pytest.raises(ValueError, match="Template Names should contain at least one element"):
            factory.build("a@b.com", "Subj", [], {})

    def test_get_message_content_type_invalid(self, template_engine: BaseTemplateEngine) -> None:
        factory = TemplateEmailMessageFactory(template_engine=template_engine)

        to_email = "test@example.com"
        subject = "Greetings"
        templates = ["main.invalid", "alt.txt"]
        context = {"name": "Bob"}

        with pytest.raises(ValueError):
            factory.build(to_email, subject, templates, context)
