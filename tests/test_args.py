"""
Test whitelisting/blacklisting of specific tags.

"""
import time

import pytest

from markdownify import markdownify, LSTRIP, RSTRIP, STRIP, STRIP_ONE
from .utils import md


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
    assert markdownify("<p>Hello</p>") == "Hello"  # test default of STRIP
    assert markdownify("<p>Hello</p>", strip_document=LSTRIP) == "Hello\n\n"
    assert markdownify("<p>Hello</p>", strip_document=RSTRIP) == "\n\nHello"
    assert markdownify("<p>Hello</p>", strip_document=STRIP) == "Hello"
    assert markdownify("<p>Hello</p>", strip_document=None) == "\n\nHello\n\n"


def test_strip_pre():
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>") == "```\n  Hello\n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=STRIP) == "```\n  Hello\n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=STRIP_ONE) == "```\n  \n  Hello  \n  \n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=None) == "```\n  \n  \n  Hello  \n  \n  \n```"


def bs4_options():
    assert markdownify("<p>Hello</p>", bs4_options="html.parser") == "Hello"
    assert markdownify("<p>Hello</p>", bs4_options=["html.parser"]) == "Hello"
    assert markdownify("<p>Hello</p>", bs4_options={"features": "html.parser"}) == "Hello"


@pytest.mark.parametrize('text, expected', [
    ('  indented', '  indented'), ('x  ', 'x'), ('x \n ', 'x'),
    ('', ''), ('  \n  ', ''), ('\tx\t', '\tx\t'),
    ('x\r', 'x\r'), ('x\v', 'x\v'), ('x\u00a0', 'x\u00a0'),
    ('  \n  x  \n  ', '  x'),
])
def test_strip_pre_whitespace_semantics(text, expected):
    expected_markdown = '```\n' + expected + '\n```' if text else ''
    assert markdownify('<pre>' + text + '</pre>') == expected_markdown


def test_strip_pre_long_indentation():
    # A space run followed by text must not restart a trailing-whitespace
    # search at every position. The linear implementation takes milliseconds;
    # this generous limit catches the quadratic regression.
    text = ' ' * 65536 + 'x'
    start = time.monotonic()
    result = markdownify('<pre>' + text + '</pre>')
    elapsed = time.monotonic() - start
    assert result == '```\n' + text + '\n```'
    assert elapsed < 5
