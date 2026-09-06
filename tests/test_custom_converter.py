from markdownify import MarkdownConverter
from bs4 import BeautifulSoup


class UnitTestConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter for unit tests
    """
    def convert_img(self, el, text, parent_tags):
        """Add two newlines after an image"""
        return super().convert_img(el, text, parent_tags) + '\n\n'

    def convert_custom_tag(self, el, text, parent_tags):
        """Ensure conversion function is found for tags with special characters in name"""
        return "convert_custom_tag(): %s" % text

    def convert_h1(self, el, text, parent_tags):
        """Ensure explicit heading conversion function is used"""
        return "convert_h1: %s" % (text)

    def convert_hN(self, n, el, text, parent_tags):
        """Ensure general heading conversion function is used"""
        return "convert_hN(%d): %s" % (n, text)


def test_custom_conversion_functions():
    # Create shorthand method for conversion
    def md(html, **options):
        return UnitTestConverter(**options).convert(html)

    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />text') == '![Alt text](/path/to/img.jpg "Optional title")\n\ntext'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />text') == '![Alt text](/path/to/img.jpg)\n\ntext'

    assert md("<custom-tag>text</custom-tag>") == "convert_custom_tag(): text"

    assert md("<h1>text</h1>") == "convert_h1: text"

    assert md("<h3>text</h3>") == "convert_hN(3): text"


def test_soup():
    html = '<b>test</b>'
    soup = BeautifulSoup(html, 'html.parser')
    assert MarkdownConverter().convert_soup(soup) == '**test**'


def test_tag_document_stripping():
    from markdownify import LSTRIP, RSTRIP, STRIP

    html = '<html><body><div><p>hello</p><p>world</p></div></body></html>'
    for mode, expected in [(LSTRIP, 'hello\n\nworld\n\n'),
                           (RSTRIP, '\n\nhello\n\nworld'),
                           (STRIP, 'hello\n\nworld'),
                           (None, '\n\nhello\n\nworld\n\n')]:
        for name in ['html', 'body', 'div']:
            soup = BeautifulSoup(html, 'html.parser')
            tag = soup.find(name)
            before = str(soup)
            assert MarkdownConverter(strip_document=mode).convert_soup(tag) == expected
            assert str(soup) == before
            assert tag.parent is not None


def test_tag_document_invalid_strip_mode():
    import pytest

    soup = BeautifulSoup('<p>hello</p>', 'html.parser')
    with pytest.raises(ValueError, match='Invalid value for strip_document'):
        MarkdownConverter(strip_document='invalid').convert_soup(soup.p)


def test_document_converter_called_once():
    class CountingConverter(MarkdownConverter):
        calls = 0

        def convert__document_(self, el, text, parent_tags):
            self.calls += 1
            return super().convert__document_(el, text, parent_tags)

    soup = BeautifulSoup('<div><p>hello</p></div>', 'html.parser')
    for root in [soup, soup.div, soup.p]:
        converter = CountingConverter()
        assert converter.convert_soup(root) == 'hello'
        assert converter.calls == 1


def test_tag_document_converter_exclusion():
    soup = BeautifulSoup('<p>hello</p>', 'html.parser')
    for root in [soup, soup.p]:
        assert MarkdownConverter(strip=['[document]']).convert_soup(root) == '\n\nhello\n\n'
