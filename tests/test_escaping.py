from markdownify import markdownify as md


def test_asterisks():
    assert md('*hey*dude*') == r'\*hey\*dude\*'
    assert md('*hey*dude*', escape_asterisks=False) == r'*hey*dude*'


def test_underscore():
    assert md('_hey_dude_') == r'\_hey\_dude\_'
    assert md('_hey_dude_', escape_underscores=False) == r'_hey_dude_'


def test_xml_entities():
    assert md('&amp;') == r'\&'


def test_named_entities():
    assert md('&raquo;') == u'\xbb'


def test_hexadecimal_entities():
    # This looks to be a bug in BeautifulSoup (fixed in bs4) that we have to work around.
    assert md('&#x27;') == '\x27'


def test_single_escaping_entities():
    assert md('&amp;amp;') == r'\&amp;'


def test_misc():
    assert md('\\*') == r'\\\*'
    assert md('&lt;foo>') == r'\<foo\>'
    assert md('# foo') == r'\# foo'
    assert md('#5') == r'#5'
    assert md('5#') == '5#'
    assert md('####### foo') == r'####### foo'
    assert md('> foo') == r'\> foo'
    assert md('~~foo~~') == r'\~\~foo\~\~'
    assert md('foo\n===\n') == 'foo\n\\=\\=\\=\n'
    assert md('---\n') == '\\---\n'
    assert md('- test') == r'\- test'
    assert md('x - y') == r'x \- y'
    assert md('test-case') == 'test-case'
    assert md('x-') == 'x-'
    assert md('-y') == '-y'
    assert md('+ x\n+ y\n') == '\\+ x\n\\+ y\n'
    assert md('`x`') == r'\`x\`'
    assert md('[text](link)') == r'\[text](link)'
    assert md('1. x') == r'1\. x'
    # assert md('1<span>.</span> x') == r'1\. x'
    assert md('<span>1.</span> x') == r'1\. x'
    assert md(' 1. x') == r' 1\. x'
    assert md('123456789. x') == r'123456789\. x'
    assert md('1234567890. x') == r'1234567890. x'
    assert md('A1. x') == r'A1. x'
    assert md('1.2') == r'1.2'
    assert md('not a number. x') == r'not a number. x'
    assert md('1) x') == r'1\) x'
    # assert md('1<span>)</span> x') == r'1\) x'
    assert md('<span>1)</span> x') == r'1\) x'
    assert md(' 1) x') == r' 1\) x'
    assert md('123456789) x') == r'123456789\) x'
    assert md('1234567890) x') == r'1234567890) x'
    assert md('(1) x') == r'(1) x'
    assert md('A1) x') == r'A1) x'
    assert md('1)x') == r'1)x'
    assert md('not a number) x') == r'not a number) x'
    assert md('|not table|') == r'\|not table\|'
    assert md(r'\ &lt;foo> &amp;amp; | ` `', escape_misc=False) == r'\ <foo> &amp; | ` `'
