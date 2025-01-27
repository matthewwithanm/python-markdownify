from .utils import md


def test_single_tag():
    assert md('<span>Hello</span>') == 'Hello'


def test_soup():
    assert md('<div><span>Hello</div></span>') == 'Hello'


def test_whitespace():
    assert md(' a  b \t\t c ') == ' a b c '
    assert md(' a  b \n\n c ') == ' a b\nc '
