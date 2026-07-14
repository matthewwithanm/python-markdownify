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
# Rowspan test tables
table_with_simple_rowspan = """<table>
    <tr>
        <th>Name</th>
        <th>Department</th>
        <th>Age</th>
    </tr>
    <tr>
        <td rowspan="2">John</td>
        <td>IT</td>
        <td>30</td>
    </tr>
    <tr>
        <td>Management</td>
        <td>31</td>
    </tr>
    <tr>
        <td>Jane</td>
        <td>HR</td>
        <td>28</td>
    </tr>
</table>"""

table_with_complex_rowspan = """<table>
    <tr>
        <th>Category</th>
        <th>Item</th>
        <th>Price</th>
        <th>Stock</th>
    </tr>
    <tr>
        <td rowspan="3">Electronics</td>
        <td>Phone</td>
        <td>$500</td>
        <td>10</td>
    </tr>
    <tr>
        <td>Laptop</td>
        <td>$1000</td>
        <td>5</td>
    </tr>
    <tr>
        <td>Tablet</td>
        <td>$300</td>
        <td>8</td>
    </tr>
    <tr>
        <td>Books</td>
        <td>Novel</td>
        <td>$15</td>
        <td>20</td>
    </tr>
</table>"""

table_with_rowspan_and_colspan = """<table>
    <tr>
        <th colspan="2">Product Info</th>
        <th>Details</th>
    </tr>
    <tr>
        <td rowspan="2">Electronics</td>
        <td>Phone</td>
        <td>Latest model</td>
    </tr>
    <tr>
        <td>Laptop</td>
        <td>High performance</td>
    </tr>
</table>"""

table_with_multiple_rowspan = """<table>
    <tr>
        <th>Region</th>
        <th>Country</th>
        <th>City</th>
        <th>Population</th>
    </tr>
    <tr>
        <td rowspan="2">Asia</td>
        <td rowspan="2">China</td>
        <td>Beijing</td>
        <td>21M</td>
    </tr>
    <tr>
        <td>Shanghai</td>
        <td>24M</td>
    </tr>
    <tr>
        <td rowspan="1">Europe</td>
        <td>France</td>
        <td>Paris</td>
        <td>2M</td>
    </tr>
</table>"""

table_with_thead_rowspan = """<table>
    <thead>
        <tr>
            <th rowspan="2">Name</th>
            <th colspan="2">Contact</th>
        </tr>
        <tr>
            <th>Email</th>
            <th>Phone</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>John</td>
            <td>john@example.com</td>
            <td>123-456</td>
        </tr>
    </tbody>
</table>"""


def test_table():
    assert md(table) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(
        table_with_html_content) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| **Jill** | *Smith* | [50](#) |\n| Eve | Jackson | 94 |\n\n'
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
    assert md(
        table_with_undefined_colspan) == '\n\n| Name | Age |\n| --- | --- |\n| Jill | Smith |\n\n'
    assert md(table_with_colspan_missing_head) == '\n\n|  |  |  |\n| --- | --- | --- |\n| Name | | Age |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_simple_rowspan) == '\n\n| Name | Department | Age |\n| --- | --- | --- |\n| John | IT | 30 |\n|  | Management | 31 |\n| Jane | HR | 28 |\n\n'
    assert md(table_with_complex_rowspan) == '\n\n| Category | Item | Price | Stock |\n| --- | --- | --- | --- |\n| Electronics | Phone | $500 | 10 |\n|  | Laptop | $1000 | 5 |\n|  | Tablet | $300 | 8 |\n| Books | Novel | $15 | 20 |\n\n'
    assert md(table_with_rowspan_and_colspan) == '\n\n| Product Info | | Details |\n| --- | --- | --- |\n| Electronics | Phone | Latest model |\n|  | Laptop | High performance |\n\n'
    assert md(table_with_multiple_rowspan) == '\n\n| Region | Country | City | Population |\n| --- | --- | --- | --- |\n| Asia | China | Beijing | 21M |\n|  |  | Shanghai | 24M |\n| Europe | France | Paris | 2M |\n\n'
    assert md(table_with_thead_rowspan) == '\n\n| Name | Contact | |\n| --- | --- | --- |\n|  | Email | Phone |\n| John | john@example.com | 123-456 |\n\n'


def test_table_infer_header():
    assert md(table, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_html_content,
              table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| **Jill** | *Smith* | [50](#) |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_paragraphs, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_linebreaks, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith Jackson | 50 |\n| Eve | Jackson Smith | 94 |\n\n'
    assert md(table_with_header_column,
              table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_head_body, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_head_body_multiple_head, table_infer_header=True) == '\n\n| Creator | Editor | Server |\n| --- | --- | --- |\n| Operator | Manager | Engineer |\n| Bob | Oliver | Tom |\n| Thomas | Lucas | Ethan |\n\n'
    assert md(table_head_body_missing_head,
              table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_missing_text, table_infer_header=True) == '\n\n|  | Lastname | Age |\n| --- | --- | --- |\n| Jill |  | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_missing_head, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_body, table_infer_header=True) == '\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_caption,
              table_infer_header=True) == 'TEXT\n\nCaption\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n\n'
    assert md(table_with_colspan, table_infer_header=True) == '\n\n| Name | | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_undefined_colspan,
              table_infer_header=True) == '\n\n| Name | Age |\n| --- | --- |\n| Jill | Smith |\n\n'
    assert md(table_with_colspan_missing_head,
              table_infer_header=True) == '\n\n| Name | | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n'
    assert md(table_with_simple_rowspan,
              table_infer_header=True) == '\n\n| Name | Department | Age |\n| --- | --- | --- |\n| John | IT | 30 |\n|  | Management | 31 |\n| Jane | HR | 28 |\n\n'
    assert md(table_with_complex_rowspan, table_infer_header=True) == '\n\n| Category | Item | Price | Stock |\n| --- | --- | --- | --- |\n| Electronics | Phone | $500 | 10 |\n|  | Laptop | $1000 | 5 |\n|  | Tablet | $300 | 8 |\n| Books | Novel | $15 | 20 |\n\n'
    assert md(table_with_rowspan_and_colspan,
              table_infer_header=True) == '\n\n| Product Info | | Details |\n| --- | --- | --- |\n| Electronics | Phone | Latest model |\n|  | Laptop | High performance |\n\n'
    assert md(table_with_multiple_rowspan, table_infer_header=True) == '\n\n| Region | Country | City | Population |\n| --- | --- | --- | --- |\n| Asia | China | Beijing | 21M |\n|  |  | Shanghai | 24M |\n| Europe | France | Paris | 2M |\n\n'
    assert md(table_with_thead_rowspan,
              table_infer_header=True) == '\n\n| Name | Contact | |\n| --- | --- | --- |\n|  | Email | Phone |\n| John | john@example.com | 123-456 |\n\n'
