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


def test_code_with_tricky_content():
    assert md('<code>></code>') == "`>`"
    assert md('<code>/home/</code><b>username</b>') == "`/home/`**username**"
    assert md('First line <code>blah blah<br />blah blah</code> second line') \
        == "First line `blah blah  \nblah blah` second line"


def test_special_tags():
    assert md('<!DOCTYPE html>') == ''
    assert md('<![CDATA[foobar]]>') == 'foobar'


def test_cyclic_tree_does_not_recurse():
    """A cyclic BeautifulSoup tree (a descendant referencing an ancestor, as
    some PDF-to-HTML pipelines can produce) must not send process_tag /
    process_element into unbounded recursion. Regression test for #256."""
    import sys
    from bs4 import BeautifulSoup
    from markdownify import MarkdownConverter

    soup = BeautifulSoup('<div><p>hello</p></div>', 'html.parser')
    div = soup.find('div')
    p = soup.find('p')
    # Introduce a cycle: p now contains div, which already contains p.
    p.contents.append(div)

    original_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(300)
    try:
        # Must complete without raising RecursionError.
        result = MarkdownConverter().convert_soup(soup)
    finally:
        sys.setrecursionlimit(original_limit)
    assert 'hello' in result
