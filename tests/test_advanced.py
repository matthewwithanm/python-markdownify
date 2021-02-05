from markdownify import markdownify as md


def test_nested():
    text = md('<p>This is an <a href="http://example.com/">example link</a>.</p>')
    assert text == 'This is an [example link](http://example.com/).\n\n'


def test_ignore_comments():
    text = md("<!-- This is a comment -->")
    assert text == ""


def test_ignore_comments_with_other_tags():
    text = md("<!-- This is a comment --><a href='http://example.com/'>example link</a>")
    assert text == "[example link](http://example.com/)"
