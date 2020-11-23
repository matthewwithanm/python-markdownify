from markdownify import markdownify as md


def test_nested():
    text = md('<p>This is an <a href="http://example.com/">example link</a>.</p>')
    assert text == 'This is an [example link](http://example.com/).\n\n'


def test_code_with_tricky_content():
    assert md('<code>></code>') == "`>`"
    assert md('<code>/home/</code><b>username</b>') == "`/home/`**username**"
    # convert_br() adds trailing spaces (why?); ignore them by using 2 tests,
    assert md('<code>Line1<br />Line2</code>').startswith("`Line1")
    assert md('<code>Line1<br />Line2</code>').endswith("\nLine2`")
