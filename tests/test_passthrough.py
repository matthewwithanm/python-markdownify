from io import StringIO
import re

from bs4 import BeautifulSoup
import pytest

from markdownify import ATX, MarkdownConverter, markdownify
from markdownify.main import main


def test_iframe_keeps_attributes_entities_and_neighbors():
    iframe = '<iframe allowfullscreen="" src="https://example.com/?a=1&amp;b=2"></iframe>'
    assert markdownify('<h1>Video</h1>' + iframe + '<p><em>Caption</em></p>',
                       passthrough=['iframe']) == 'Video\n=====\n\n' + iframe + '\n\n*Caption*'


@pytest.mark.parametrize('selector', [['foo'], ('FOO',), 'foo', {'foo'}])
def test_custom_tag_in_list(selector):
    assert markdownify('<ul><li><foo>bar</foo></li></ul>',
                       passthrough=selector) == '* <foo>bar</foo>'


def test_preserved_subtree_is_not_converted_or_escaped():
    html = '<custom-tag><!--keep-->\n <b>*a_b*</b> &amp; <br/>\n</custom-tag>'
    expected = '<custom-tag><!--keep-->\n<b>*a_b*</b> &amp; <br/>\n</custom-tag>'
    assert markdownify(html, passthrough=['custom-tag'], escape_misc=True) == expected


def test_callback_selects_attributes_without_tag_name_cache():
    html = '<span custom-style="MyStyle">a</span> <span>b</span> <span id="keep-2">c</span>'

    def select(el):
        return (el.name == 'span'
                and (el.has_attr('custom-style')
                     or re.match(r'keep-\d+$', el.get('id', ''))))
    assert markdownify(html, passthrough=select) == (
        '<span custom-style="MyStyle">a</span> b <span id="keep-2">c</span>')


def test_selected_parent_does_not_visit_children_or_custom_converters():
    seen = []

    class Converter(MarkdownConverter):
        def convert_b(self, el, text, parent_tags):
            raise AssertionError('selected descendants must not be converted')

    def select(el):
        seen.append(el.name)
        return el.name == 'div'
    converter = Converter(passthrough=select)
    assert converter.convert('<div><b>inside</b></div>') == '<div><b>inside</b></div>'
    assert seen == ['div']


@pytest.mark.parametrize('options', [{'strip': ['b']}, {'convert': ['i']}])
def test_passthrough_overrides_strip_and_convert(options):
    assert markdownify('<b>keep</b><i>convert</i>', passthrough=['b'],
                       **options) == '<b>keep</b>*convert*'


def test_passthrough_overrides_selected_custom_converter():
    class Converter(MarkdownConverter):
        def convert_iframe(self, el, text, parent_tags):
            return 'custom'
    converter = Converter(passthrough=['iframe'])
    assert converter.convert('<iframe></iframe>') == '<iframe></iframe>'


def test_callback_exceptions_propagate_and_reuse_has_no_state():
    error = RuntimeError('predicate failed')

    def select(el):
        if el.get('id') == 'bad':
            raise error
        return el.name == 'foo'
    converter = MarkdownConverter(passthrough=select)
    with pytest.raises(RuntimeError) as caught:
        converter.convert('<foo id="bad">text</foo>')
    assert caught.value is error
    assert converter.convert('<foo>good</foo>') == '<foo>good</foo>'


def test_soup_is_not_mutated_and_generator_option_is_reusable():
    soup = BeautifulSoup('<div><foo>one</foo><b>two</b></div>', 'html.parser')
    before = str(soup)
    converter = MarkdownConverter(passthrough=(tag for tag in ['foo']))
    assert converter.convert_soup(soup) == '<foo>one</foo>**two**'
    assert converter.convert_soup(soup) == '<foo>one</foo>**two**'
    assert str(soup) == before
    assert type(converter.convert_soup(soup)) is str
    assert converter.convert_soup(soup.foo) == '<foo>one</foo>'


def test_paragraph_containing_raw_html_is_not_rewrapped():
    raw = '<span title="many   words">inside   words\nnext</span>'
    html = '<p>before ' + raw + ' after</p><p>one two three four</p>'
    assert markdownify(html, passthrough=['span'], wrap=True, wrap_width=8) == (
        'before ' + raw + ' after\n\none two\nthree\nfour')


def test_normalization_does_not_change_preserved_attributes_in_heading_and_term():
    raw = '<span title="many   words">a\nb</span>'
    for html, prefix in [('<h3>' + raw + '</h3>', '### '),
                         ('<dl><dt>' + raw + '</dt></dl>', '')]:
        assert markdownify(html, passthrough=['span'], heading_style=ATX) == prefix + raw


def test_raw_html_in_code_uses_actual_backticks_to_choose_delimiter():
    assert markdownify('<code><foo>`x`</foo></code>', passthrough=['foo']) == (
        '`` <foo>`x`</foo> ``')


def test_multiline_raw_subtree_keeps_list_and_blockquote_indentation():
    raw = '<foo>one\ntwo</foo>'
    assert markdownify('<ul><li>' + raw + '</li></ul>', passthrough=['foo']) == (
        '* <foo>one\n  two</foo>')
    assert markdownify('<blockquote>' + raw + '</blockquote>', passthrough=['foo']) == (
        '> <foo>one\n> two</foo>')


def test_raw_block_keeps_separation_and_nested_html():
    raw = '<div><p><b>inside</b></p></div>'
    assert markdownify('before' + raw + 'after', passthrough=['div']) == (
        'before\n\n' + raw + '\n\nafter')


def test_whole_table_is_preserved():
    html = '<table>\n<tr><td><b>A</b></td><td>B</td></tr>\n</table>'
    assert markdownify(html, passthrough=['table']) == html


def test_inline_raw_html_survives_table_conversion():
    html = '<table><tr><th><span title="a   b">c</span></th></tr></table>'
    assert markdownify(html, passthrough=['span']) == (
        '| <span title="a   b">c</span> |\n| --- |')


@pytest.mark.parametrize('value', [True, 1, [1], b'iframe'])
def test_invalid_selector_has_clear_error(value):
    with pytest.raises(TypeError, match='passthrough'):
        MarkdownConverter(passthrough=value)


def test_cli_passthrough(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('<iframe src="video"></iframe>'))
    # main's parser reads sys.stdin at invocation time.
    main(['--passthrough', 'iframe'])
    assert capsys.readouterr().out == '<iframe src="video"></iframe>\n'


def test_disabled_option_keeps_existing_output():
    html = '<p><foo><b>bold</b></foo></p>'
    for option in (None, [], lambda el: False):
        assert markdownify(html, passthrough=option) == '**bold**'
