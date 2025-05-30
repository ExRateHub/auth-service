from __future__ import annotations

from dataclasses import dataclass

from litestar.contrib.jinja import JinjaTemplateEngine


@dataclass(frozen=True)
class EmailMessage:
    to_email: str
    subject: str
    body: str

    @classmethod
    def from_template(cls,to_email: str, subject: str, template_name: str, context: dict[str, str] | None = None) -> EmailMessage:
        context = {} if context is None else context

        JinjaTemplateEngine()

