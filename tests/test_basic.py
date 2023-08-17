from markdownify import markdownify as md


def test_single_tag():
    assert md('<span>Hello</span>') == 'Hello'


def test_soup():
    assert md('<div><span>Hello</div></span>') == 'Hello'


def test_whitespace():
    assert md(' a  b \t\t c ') == ' a b c '


def test_style_sheet():
    assert md('<!DOCTYPE html><html><head><style>body {background-color: powderblue;}h1 {color: blue;}p {color: red;}</style></head><body><p>This is text</p></body></html>') == 'This is text\n\n'
