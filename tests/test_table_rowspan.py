import pytest
from bs4 import BeautifulSoup

from markdownify import MarkdownConverter, markdownify


def test_rowspan_keeps_following_cells_in_their_columns():
    html = '''<table><tr><th>A</th><th>B</th><th>C</th></tr>
        <tr><td rowspan="3"><b>one</b></td><td>two</td><td rowspan="2">three</td></tr>
        <tr><td>four</td></tr><tr><td>five</td><td>six</td></tr></table>'''
    assert markdownify(html) == (
        '| A | B | C |\n| --- | --- | --- |\n'
        '| **one** | two | three |\n|  | four |  |\n|  | five | six |'
    )


def test_rowspan_and_colspan():
    html = '''<table><tr><td rowspan="2" colspan="2">one</td><td>two</td></tr>
        <tr><td><a href="/three">three</a></td></tr></table>'''
    assert markdownify(html, table_infer_header=True) == (
        '| one | | two |\n| --- | --- | --- |\n|  |  | [three](/three) |'
    )


@pytest.mark.parametrize('span', ['0', '99', '65534'])
def test_rowspan_stops_at_the_row_group(span):
    html = '''<table><thead><tr><th>A</th><th>B</th></tr></thead>
        <tbody><tr><td rowspan="%s">one</td><td>two</td></tr>
        <tr><td>three</td></tr></tbody>
        <tbody><tr><td>four</td><td>five</td></tr></tbody></table>''' % span
    output = markdownify(html)
    assert '|  | three |' in output
    assert '| four | five |' in output
    assert output.count('three') == 1


@pytest.mark.parametrize('span', ['-1', 'undefined', '', '1.5'])
def test_invalid_rowspan_is_ignored(span):
    html = '<table><tr><td rowspan="%s">one</td></tr><tr><td>two</td></tr></table>' % span
    assert markdownify(html) == '|  |\n| --- |\n| one |\n| two |'


def test_rowspan_fills_an_empty_row():
    html = '<table><tr><td rowspan="2">one</td></tr><tr></tr></table>'
    assert markdownify(html) == '|  |\n| --- |\n| one |\n|  |'


def test_rowspan_does_not_change_the_callers_soup_or_leak_between_tables():
    html = '<table><tr><td rowspan="2">one</td><td>two</td></tr><tr><td>three</td></tr></table>'
    soup = BeautifulSoup(html, 'html.parser')
    original = str(soup)
    converter = MarkdownConverter()
    first = converter.convert_soup(soup)
    assert '|  | three |' in first
    assert converter.convert_soup(soup) == first
    assert str(soup) == original
    assert converter.convert('<table><tr><td>next</td></tr></table>') == '|  |\n| --- |\n| next |'


def test_nested_tables_have_independent_rowspans():
    inner = '<table><tr><td rowspan="2">inner</td><td>x</td></tr><tr><td>y</td></tr></table>'
    html = '<table><tr><td rowspan="2">outer</td><td>%s</td></tr><tr><td>end</td></tr></table>' % inner
    output = markdownify(html)
    assert '|  | end |' in output
    assert '|  | y |' in output
    assert output.count('outer') == 1
    assert output.count('inner') == 1


def test_rowspan_preserves_custom_cell_conversion():
    class Converter(MarkdownConverter):
        def convert_td(self, el, text, parent_tags):
            return super().convert_td(el, text.upper(), parent_tags)

    html = '<table><tr><td rowspan="2">one</td><td>two</td></tr><tr><td>three</td></tr></table>'
    assert '| ONE | TWO |\n|  | THREE |' in Converter().convert(html)
