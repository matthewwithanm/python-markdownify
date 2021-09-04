from markdownify import markdownify as md


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


def test_ol():
    assert md('<ol><li>a</li><li>b</li></ol>') == '1. a\n2. b\n'
    assert md('<ol start="3"><li>a</li><li>b</li></ol>') == '3. a\n4. b\n'


def test_nested_ols():
    assert md(nested_ols) == '\n1. 1\n\t1. a\n\t\t1. I\n\t\t2. II\n\t\t3. III\n\t2. b\n\t3. c\n2. 2\n3. 3\n'


def test_ul():
    assert md('<ul><li>a</li><li>b</li></ul>') == '* a\n* b\n'
    assert md("""<ul>
     <li>
             a
     </li>
     <li> b </li>
     <li>   c
     </li>
 </ul>""") == '* a\n* b\n* c\n'


def test_inline_ul():
    assert md('<p>foo</p><ul><li>a</li><li>b</li></ul><p>bar</p>') == 'foo\n\n* a\n* b\n\nbar\n\n'


def test_nested_uls():
    """
    Nested ULs should alternate bullet characters.

    """
    assert md(nested_uls) == '\n* 1\n\t+ a\n\t\t- I\n\t\t- II\n\t\t- III\n\t+ b\n\t+ c\n* 2\n* 3\n'


def test_bullets():
    assert md(nested_uls, bullets='-') == '\n- 1\n\t- a\n\t\t- I\n\t\t- II\n\t\t- III\n\t- b\n\t- c\n- 2\n- 3\n'


def test_li_text():
    assert md('<ul><li>foo <a href="#">bar</a></li><li>foo bar  </li><li>foo <b>bar</b>   <i>space</i>.</ul>') == '* foo [bar](#)\n* foo bar\n* foo **bar** *space*.\n'
