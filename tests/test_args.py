"""
Test whitelisting/blacklisting of specific tags.

"""

import pytest
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter, markdownify, LSTRIP, RSTRIP, STRIP, STRIP_ONE
from .utils import md


def test_strip():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', strip=['a'])
    assert text == 'Some Text'


def test_do_not_strip():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', strip=[])
    assert text == '[Some Text](https://github.com/matthewwithanm)'


def test_convert():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', convert=['a'])
    assert text == '[Some Text](https://github.com/matthewwithanm)'


def test_do_not_convert():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', convert=[])
    assert text == 'Some Text'


def test_strip_document():
    assert markdownify("<p>Hello</p>") == "Hello"  # test default of STRIP
    assert markdownify("<p>Hello</p>", strip_document=LSTRIP) == "Hello\n\n"
    assert markdownify("<p>Hello</p>", strip_document=RSTRIP) == "\n\nHello"
    assert markdownify("<p>Hello</p>", strip_document=STRIP) == "Hello"
    assert markdownify("<p>Hello</p>", strip_document=None) == "\n\nHello\n\n"


@pytest.mark.parametrize('strip, expected', [
    (LSTRIP, 'Hello\n\n'),
    (RSTRIP, '\n\nHello'),
    (STRIP, 'Hello'),
    (None, '\n\nHello\n\n'),
])
@pytest.mark.parametrize('tag', ['html', 'div', 'p'])
def test_strip_document_tag_root(strip, expected, tag):
    soup = BeautifulSoup('<html><div><p>Hello</p></div></html>', 'html.parser')
    converter = MarkdownConverter(strip_document=strip)
    assert converter.convert_soup(soup.find(tag)) == expected


def test_tag_root_document_converter_runs_once():
    class DocumentConverter(MarkdownConverter):
        def convert__document_(self, el, text, parent_tags):
            return '[' + text.strip() + ']'

    soup = BeautifulSoup('<p>Hello</p>', 'html.parser')
    converter = DocumentConverter()
    assert converter.convert_soup(soup) == '[Hello]'
    assert converter.convert_soup(soup.p) == '[Hello]'


def test_tag_root_honors_document_conversion_filter():
    soup = BeautifulSoup('<p>Hello</p>', 'html.parser')
    converter = MarkdownConverter(convert=['p'])
    assert converter.convert_soup(soup.p) == converter.convert_soup(soup)


def test_strip_pre():
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>") == "```\n  Hello\n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=STRIP) == "```\n  Hello\n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=STRIP_ONE) == "```\n  \n  Hello  \n  \n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=None) == "```\n  \n  \n  Hello  \n  \n  \n```"


def bs4_options():
    assert markdownify("<p>Hello</p>", bs4_options="html.parser") == "Hello"
    assert markdownify("<p>Hello</p>", bs4_options=["html.parser"]) == "Hello"
    assert markdownify("<p>Hello</p>", bs4_options={"features": "html.parser"}) == "Hello"
