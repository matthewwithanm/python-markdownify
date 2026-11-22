import pytest

from markdownify import markdownify


@pytest.mark.parametrize('style', ['SPACES', 'BACKSLASH'])
@pytest.mark.parametrize('content', [
    'print(1)<br>print(2)',
    '<code>print(1)<br>print(2)</code>',
    '<span>print(1)<br>print(2)</span>',
])
def test_preformatted_breaks_are_plain_newlines(style, content):
    assert markdownify('<pre>' + content + '</pre>', newline_style=style) == (
        '```\nprint(1)\nprint(2)\n```'
    )


def test_mixed_break_forms_keep_nested_text_in_pre():
    assert markdownify('<pre>a<br>b<br />c</pre>') == '```\na\nb\nc\n```'


def test_stripped_pre_keeps_normal_break_behavior():
    assert markdownify('<pre>a<br>b</pre>', strip=['pre']) == 'a  \nb'
