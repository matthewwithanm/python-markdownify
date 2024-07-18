from markdownify import markdownify as md


def test_asterisks():
    assert md('*hey*dude*') == r'\*hey\*dude\*'
    assert md('*hey*dude*', escape_asterisks=False) == r'*hey*dude*'


def test_underscore():
    assert md('_hey_dude_') == r'\_hey\_dude\_'
    assert md('_hey_dude_', escape_underscores=False) == r'_hey_dude_'


def test_xml_entities():
    assert md('&amp;') == r'&'


def test_named_entities():
    assert md('&raquo;') == u'\xbb'


def test_hexadecimal_entities():
    # This looks to be a bug in BeautifulSoup (fixed in bs4) that we have to work around.
    assert md('&#x27;') == '\x27'


def test_single_escaping_entities():
    assert md('&amp;amp;') == r'\&amp;'


def test_escape_misc_chars():
    assert md('[yes](link)') == '\\[yes](link)'
    assert md('&lt;yes&gt;') == '\\<yes>'
    assert md('\\yes') == '\\\\yes'
    assert md('*yes') == '\\*yes'

    assert md('\\ &lt;foo> &amp;amp; | ` `', escape_misc=False) == '\\ <foo> &amp; | ` `'


def test_escape_misc_hash():
    assert md('# yes\n## yes') == '\\# yes\n\\## yes'
    assert md(' # no\n ## no') == ' # no\n ## no'


def test_escape_misc_ampersand():
    assert md('&amp;yes;') == '\\&yes;'
    assert md('& no') == '& no'


def test_escape_misc_plus():
    assert md('+ yes\n + yes\n') == '\\+ yes\n \\+ yes\n'
    assert md('no+no\nno + no\n') == 'no+no\nno + no\n'


def test_escape_misc_hyphen():
    assert md('---\n') == '\\---\n'
    assert md('- yes\n - yes') == '\\- yes\n \\- yes'
    assert md('no-\n') == 'no-\n'
    assert md('yes--\n') == 'yes\\--\n'
    assert md('yes---\n') == 'yes\\---\n'
    assert md('no----\n') == 'no----\n'


def test_escape_misc_equals():
    assert md('yes\n=\n') == 'yes\n\\=\n'
    assert md('yes\n===\n') == 'yes\n\\===\n'
    assert md('no\n =\n') == 'no\n =\n'
    assert md('no=no') == 'no=no'
    assert md('yes==yes') == 'yes\\==yes'
    assert md('yes===yes') == 'yes\\===yes'


def test_escape_misc_greaterthan():
    assert md('> yes\n > yes') == '\\> yes\n \\> yes'
    assert md('>no\n >no') == '>no\n >no'


def test_escape_misc_backtick():
    assert md('```\n```yes') == '\\```\n\\```yes'
    assert md('``````\n``````yes') == '\\``````\n\\``````yes'
    assert md('`yes`\n `yes`') == '\\`yes\\`\n \\`yes\\`'


def test_escape_misc_pipe():
    assert md('|') == '\\|'
    assert md('|-|') == '\\|-\\|'
    assert md('| ---- |') == '\\| ---- \\|'
    assert md('|yes|') == '\\|yes\\|'
    assert md('| yes |') == '\\| yes \\|'


def test_escape_misc_tilde():
    assert md(' ~yes~') == ' \\~yes\\~'
    assert md(' ~~yes~~') == ' \\~\\~yes\\~\\~'
    assert md('~~~\n~~~yes\n') == '\\~~~\n\\~~~yes\n'


def test_escape_misc_listitems():
    assert md('1. yes\n 1. yes') == '1\\. yes\n 1\\. yes'
    assert md('1) yes\n 1) yes') == '1\\) yes\n 1\\) yes'
    assert md('1.no\n 1.no') == '1.no\n 1.no'
    assert md('1)no\n 1)no') == '1)no\n 1)no'
    assert md('no1. x\n no1. y') == 'no1. x\n no1. y'
    assert md('no1) x\n no1) y') == 'no1) x\n no1) y'
