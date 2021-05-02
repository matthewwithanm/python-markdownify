from markdownify import markdownify as md


def test_underscore():
    assert md('_hey_dude_') == r'\_hey\_dude\_'


def test_xml_entities():
    assert md('&amp;') == '&'


def test_named_entities():
    assert md('&raquo;') == u'\xbb'


def test_hexadecimal_entities():
    # This looks to be a bug in BeautifulSoup (fixed in bs4) that we have to work around.
    assert md('&#x27;') == '\x27'


def test_single_escaping_entities():
    assert md('&amp;amp;') == '&amp;'
