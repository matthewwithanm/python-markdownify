from html_to_markdown import convert_to_markdown

nested_uls = """
    <ul>
        <li>1
            <ul>
                <li>a
                    <ul>
                        <li>I</li>
                        <li>II</li>
                        <li>III</li>
                    </ul>
                </li>
                <li>b</li>
                <li>c</li>
            </ul>
        </li>
        <li>2</li>
        <li>3</li>
    </ul>"""

nested_ols = """
    <ol>
        <li>1
            <ol>
                <li>a
                    <ol>
                        <li>I</li>
                        <li>II</li>
                        <li>III</li>
                    </ol>
                </li>
                <li>b</li>
                <li>c</li>
            </ol>
        </li>
        <li>2</li>
        <li>3</li>
    </ul>"""


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

table_with_caption = """TEXT<table><caption>Caption</caption>
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


def test_single_tag() -> None:
    assert convert_to_markdown("<span>Hello</span>") == "Hello"


def test_soup() -> None:
    assert convert_to_markdown("<div><span>Hello</div></span>") == "Hello"


def test_whitespace() -> None:
    assert convert_to_markdown(" a  b \t\t c ") == " a b c "


def test_asterisks() -> None:
    assert convert_to_markdown("*hey*dude*") == r"\*hey\*dude\*"
    assert convert_to_markdown("*hey*dude*", escape_asterisks=False) == r"*hey*dude*"


def test_underscore() -> None:
    assert convert_to_markdown("_hey_dude_") == r"\_hey\_dude\_"
    assert convert_to_markdown("_hey_dude_", escape_underscores=False) == r"_hey_dude_"


def test_xml_entities() -> None:
    assert convert_to_markdown("&amp;") == r"\&"


def test_named_entities() -> None:
    assert convert_to_markdown("&raquo;") == "\xbb"


def test_hexadecimal_entities() -> None:
    # This looks to be a bug in BeautifulSoup (fixed in bs4) that we have to work around.
    assert convert_to_markdown("&#x27;") == "\x27"


def test_single_escaping_entities() -> None:
    assert convert_to_markdown("&amp;amp;") == r"\&amp;"


def text_misc() -> None:
    assert convert_to_markdown("\\*") == r"\\\*"
    assert convert_to_markdown("<foo>") == r"\<foo\>"
    assert convert_to_markdown("# foo") == r"\# foo"
    assert convert_to_markdown("> foo") == r"\> foo"
    assert convert_to_markdown("~~foo~~") == r"\~\~foo\~\~"
    assert convert_to_markdown("foo\n===\n") == "foo\n\\=\\=\\=\n"
    assert convert_to_markdown("---\n") == "\\-\\-\\-\n"
    assert convert_to_markdown("+ x\n+ y\n") == "\\+ x\n\\+ y\n"
    assert convert_to_markdown("`x`") == r"\`x\`"
    assert convert_to_markdown("[text](link)") == r"\[text](link)"
    assert convert_to_markdown("1. x") == r"1\. x"
    assert convert_to_markdown("not a number. x") == r"not a number. x"
    assert convert_to_markdown("1) x") == r"1\) x"
    assert convert_to_markdown("not a number) x") == r"not a number) x"
    assert convert_to_markdown("|not table|") == r"\|not table\|"
    assert convert_to_markdown(r"\ <foo> &amp;amp; | ` `", escape_misc=False) == r"\ <foo> &amp; | ` `"


def test_chomp() -> None:
    assert convert_to_markdown(" <b></b> ") == "  "
    assert convert_to_markdown(" <b> </b> ") == "  "
    assert convert_to_markdown(" <b>  </b> ") == "  "
    assert convert_to_markdown(" <b>   </b> ") == "  "
    assert convert_to_markdown(" <b>s </b> ") == " **s**  "
    assert convert_to_markdown(" <b> s</b> ") == "  **s** "
    assert convert_to_markdown(" <b> s </b> ") == "  **s**  "
    assert convert_to_markdown(" <b>  s  </b> ") == "  **s**  "


def test_nested() -> None:
    text = convert_to_markdown('<p>This is an <a href="http://example.com/">example link</a>.</p>')
    assert text == "This is an [example link](http://example.com/).\n\n"


def test_ignore_comments() -> None:
    text = convert_to_markdown("<!-- This is a comment -->")
    assert text == ""


def test_ignore_comments_with_other_tags() -> None:
    text = convert_to_markdown("<!-- This is a comment --><a href='http://example.com/'>example link</a>")
    assert text == "[example link](http://example.com/)"


def test_code_with_tricky_content() -> None:
    assert convert_to_markdown("<code>></code>") == "`>`"
    assert convert_to_markdown("<code>/home/</code><b>username</b>") == "`/home/`**username**"
    assert (
        convert_to_markdown("First line <code>blah blah<br />blah blah</code> second line")
        == "First line `blah blah  \nblah blah` second line"
    )


def test_special_tags() -> None:
    assert convert_to_markdown("<!DOCTYPE html>") == ""
    assert convert_to_markdown("<![CDATA[foobar]]>") == "foobar"


def test_strip() -> None:
    text = convert_to_markdown('<a href="https://github.com/matthewwithanm">Some Text</a>', strip=["a"])
    assert text == "Some Text"


def test_do_not_strip() -> None:
    text = convert_to_markdown('<a href="https://github.com/matthewwithanm">Some Text</a>', strip=[])
    assert text == "[Some Text](https://github.com/matthewwithanm)"


def test_convert() -> None:
    text = convert_to_markdown('<a href="https://github.com/matthewwithanm">Some Text</a>', convert=["a"])
    assert text == "[Some Text](https://github.com/matthewwithanm)"


def test_do_not_convert() -> None:
    text = convert_to_markdown('<a href="https://github.com/matthewwithanm">Some Text</a>', convert=[])
    assert text == "Some Text"


def test_ol() -> None:
    assert convert_to_markdown("<ol><li>a</li><li>b</li></ol>") == "1. a\n2. b\n"
    assert convert_to_markdown('<ol start="3"><li>a</li><li>b</li></ol>') == "3. a\n4. b\n"
    assert convert_to_markdown('<ol start="-1"><li>a</li><li>b</li></ol>') == "1. a\n2. b\n"
    assert convert_to_markdown('<ol start="foo"><li>a</li><li>b</li></ol>') == "1. a\n2. b\n"
    assert convert_to_markdown('<ol start="1.5"><li>a</li><li>b</li></ol>') == "1. a\n2. b\n"


def test_nested_ols() -> None:
    assert (
        convert_to_markdown(nested_ols)
        == "\n1. 1\n\t1. a\n\t\t1. I\n\t\t2. II\n\t\t3. III\n\t2. b\n\t3. c\n2. 2\n3. 3\n"
    )


def test_ul() -> None:
    assert convert_to_markdown("<ul><li>a</li><li>b</li></ul>") == "* a\n* b\n"
    assert (
        convert_to_markdown("""<ul>
     <li>
             a
     </li>
     <li> b </li>
     <li>   c
     </li>
 </ul>""")
        == "* a\n* b\n* c\n"
    )


def test_inline_ul() -> None:
    assert convert_to_markdown("<p>foo</p><ul><li>a</li><li>b</li></ul><p>bar</p>") == "foo\n\n* a\n* b\n\nbar\n\n"


def test_nested_uls() -> None:
    """
    Nested ULs should alternate bullet characters.

    """
    assert convert_to_markdown(nested_uls) == "\n* 1\n\t+ a\n\t\t- I\n\t\t- II\n\t\t- III\n\t+ b\n\t+ c\n* 2\n* 3\n"


def test_bullets() -> None:
    assert (
        convert_to_markdown(nested_uls, bullets="-")
        == "\n- 1\n\t- a\n\t\t- I\n\t\t- II\n\t\t- III\n\t- b\n\t- c\n- 2\n- 3\n"
    )


def test_li_text() -> None:
    assert (
        convert_to_markdown(
            '<ul><li>foo <a href="#">bar</a></li><li>foo bar  </li><li>foo <b>bar</b>   <i>space</i>.</ul>'
        )
        == "* foo [bar](#)\n* foo bar\n* foo **bar** *space*.\n"
    )


def test_table() -> None:
    assert (
        convert_to_markdown(table)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_with_html_content)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| **Jill** | *Smith* | [50](#) |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_with_paragraphs)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_with_linebreaks)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith  Jackson | 50 |\n| Eve | Jackson  Smith | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_with_header_column)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_head_body)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_head_body_missing_head)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_missing_text)
        == "\n\n|  | Lastname | Age |\n| --- | --- | --- |\n| Jill |  | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_missing_head)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_body)
        == "\n\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_with_caption)
        == "TEXT\n\nCaption\n| Firstname | Lastname | Age |\n| --- | --- | --- |\n\n"
    )
    assert (
        convert_to_markdown(table_with_colspan)
        == "\n\n| Name | | Age |\n| --- | --- | --- |\n| Jill | Smith | 50 |\n| Eve | Jackson | 94 |\n\n"
    )
    assert (
        convert_to_markdown(table_with_undefined_colspan) == "\n\n| Name | Age |\n| --- | --- |\n| Jill | Smith |\n\n"
    )
