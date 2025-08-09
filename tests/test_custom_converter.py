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
