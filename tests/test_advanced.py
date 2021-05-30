from markdownify import markdownify as md


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
    assert text == 'This is an [example link](http://example.com/).\n\n'


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
