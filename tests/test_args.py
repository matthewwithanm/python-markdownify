"""
Test whitelisting/blacklisting of specific tags.

"""
from markdownify import markdownify as md, LSTRIP, RSTRIP, STRIP


def test_strip():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', strip=['a'])
    assert text == 'Some Text'


def test_do_not_strip():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', strip=[])
    assert text == '[Some Text](https://github.com/matthewwithanm)'


def test_convert():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', convert=['a'])
    assert text == '[Some Text](https://github.com/matthewwithanm)'


def test_do_not_convert():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', convert=[])
    assert text == 'Some Text'


def test_strip_document():
    assert md("<p>Hello</p>") == "Hello\n\n"  # defaults to LSTRIP
    assert md("<p>Hello</p>", strip_document=LSTRIP) == "Hello\n\n"
    assert md("<p>Hello</p>", strip_document=RSTRIP) == "\n\nHello"
    assert md("<p>Hello</p>", strip_document=STRIP) == "Hello"
    assert md("<p>Hello</p>", strip_document=None) == "\n\nHello\n\n"
