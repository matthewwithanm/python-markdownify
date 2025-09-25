from markdownify import markdownify as md

import re

def test_unordered_list_multiple_items():
    html = "<ul><li>a</li><li>b</li><li>c</li></ul>"
    out = md(html)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    assert any(re.match(r"^[-*]\s+a$", ln) for ln in lines)
    assert any(re.match(r"^[-*]\s+b$", ln) for ln in lines)
    assert any(re.match(r"^[-*]\s+c$", ln) for ln in lines)

def test_ordered_list_multiple_items():
    html = "<ol><li>one</li><li>two</li></ol>"
    out = md(html)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    assert any(ln.startswith("1. ") and "one" in ln for ln in lines)
    assert any(ln.startswith("2. ") and "two" in ln for ln in lines)

def test_link_basic():
    html = '<a href="https://example.com">Example</a>'
    out = md(html)
    assert "[Example](https://example.com)" in out

def test_image_basic_alt_and_src():
    html = '<img src="https://example.com/img.png" alt="Logo" />'
    out = md(html)
    assert "![Logo]" in out and "(https://example.com/img.png)" in out 
