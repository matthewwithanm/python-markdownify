import warnings
from bs4 import MarkupResemblesLocatorWarning
from .utils import md


def test_asterisks():
    assert md('*hey*dude*') == r'\*hey\*dude\*'
    assert md('*hey*dude*', escape_asterisks=False) == r'*hey*dude*'


def test_underscore():
    assert md('_hey_dude_') == r'\_hey\_dude\_'
    assert md('_hey_dude_', escape_underscores=False) == r'_hey_dude_'


def test_xml_entities():
    assert md('&amp;', escape_misc=True) == r'\&'


def test_named_entities():
    assert md('&raquo;') == u'\xbb'


def test_hexadecimal_entities():
    # This looks to be a bug in BeautifulSoup (fixed in bs4) that we have to work around.
    assert md('&#x27;') == '\x27'


def test_single_escaping_entities():
    assert md('&amp;amp;', escape_misc=True) == r'\&amp;'


def test_misc():
    # ignore the bs4 warning that "1.2" or "*" looks like a filename
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

    assert md('\\*', escape_misc=True) == r'\\\*'
    assert md('&lt;foo>', escape_misc=True) == r'\<foo\>'
    assert md('# foo', escape_misc=True) == r'\# foo'
    assert md('#5', escape_misc=True) == r'#5'
    assert md('5#', escape_misc=True) == '5#'
    assert md('####### foo', escape_misc=True) == r'####### foo'
    assert md('> foo', escape_misc=True) == r'\> foo'
    assert md('~~foo~~', escape_misc=True) == r'\~\~foo\~\~'
    assert md('foo\n===\n', escape_misc=True) == 'foo\n\\=\\=\\=\n'
    assert md('---\n', escape_misc=True) == '\\---\n'
    assert md('- test', escape_misc=True) == r'\- test'
    assert md('x - y', escape_misc=True) == r'x \- y'
    assert md('test-case', escape_misc=True) == 'test-case'
    assert md('x-', escape_misc=True) == 'x-'
    assert md('-y', escape_misc=True) == '-y'
    assert md('+ x\n+ y\n', escape_misc=True) == '\\+ x\n\\+ y\n'
    assert md('`x`', escape_misc=True) == r'\`x\`'
    assert md('[text](link)', escape_misc=True) == r'\[text](link)'
    assert md('1. x', escape_misc=True) == r'1\. x'
    # assert md('1<span>.</span> x', escape_misc=True) == r'1\. x'
    assert md('<span>1.</span> x', escape_misc=True) == r'1\. x'
    assert md(' 1. x', escape_misc=True) == r' 1\. x'
    assert md('123456789. x', escape_misc=True) == r'123456789\. x'
    assert md('1234567890. x', escape_misc=True) == r'1234567890. x'
    assert md('A1. x', escape_misc=True) == r'A1. x'
    assert md('1.2', escape_misc=True) == r'1.2'
    assert md('not a number. x', escape_misc=True) == r'not a number. x'
    assert md('1) x', escape_misc=True) == r'1\) x'
    # assert md('1<span>)</span> x', escape_misc=True) == r'1\) x'
    assert md('<span>1)</span> x', escape_misc=True) == r'1\) x'
    assert md(' 1) x', escape_misc=True) == r' 1\) x'
    assert md('123456789) x', escape_misc=True) == r'123456789\) x'
    assert md('1234567890) x', escape_misc=True) == r'1234567890) x'
    assert md('(1) x', escape_misc=True) == r'(1) x'
    assert md('A1) x', escape_misc=True) == r'A1) x'
    assert md('1)x', escape_misc=True) == r'1)x'
    assert md('not a number) x', escape_misc=True) == r'not a number) x'
    assert md('|not table|', escape_misc=True) == r'\|not table\|'
    assert md(r'\ &lt;foo> &amp;amp; | ` `', escape_misc=False) == r'\ <foo> &amp; | ` `'
