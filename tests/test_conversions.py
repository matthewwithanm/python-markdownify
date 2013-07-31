from markdownify import markdownify as md


def test_a():
    assert md('<a href="http://google.com">Google</a>') == '[Google](http://google.com)'


def test_a_with_title():
    text = md('<a href="http://google.com" title="The &quot;Goog&quot;">Google</a>')
    assert text == r'[Google](http://google.com "The \"Goog\"")'


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
