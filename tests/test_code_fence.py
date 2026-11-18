import pytest

from markdownify import MarkdownConverter, STRIP, STRIP_ONE, markdownify


@pytest.mark.parametrize('fence', ['```', '~~~', '````', '~~~~'])
def test_code_fence(fence):
    assert markdownify('<pre><code>hello\nworld</code></pre>', code_fence=fence) == (
        fence + '\nhello\nworld\n' + fence
    )


def test_tilde_fence_with_language():
    assert markdownify('<pre>print(1)</pre>', code_fence='~~~', code_language='python') == (
        '~~~python\nprint(1)\n~~~'
    )


def test_tilde_fence_with_language_callback():
    assert markdownify(
        '<pre class="python">print(1)</pre>',
        code_fence='~~~',
        code_language_callback=lambda el: el['class'][0],
    ) == '~~~python\nprint(1)\n~~~'


@pytest.mark.parametrize('strip_pre, content', [
    (None, '\n\nhello\n\n'),
    (STRIP, 'hello'),
    (STRIP_ONE, '\nhello'),
])
def test_tilde_fence_preserves_strip_pre(strip_pre, content):
    assert markdownify(
        '<pre>\n\nhello\n\n</pre>', code_fence='~~~', strip_pre=strip_pre,
    ) == '~~~\n' + content + '\n~~~'


def test_code_fence_subclass_option():
    class TildeConverter(MarkdownConverter):
        class Options:
            code_fence = '~~~'

    assert TildeConverter().convert('<pre>hello</pre>') == '~~~\nhello\n~~~'


def test_tilde_fence_does_not_change_inline_code_or_empty_pre():
    assert markdownify('<code>hello</code><pre></pre>', code_fence='~~~') == '`hello`'


@pytest.mark.parametrize('fence', ['', '``', '~~', '```~', '~~~\n', 'abc', None, 3])
def test_invalid_code_fence(fence):
    with pytest.raises(ValueError, match='Invalid value for code_fence'):
        MarkdownConverter(code_fence=fence)


def test_code_fence_cli(monkeypatch, capsys):
    from io import StringIO
    from markdownify.main import main

    monkeypatch.setattr('sys.stdin', StringIO('<pre>print(1)</pre>'))
    main(['--code-fence', '~~~', '--code-language', 'python'])
    assert capsys.readouterr().out == '~~~python\nprint(1)\n~~~\n'
