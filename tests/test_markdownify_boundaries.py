import pytest
from markdownify import markdownify as md

def test_empty_string_returns_empty_markdown():
    out = md("")
    assert out == ""

def test_plain_text_without_html_returns_as_is():
    s = "just plain text"
    assert md(s) == s

def test_unknown_tag_text_preserved():
    html = "<custom>Hi</custom>"
    out = md(html)
    assert "Hi" in out

def test_link_without_href_falls_back_to_text():
    html = '<a>Just text</a>'
    out = md(html)
    assert "Just text" in out and "[" not in out

def test_none_raises_type_error():
    with pytest.raises((TypeError, AttributeError)):
        md(None)
