# ruff: noqa: F821

from markdown2 import markdown
from render_engine_parser import BasePageParser

__all__ = ["BasePageParser"]


class MarkdownPageParser(BasePageParser):
    """
    Uses the Base Parse to frontmatter parser the attrs
    Markdown2 then parses the content
    """

    @staticmethod
    def parse(content: str, extras: dict[str, any] | None = None) -> str:
        """Parses the content with the parser"""
        return markdown(
            content,
            extras=extras.get("markdown_extras", []) if extras else [],
        )
