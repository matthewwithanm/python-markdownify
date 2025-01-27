from .utils import md


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
    assert md('<ol><li>a</li><li>b</li></ol>') == '\n\n1. a\n2. b\n'
    assert md('<ol start="3"><li>a</li><li>b</li></ol>') == '\n\n3. a\n4. b\n'
    assert md('foo<ol start="3"><li>a</li><li>b</li></ol>bar') == 'foo\n\n3. a\n4. b\n\nbar'
    assert md('<ol start="-1"><li>a</li><li>b</li></ol>') == '\n\n1. a\n2. b\n'
    assert md('<ol start="foo"><li>a</li><li>b</li></ol>') == '\n\n1. a\n2. b\n'
    assert md('<ol start="1.5"><li>a</li><li>b</li></ol>') == '\n\n1. a\n2. b\n'
    assert md('<ol start="1234"><li><p>first para</p><p>second para</p></li><li><p>third para</p><p>fourth para</p></li></ol>') == '\n\n1234. first para\n\n      second para\n1235. third para\n\n      fourth para\n'


def test_nested_ols():
    assert md(nested_ols) == '\n\n1. 1\n   1. a\n      1. I\n      2. II\n      3. III\n   2. b\n   3. c\n2. 2\n3. 3\n'


def test_ul():
    assert md('<ul><li>a</li><li>b</li></ul>') == '\n\n* a\n* b\n'
    assert md("""<ul>
     <li>
             a
     </li>
     <li> b </li>
     <li>   c
     </li>
 </ul>""") == '\n\n* a\n* b\n* c\n'
    assert md('<ul><li><p>first para</p><p>second para</p></li><li><p>third para</p><p>fourth para</p></li></ul>') == '\n\n* first para\n\n  second para\n* third para\n\n  fourth para\n'


def test_inline_ul():
    assert md('<p>foo</p><ul><li>a</li><li>b</li></ul><p>bar</p>') == '\n\nfoo\n\n* a\n* b\n\nbar\n\n'
    assert md('foo<ul><li>bar</li></ul>baz') == 'foo\n\n* bar\n\nbaz'


def test_nested_uls():
    """
    Nested ULs should alternate bullet characters.

    """
    assert md(nested_uls) == '\n\n* 1\n  + a\n    - I\n    - II\n    - III\n  + b\n  + c\n* 2\n* 3\n'


def test_bullets():
    assert md(nested_uls, bullets='-') == '\n\n- 1\n  - a\n    - I\n    - II\n    - III\n  - b\n  - c\n- 2\n- 3\n'


def test_li_text():
    assert md('<ul><li>foo <a href="#">bar</a></li><li>foo bar  </li><li>foo <b>bar</b>   <i>space</i>.</ul>') == '\n\n* foo [bar](#)\n* foo bar\n* foo **bar** *space*.\n'
