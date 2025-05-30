import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from infrastructure.templates.jinja import JinjaTemplateEngine


@pytest.mark.usefixtures("tmp_templates_dir")
class TestJinjaTemplateEngine:
    @pytest.fixture(autouse=True)
    def tmp_templates_dir(self) -> Generator[Path, None, None]:
        tmp = Path(tempfile.mkdtemp())
        yield tmp
        shutil.rmtree(str(tmp))

    def test_render_txt(self, tmp_templates_dir: Path):
        template_name = tmp_templates_dir / "hello.txt"
        template_name.write_text("Hello, {{ name }}!", encoding="utf-8")

        environment = Environment(loader=FileSystemLoader(tmp_templates_dir))
        engine = JinjaTemplateEngine(environment)
        result = engine.render("hello.txt", {"name": "World"})

        assert result == "Hello, World!"

    def test_render_html(self, tmp_templates_dir: Path):
        template_name = tmp_templates_dir / "page.html"
        template_name.write_text("<h1>{{ title }}</h1>", encoding="utf-8")

        environment = Environment(loader=FileSystemLoader(tmp_templates_dir))
        engine = JinjaTemplateEngine(environment)
        result = engine.render("page.html", {"title": "Welcome"})

        assert result.strip() == "<h1>Welcome</h1>"

    def test_missing_template_raises(self, tmp_templates_dir):
        environment = Environment(loader=FileSystemLoader(tmp_templates_dir))
        engine = JinjaTemplateEngine(environment)
        with pytest.raises(TemplateNotFound):
            engine.render("no_such.template_name", {})
