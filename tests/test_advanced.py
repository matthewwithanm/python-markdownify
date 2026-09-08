import pytest
from bs4 import BeautifulSoup, Comment
from markdownify import MarkdownConverter

from .utils import md


def test_chomp():
    assert md(' <b></b> ') == '  '
    assert md(' <b> </b> ') == '  '
    assert md(' <b>  </b> ') == '  '
    assert md(' <b>   </b> ') == '  '
    assert md(' <b>s </b> ') == ' **s**  '
    assert md(' <b> s</b> ') == '  **s** '
    assert md(' <b> s </b> ') == '  **s**  '
    assert md(' <b>  s  </b> ') == '  **s**  '


def test_nested():
    text = md('<p>This is an <a href="http://example.com/">example link</a>.</p>')
    assert text == '\n\nThis is an [example link](http://example.com/).\n\n'


def test_ignore_comments():
    text = md("<!-- This is a comment -->")
    assert text == ""


def test_ignore_comments_with_other_tags():
    text = md("<!-- This is a comment --><a href='http://example.com/'>example link</a>")
    assert text == "[example link](http://example.com/)"


@pytest.mark.parametrize('separator', ['\n', ' ', '\t'])
@pytest.mark.parametrize('count', [1, 2, 4])
def test_ignore_whitespace_between_comments_and_blocks(separator, count):
    comments = separator + ('<!-- comment -->' + separator) * count
    html = '<p>line 1</p>' + comments + '<p>line 2</p>'
    assert MarkdownConverter().convert(html) == 'line 1\n\nline 2'


def test_ignore_comment_whitespace_inside_block_boundaries():
    html = '<div><!-- a --> \n<!-- b --> <p>text</p> <!-- c --> \n<!-- d --></div>'
    assert md(html) == '\n\ntext\n\n'


@pytest.mark.parametrize('html, expected', [
    ('one <!-- comment --> <b>two</b>', 'one  **two**'),
    ('one<code> a <!-- comment --> b </code>two', 'one `a  b` two'),
])
def test_comment_whitespace_between_inline_content(html, expected):
    assert md(html) == expected


@pytest.mark.parametrize('code', [False, True])
def test_comment_whitespace_in_pre(code):
    content = ' a\t\n<!-- comment -->\n\n b '
    if code:
        content = '<code>' + content + '</code>'
    assert md('<pre>' + content + '</pre>', strip_pre=None) == '\n\n```\n a\t\n\n\n b \n```\n\n'


def test_comment_whitespace_conversion_preserves_soup():
    soup = BeautifulSoup('<p>one</p>\n<!-- a -->\n<!-- b -->\n<p>two</p>', 'html.parser')
    original = str(soup)
    comments = soup.find_all(string=lambda node: isinstance(node, Comment))
    positions = [(node.parent, node.previous_sibling, node.next_sibling) for node in comments]
    converter = MarkdownConverter()
    assert converter.convert_soup(soup) == 'one\n\ntwo'
    assert converter.convert_soup(soup) == 'one\n\ntwo'
    assert str(soup) == original
    for node, (parent, previous, following) in zip(comments, positions):
        assert node.parent is parent
        assert node.previous_sibling is previous
        assert node.next_sibling is following


def test_code_with_tricky_content():
    assert md('<code>></code>') == "`>`"
    assert md('<code>/home/</code><b>username</b>') == "`/home/`**username**"
    assert md('First line <code>blah blah<br />blah blah</code> second line') \
        == "First line `blah blah  \nblah blah` second line"


def test_special_tags():
    assert md('<!DOCTYPE html>') == ''
    assert md('<![CDATA[foobar]]>') == 'foobar'
