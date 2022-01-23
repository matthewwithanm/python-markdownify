from markdownify import MarkdownConverter
from bs4 import BeautifulSoup


class ImageBlockConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """
    def convert_img(self, el, text, convert_as_inline):
        return super().convert_img(el, text, convert_as_inline) + '\n\n'


def test_img():
    # Create shorthand method for conversion
    def md(html, **options):
        return ImageBlockConverter(**options).convert(html)

    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />') == '![Alt text](/path/to/img.jpg "Optional title")\n\n'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />') == '![Alt text](/path/to/img.jpg)\n\n'


def test_soup():
    html = '<b>test</b>'
    soup = BeautifulSoup(html, 'html.parser')
    assert MarkdownConverter().convert_soup(soup) == '**test**'
