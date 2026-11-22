import io

from bs4 import BeautifulSoup

from markdownify import MarkdownConverter, markdownify
from markdownify.main import main


def test_decompose_suppresses_content_and_descendant_converters():
    class GuardConverter(MarkdownConverter):
        def convert_b(self, el, text, parent_tags):
            raise AssertionError('Excluded subtree was visited')

    html = '<p>Hello</p><aside><b>Noise</b></aside><p>World</p>'
    assert GuardConverter(decompose=['aside']).convert(html) == 'Hello\n\nWorld'


def test_decompose_takes_precedence_over_strip_and_convert():
    html = '<script>alert(1)</script><noscript>Noise</noscript><p>Keep</p>'
    assert markdownify(html, decompose=['script', 'noscript'], strip=['script']) == 'Keep'
    assert markdownify(html, decompose=['noscript'], convert=['p']) == 'alert(1)\n\nKeep\n\n'


def test_decompose_works_with_root_tags_without_mutating_soup():
    soup = BeautifulSoup('<aside><p>Noise</p></aside>', 'html.parser')
    original = str(soup)
    converter = MarkdownConverter(decompose=['aside'])
    assert converter.convert_soup(soup.aside) == ''
    assert str(soup) == original


def test_decompose_preserves_default_and_inline_boundaries():
    html = '<p>before <span>noise</span> after</p>'
    assert markdownify(html) == 'before noise after'
    assert markdownify(html, decompose=[]) == 'before noise after'
    assert markdownify(html, decompose=['span']) == 'before  after'


def test_decompose_cli(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('<p>Keep</p><aside>Noise</aside>'))
    main(['--decompose', 'aside'])
    assert capsys.readouterr().out == 'Keep\n'
