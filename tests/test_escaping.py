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


def text_misc():
    assert md('\\*') == r'\\\*'
    assert md('<foo>') == r'\<foo\>'
    assert md('# foo') == r'\# foo'
    assert md('> foo') == r'\> foo'
    assert md('~~foo~~') == r'\~\~foo\~\~'
    assert md('foo\n===\n') == 'foo\n\\=\\=\\=\n'
    assert md('---\n') == '\\-\\-\\-\n'
    assert md('+ x\n+ y\n') == '\\+ x\n\\+ y\n'
    assert md('`x`') == r'\`x\`'
    assert md('[text](link)') == r'\[text](link)'
    assert md('1. x') == r'1\. x'
    assert md('not a number. x') == r'not a number. x'
    assert md('1) x') == r'1\) x'
    assert md('not a number) x') == r'not a number) x'
    assert md('|not table|') == r'\|not table\|'
    assert md(r'\ <foo> &amp;amp; | ` `', escape_misc=False) == r'\ <foo> &amp; | ` `'
