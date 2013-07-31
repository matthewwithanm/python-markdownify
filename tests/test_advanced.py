from markdownify import markdownify as md


def test_nested():
    text = md('<p>This is an <a href="http://example.com/">example link</a>.</p>')
    assert text == 'This is an [example link](http://example.com/).\n\n'
