import pytest
from render_engine_markdown import MarkdownPageParser


@pytest.fixture()
def markdown_content():
    return """# Test"""


def test_parser_parse_content(markdown_content):
    assert (
        MarkdownPageParser.parse(
            content=markdown_content,
        )
        == "<h1>Test</h1>\n"
    )
