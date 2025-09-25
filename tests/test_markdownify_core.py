from markdownify import markdownify as md

def test_paragraph_and_strong_basic():
    html = "<p>Hello <strong>world</strong>!</p>"
    out = md(html)
    assert "Hello" in out
    assert "**world**" in out 

def test_h1_heading_converts_to_markdown():
    html = "<h1>Title</h1>"
    out = md(html).strip()
    lines = out.splitlines()
    atx = out.startswith("# ")
    setext = len(lines) >= 2 and lines[0].strip() == "Title" and set(lines[1].strip()) == {"="}
    assert atx or setext

def test_h3_heading_converts():
    html = "<h3>Sub</h3>"
    out = md(html)
    assert out.strip().startswith("### ")
