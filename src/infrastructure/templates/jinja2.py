from dataclasses import dataclass
from typing import Any

from jinja2 import Environment, FileSystemLoader

from application.ports.template_engine import BaseTemplateEngine
from core.config import Settings


def get_jinja2_environment_from_settings(settings: Settings) -> Environment:
    """
    Creates and returns a Jinja2 Environment configured with the template directory specified in the settings.

    :param settings: An instance containing configuration settings, including the path to email templates.
    :type settings: Settings

    :returns: A Jinja2 Environment object with the FileSystemLoader set to the templates directory.
    :rtype: Environment
    """
    environment = Environment(
        loader=FileSystemLoader(settings.email.templates_dir),
    )
    return environment


@dataclass
class Jinja2TemplateEngine(BaseTemplateEngine):
    """Template engine uses Jinja2"""

    environment: Environment

    def render(self, template_name: str, context: dict[str, Any]) -> str:
        """
        Render the given template file with provided context.
        :param template_name: filename including extension (e.g., 'confirm_email.html')
        :param context: mapping of variables for template rendering
        :return: template rendered as string
        """
        template = self.environment.get_template(template_name)
        return template.render(**context)
