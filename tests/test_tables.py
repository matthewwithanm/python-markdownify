import re

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


def test_pipes_in_cells():
    # an unescaped '|' in cell content would be parsed as a column delimiter
    assert md('<table><tr><th>A</th><th>B</th></tr><tr><td>1|2</td><td>3</td></tr></table>') == '\n\n| A | B |\n| --- | --- |\n| 1\\|2 | 3 |\n\n'
    assert md('<table><tr><th>A|B</th><th>C</th></tr><tr><td>1</td><td>2</td></tr></table>') == '\n\n| A\\|B | C |\n| --- | --- |\n| 1 | 2 |\n\n'
    assert md('<table><tr><th>A</th></tr><tr><td>1|2|3</td></tr></table>') == '\n\n| A |\n| --- |\n| 1\\|2\\|3 |\n\n'
    assert md('<table><tr><th>A</th></tr><tr><td>|</td></tr></table>') == '\n\n| A |\n| --- |\n| \\| |\n\n'
    assert md('<table><tr><th>A</th></tr><tr><td><b>1|2</b></td></tr></table>') == '\n\n| A |\n| --- |\n| **1\\|2** |\n\n'
    assert md('<table><tr><th>A</th></tr><tr><td><a href="#">1|2</a></td></tr></table>') == '\n\n| A |\n| --- |\n| [1\\|2](#) |\n\n'
    # GFM tables require pipes to be escaped even inside code spans
    assert md('<table><tr><th>A</th></tr><tr><td><code>1|2</code></td></tr></table>') == '\n\n| A |\n| --- |\n| `1\\|2` |\n\n'
    assert md('<table><tr><th>A</th><th>B</th></tr><tr><td colspan="2">1|2</td></tr></table>') == '\n\n| A | B |\n| --- | --- |\n| 1\\|2 | |\n\n'
    # escape_misc=True escapes pipes on its own; make sure they are not escaped twice
    assert md('<table><tr><th>A</th></tr><tr><td>1|2</td></tr></table>', escape_misc=True) == '\n\n| A |\n| --- |\n| 1\\|2 |\n\n'
    # pipes outside of tables are unaffected
    assert md('1|2') == '1|2'

    # every row keeps the delimiter count of a two-column table
    result = md('<table><tr><th>A|B</th><th>C</th></tr><tr><td>1|2</td><td>3|4</td></tr></table>')
    assert [len(re.findall(r'(?<!\\)\|', line)) for line in result.strip().split('\n')] == [3, 3, 3]
