import time
import pytest

from markdownify import markdownify
from .utils import md


def test_single_tag():
    assert md('<span>Hello</span>') == 'Hello'


def test_soup():
    assert md('<div><span>Hello</div></span>') == '\n\nHello\n\n'


def test_whitespace():
    assert md(' a  b \t\t c ') == ' a b c '
    assert md(' a  b \n\n c ') == ' a b\nc '


def test_long_whitespace_run():
    # A long run of spaces with no newline must not be rescanned from every
    # position while collapsing newline whitespace. The linear implementation
    # takes milliseconds; this generous limit catches the quadratic regression.
    start = time.monotonic()
    assert md('a' + ' ' * 65536 + 'b') == 'a b'
    assert time.monotonic() - start < 5


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
