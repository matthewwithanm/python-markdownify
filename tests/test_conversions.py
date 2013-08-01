from markdownify import markdownify as md, ATX, ATX_CLOSED
import re


nested_uls = re.sub('\s+', '', """
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
    </ul>""")


def test_a():
    assert md('<a href="http://google.com">Google</a>') == '[Google](http://google.com)'


def test_a_with_title():
    text = md('<a href="http://google.com" title="The &quot;Goog&quot;">Google</a>')
    assert text == r'[Google](http://google.com "The \"Goog\"")'


def test_a_shortcut():
    text = md('<a href="http://google.com">http://google.com</a>')
    assert text == '<http://google.com>'


def test_a_no_autolinks():
    text = md('<a href="http://google.com">http://google.com</a>', autolinks=False)
    assert text == '[http://google.com](http://google.com)'


def test_b():
    assert md('<b>Hello</b>') == '**Hello**'


def test_blockquote():
    assert md('<blockquote>Hello</blockquote>').strip() == '> Hello'


def test_nested_blockquote():
    text = md('<blockquote>And she was like <blockquote>Hello</blockquote></blockquote>').strip()
    assert text == '> And she was like \n> > Hello'


def test_br():
    assert md('a<br />b<br />c') == 'a  \nb  \nc'


def test_em():
    assert md('<em>Hello</em>') == '*Hello*'


def test_h1():
    assert md('<h1>Hello</h1>') == 'Hello\n=====\n\n'


def test_h2():
    assert md('<h2>Hello</h2>') == 'Hello\n-----\n\n'


def test_hn():
    assert md('<h3>Hello</h3>') == '### Hello\n\n'
    assert md('<h6>Hello</h6>') == '###### Hello\n\n'


def test_atx_headings():
    assert md('<h1>Hello</h1>', heading_style=ATX) == '# Hello\n\n'
    assert md('<h2>Hello</h2>', heading_style=ATX) == '## Hello\n\n'


def test_atx_closed_headings():
    assert md('<h1>Hello</h1>', heading_style=ATX_CLOSED) == '# Hello #\n\n'
    assert md('<h2>Hello</h2>', heading_style=ATX_CLOSED) == '## Hello ##\n\n'


def test_i():
    assert md('<i>Hello</i>') == '*Hello*'


def test_ol():
    assert md('<ol><li>a</li><li>b</li></ol>') == '1. a\n2. b\n'


def test_p():
    assert md('<p>hello</p>') == 'hello\n\n'


def test_strong():
    assert md('<strong>Hello</strong>') == '**Hello**'


def test_ul():
    assert md('<ul><li>a</li><li>b</li></ul>') == '* a\n* b\n'


def test_nested_uls():
    """
    Nested ULs should alternate bullet characters.

    """
    assert md(nested_uls) == '* 1\n\t+ a\n\t\t- I\n\t\t- II\n\t\t- III\n\t\t\n\t+ b\n\t+ c\n\t\n* 2\n* 3\n'


def test_bullets():
    assert md(nested_uls, bullets='-') == '- 1\n\t- a\n\t\t- I\n\t\t- II\n\t\t- III\n\t\t\n\t- b\n\t- c\n\t\n- 2\n- 3\n'


def test_img():
    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />') == '![Alt text](/path/to/img.jpg "Optional title")'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />') == '![Alt text](/path/to/img.jpg)'
