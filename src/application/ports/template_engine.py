from abc import ABC, abstractmethod
from typing import Any


class BaseTemplateEngine(ABC):
    @abstractmethod
    def render(self, template_name: str, context: dict[str, Any]) -> str:
        """
        Render a template with the given context.

        :param template_name: The name of the template to render.
        :type template_name: str
        :param context: A dictionary containing context data for rendering the template.
        :type context: dict[str, Any]
        :return: The rendered template as a string.
        :rtype: str
        """
