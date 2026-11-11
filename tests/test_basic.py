import time

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
