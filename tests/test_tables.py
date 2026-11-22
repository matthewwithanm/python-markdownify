import pytest

from .utils import md


table = """<table>
    <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Age</th>
    </tr>
    <tr>
        <td>Jill</td>
        <td>Smith</td>
        <td>50</td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""


table_with_html_content = """<table>
    <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Age</th>
    </tr>
    <tr>
        <td><b>Jill</b></td>
        <td><i>Smith</i></td>
        <td><a href="#">50</a></td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""


table_with_paragraphs = """<table>
    <tr>
        <th>Firstname</th>
        <th><p>Lastname</p></th>
        <th>Age</th>
    </tr>
    <tr>
        <td><p>Jill</p></td>
        <td><p>Smith</p></td>
        <td><p>50</p></td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""

table_with_linebreaks = """<table>
    <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Age</th>
    </tr>
    <tr>
        <td>Jill</td>
        <td>Smith
        Jackson</td>
        <td>50</td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson
        Smith</td>
        <td>94</td>
    </tr>
</table>"""


table_with_header_column = """<table>
    <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Age</th>
    </tr>
    <tr>
        <th>Jill</th>
        <td>Smith</td>
        <td>50</td>
    </tr>
    <tr>
        <th>Eve</th>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""


table_head_body = """<table>
    <thead>
        <tr>
            <th>Firstname</th>
            <th>Lastname</th>
            <th>Age</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Jill</td>
            <td>Smith</td>
            <td>50</td>
        </tr>
        <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
        </tr>
    </tbody>
</table>"""

table_head_body_missing_head = """<table>
    <thead>
        <tr>
            <td>Firstname</td>
            <td>Lastname</td>
            <td>Age</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Jill</td>
            <td>Smith</td>
            <td>50</td>
        </tr>
        <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
        </tr>
    </tbody>
</table>"""

table_head_body_multiple_head = """<table>
    <thead>
        <tr>
            <td>Creator</td>
            <td>Editor</td>
            <td>Server</td>
        </tr>
        <tr>
            <td>Operator</td>
            <td>Manager</td>
            <td>Engineer</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Bob</td>
            <td>Oliver</td>
            <td>Tom</td>
        </tr>
        <tr>
            <td>Thomas</td>
            <td>Lucas</td>
            <td>Ethan</td>
        </tr>
    </tbody>
</table>"""

table_missing_text = """<table>
    <thead>
        <tr>
            <th></th>
            <th>Lastname</th>
            <th>Age</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Jill</td>
            <td></td>
            <td>50</td>
        </tr>
        <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
        </tr>
    </tbody>
</table>"""

table_missing_head = """<table>
    <tr>
        <td>Firstname</td>
        <td>Lastname</td>
        <td>Age</td>
    </tr>
    <tr>
        <td>Jill</td>
        <td>Smith</td>
        <td>50</td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""

table_body = """<table>
    <tbody>
        <tr>
            <td>Firstname</td>
            <td>Lastname</td>
            <td>Age</td>
        </tr>
        <tr>
            <td>Jill</td>
            <td>Smith</td>
            <td>50</td>
        </tr>
        <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
        </tr>
    </tbody>
</table>"""

table_with_caption = """TEXT<table>
    <caption>
        Caption
    </caption>
    <tbody><tr><td>Firstname</td>
            <td>Lastname</td>
            <td>Age</td>
        </tr>
    </tbody>
</table>"""

table_with_colspan = """<table>
    <tr>
        <th colspan="2">Name</th>
        <th>Age</th>
    </tr>
    <tr>
        <td colspan="1">Jill</td>
        <td>Smith</td>
        <td>50</td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""

table_with_undefined_colspan = """<table>
    <tr>
        <th colspan="undefined">Name</th>
        <th>Age</th>
    </tr>
    <tr>
        <td colspan="-1">Jill</td>
        <td>Smith</td>
    </tr>
</table>"""

table_with_colspan_missing_head = """<table>
    <tr>
        <td colspan="2">Name</td>
        <td>Age</td>
    </tr>
    <tr>
        <td>Jill</td>
        <td>Smith</td>
        <td>50</td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""


def test_table():
    assert md(table) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_html_content) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| **Jill** | *Smith* | [50](#) |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_paragraphs) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_linebreaks) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith Jackson | 50 |\n| Eve | Jackson Smith | 94 |\n\n'
    assert md(table_with_header_column) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_head_body) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_head_body_multiple_head) == '\n\n|  |  |  |\n| --- | --- | --- |\n| Creator | Editor | Server |\n| Operator | Manager | Engineer |\n| Bob | Oliver | Tom |\n| Thomas | Lucas | Ethan |\n\n'
    assert md(table_head_body_missing_head) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_missing_text) == '\n\n|  | Lastname | Age |\n| --- | --- | --- |\n| Jill |  | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_missing_head) == '\n\n|  |  |  |\n| --- | --- | --- |\n| Firstname | Lastname | Age |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_body) == '\n\n|  |  |  |\n| --- | --- | --- |\n| Firstname | Lastname | Age |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_caption) == 'TEXT\n\nCaption\n\n|  |  |  |\n| --- | --- | --- |\n| Firstname | Lastname | Age |\n\n'
    assert md(table_with_colspan) == '\n\n| Name | | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_undefined_colspan) == '\n\n| Name | Age |\n| --- | --- |\n| Jill | Smith |\n\n'
    assert md(table_with_colspan_missing_head) == '\n\n|  |  |  |\n| --- | --- | --- |\n| Name | | Age |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'


def test_table_infer_header():
    assert md(table, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_html_content, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| **Jill** | *Smith* | [50](#) |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_paragraphs, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_linebreaks, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith Jackson | 50 |\n| Eve | Jackson Smith | 94 |\n\n'
    assert md(table_with_header_column, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_head_body, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_head_body_multiple_head, table_infer_header=True) == '\n\n| Creator | Editor | Server |\n| --- | --- | --- |\n| Operator | Manager | Engineer |\n| Bob | Oliver | Tom |\n| Thomas | Lucas | Ethan |\n\n'
    assert md(table_head_body_missing_head, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_missing_text, table_infer_header=True) == '\n\n|  | Lastname | Age |\n| --- | --- | --- |\n| Jill |  | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_missing_head, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_body, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_caption, table_infer_header=True) == 'TEXT\n\nCaption\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n\n'
    assert md(table_with_colspan, table_infer_header=True) == '\n\n| Name | | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_undefined_colspan, table_infer_header=True) == '\n\n| Name | Age |\n| --- | --- |\n| Jill | Smith |\n\n'
    assert md(table_with_colspan_missing_head, table_infer_header=True) == '\n\n| Name | | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'


@pytest.mark.parametrize('colspan, width', [
    pytest.param('9' * 5000, 1000, id='oversized'),
    pytest.param('0' * 5000 + '2', 2, id='long-leading-zeros'),
    pytest.param('0' * 5000, 1, id='long-zero'),
    pytest.param('\u0660' * 5000 + '\u0662', 2, id='unicode-leading-zeros'),
    pytest.param('1000', 1000, id='maximum'),
    pytest.param('1001', 1000, id='above-maximum'),
    pytest.param('2', 2, id='ordinary'),
    pytest.param('0', 1, id='zero'),
    pytest.param('\u0662', 2, id='unicode-decimal'),
    pytest.param('\u00b2', 1, id='superscript'),
    pytest.param('\u2461', 1, id='circled-digit'),
    pytest.param('9' * 5000 + 'x', 1, id='long-invalid'),
    pytest.param('undefined', 1, id='invalid'),
])
@pytest.mark.parametrize('cell_type', ['td', 'th'])
@pytest.mark.parametrize('infer_header', [False, True])
def test_table_colspan_is_bounded_before_integer_conversion(
        colspan, width, cell_type, infer_header):
    html = ('<p>Before</p><table><tr><{cell} colspan="{span}">Value</{cell}>'
            '</tr></table><p>After</p>').format(cell=cell_type, span=colspan)
    row = '| Value' + ' |' * width
    delimiter = '| ' + ' | '.join(['---'] * width) + ' |'
    if cell_type == 'th' or infer_header:
        expected_table = row + '\n' + delimiter
    else:
        empty_header = '| ' + ' | '.join([''] * width) + ' |'
        expected_table = empty_header + '\n' + delimiter + '\n' + row

    assert md(html, table_infer_header=infer_header).strip() == (
        'Before\n\n' + expected_table + '\n\nAfter')
