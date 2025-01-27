from markdownify import MarkdownConverter


def md(html, **options):
    # disable document-level stripping so separation newlines are included in testing
    options = {**options, "strip_document": None}

    return MarkdownConverter(**options).convert(html)


def test_single_tag():
    assert md('<span>Hello</span>') == 'Hello'


def test_soup():
    assert md('<div><span>Hello</div></span>') == 'Hello'


def test_whitespace():
    assert md(' a  b \t\t c ') == ' a b c '
    assert md(' a  b \n\n c ') == ' a b\nc '
