from markdownify import markdownify as md, ATX, ATX_CLOSED, BACKSLASH, UNDERSCORE
import re


nested_uls = re.sub(r'\s+', '', """
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


def test_chomp():
    assert md(' <b></b> ') == '  '
    assert md(' <b> </b> ') == '  '
    assert md(' <b>  </b> ') == '  '
    assert md(' <b>   </b> ') == '  '
    assert md(' <b>s </b> ') == ' **s**  '
    assert md(' <b> s</b> ') == '  **s** '
    assert md(' <b> s </b> ') == '  **s**  '
    assert md(' <b>  s  </b> ') == '  **s**  '


def test_a():
    assert md('<a href="https://google.com">Google</a>') == '[Google](https://google.com)'
    assert md('<a href="https://google.com">https://google.com</a>', autolinks=False) == '[https://google.com](https://google.com)'
    assert md('<a href="https://google.com">https://google.com</a>') == '<https://google.com>'
    assert md('<a href="https://community.kde.org/Get_Involved">https://community.kde.org/Get_Involved</a>') == '<https://community.kde.org/Get_Involved>'
    assert md('<a href="https://community.kde.org/Get_Involved">https://community.kde.org/Get_Involved</a>', autolinks=False) == '[https://community.kde.org/Get\\_Involved](https://community.kde.org/Get_Involved)'


def test_a_spaces():
    assert md('foo <a href="http://google.com">Google</a> bar') == 'foo [Google](http://google.com) bar'
    assert md('foo<a href="http://google.com"> Google</a> bar') == 'foo [Google](http://google.com) bar'
    assert md('foo <a href="http://google.com">Google </a>bar') == 'foo [Google](http://google.com) bar'
    assert md('foo <a href="http://google.com"></a> bar') == 'foo  bar'


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


def test_b_spaces():
    assert md('foo <b>Hello</b> bar') == 'foo **Hello** bar'
    assert md('foo<b> Hello</b> bar') == 'foo **Hello** bar'
    assert md('foo <b>Hello </b>bar') == 'foo **Hello** bar'
    assert md('foo <b></b> bar') == 'foo  bar'


def test_blockquote():
    assert md('<blockquote>Hello</blockquote>') == '\n> Hello\n\n'


def test_blockquote_with_paragraph():
    assert md('<blockquote>Hello</blockquote><p>handsome</p>') == '\n> Hello\n\nhandsome\n\n'


def test_nested_blockquote():
    text = md('<blockquote>And she was like <blockquote>Hello</blockquote></blockquote>')
    assert text == '\n> And she was like \n> > Hello\n> \n> \n\n'


def test_br():
    assert md('a<br />b<br />c') == 'a  \nb  \nc'


def test_em():
    assert md('<em>Hello</em>') == '*Hello*'


def test_em_spaces():
    assert md('foo <em>Hello</em> bar') == 'foo *Hello* bar'
    assert md('foo<em> Hello</em> bar') == 'foo *Hello* bar'
    assert md('foo <em>Hello </em>bar') == 'foo *Hello* bar'
    assert md('foo <em></em> bar') == 'foo  bar'


def test_h1():
    assert md('<h1>Hello</h1>') == 'Hello\n=====\n\n'


def test_h2():
    assert md('<h2>Hello</h2>') == 'Hello\n-----\n\n'


def test_hn():
    assert md('<h3>Hello</h3>') == '### Hello\n\n'
    assert md('<h6>Hello</h6>') == '###### Hello\n\n'


def test_hn_chained():
    assert md('<h1>First</h1>\n<h2>Second</h2>\n<h3>Third</h3>', heading_style=ATX) == '# First\n\n\n## Second\n\n\n### Third\n\n'
    assert md('X<h1>First</h1>', heading_style=ATX) == 'X# First\n\n'


def test_hn_nested_tag_heading_style():
    assert md('<h1>A <p>P</p> C </h1>', heading_style=ATX_CLOSED) == '# A P C #\n\n'
    assert md('<h1>A <p>P</p> C </h1>', heading_style=ATX) == '# A P C\n\n'


def test_hn_nested_simple_tag():
    tag_to_markdown = [
        ("strong", "**strong**"),
        ("b", "**b**"),
        ("em", "*em*"),
        ("i", "*i*"),
        ("p", "p"),
        ("a", "a"),
        ("div", "div"),
        ("blockquote", "blockquote"),
    ]

    for tag, markdown in tag_to_markdown:
        assert md('<h3>A <' + tag + '>' + tag + '</' + tag + '> B</h3>') == '### A ' + markdown + ' B\n\n'

    assert md('<h3>A <br>B</h3>', heading_style=ATX) == '### A B\n\n'

    # Nested lists not supported
    # assert md('<h3>A <ul><li>li1</i><li>l2</li></ul></h3>', heading_style=ATX) == '### A li1 li2 B\n\n'


def test_hn_nested_img():
    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />') == '![Alt text](/path/to/img.jpg "Optional title")'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />') == '![Alt text](/path/to/img.jpg)'
    image_attributes_to_markdown = [
        ("", ""),
        ("alt='Alt Text'", "Alt Text"),
        ("alt='Alt Text' title='Optional title'", "Alt Text"),
    ]
    for image_attributes, markdown in image_attributes_to_markdown:
        assert md('<h3>A <img src="/path/to/img.jpg " ' + image_attributes + '/> B</h3>') == '### A ' + markdown + ' B\n\n'


def test_hr():
    assert md('<hr>hr</hr>') == 'hr'


def test_head():
    assert md('<head>head</head>') == 'head'


def test_atx_headings():
    assert md('<h1>Hello</h1>', heading_style=ATX) == '# Hello\n\n'
    assert md('<h2>Hello</h2>', heading_style=ATX) == '## Hello\n\n'


def test_atx_closed_headings():
    assert md('<h1>Hello</h1>', heading_style=ATX_CLOSED) == '# Hello #\n\n'
    assert md('<h2>Hello</h2>', heading_style=ATX_CLOSED) == '## Hello ##\n\n'


def test_i():
    assert md('<i>Hello</i>') == '*Hello*'


def test_ol():
    assert md('<ol><li>a</li><li>b</li></ol>') == '\n1. a\n2. b\n\n'
    assert md('<ol start="3"><li>a</li><li>b</li></ol>') == '\n3. a\n4. b\n\n'


def test_p():
    assert md('<p>hello</p>') == 'hello\n\n'


def test_strong():
    assert md('<strong>Hello</strong>') == '**Hello**'


def test_ul():
    assert md('<ul><li>a</li><li>b</li></ul>') == '\n* a\n* b\n\n'


def test_inline_ul():
    assert md('<p>foo</p><ul><li>a</li><li>b</li></ul><p>bar</p>') == 'foo\n\n\n* a\n* b\n\nbar\n\n'


def test_nested_uls():
    """
    Nested ULs should alternate bullet characters.

    """
    assert md(nested_uls) == '\n* 1\n\t+ a\n\t\t- I\n\t\t- II\n\t\t- III\n\t+ b\n\t+ c\n* 2\n* 3\n\n'


def test_bullets():
    assert md(nested_uls, bullets='-') == '\n- 1\n\t- a\n\t\t- I\n\t\t- II\n\t\t- III\n\t- b\n\t- c\n- 2\n- 3\n\n'


def test_img():
    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />') == '![Alt text](/path/to/img.jpg "Optional title")'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />') == '![Alt text](/path/to/img.jpg)'


def test_div():
    assert md('Hello</div> World') == 'Hello World'


def test_strong_em_symbol():
    assert md('<strong>Hello</strong>', strong_em_symbol=UNDERSCORE) == '__Hello__'
    assert md('<b>Hello</b>', strong_em_symbol=UNDERSCORE) == '__Hello__'
    assert md('<em>Hello</em>', strong_em_symbol=UNDERSCORE) == '_Hello_'
    assert md('<i>Hello</i>', strong_em_symbol=UNDERSCORE) == '_Hello_'


def test_newline_style():
    assert md('a<br />b<br />c', newline_style=BACKSLASH) == 'a\\\nb\\\nc'
