from markdownify import markdownify, ASTERISK, BACKSLASH, LSTRIP, RSTRIP, SPACES, STRIP, UNDERLINED, UNDERSCORE, MarkdownConverter
from bs4 import BeautifulSoup
from typing import Union

markdownify("<p>Hello</p>") == "Hello"  # test default of STRIP
markdownify("<p>Hello</p>", strip_document=LSTRIP) == "Hello\n\n"
markdownify("<p>Hello</p>", strip_document=RSTRIP) == "\n\nHello"
markdownify("<p>Hello</p>", strip_document=STRIP) == "Hello"
markdownify("<p>Hello</p>", strip_document=None) == "\n\nHello\n\n"

# default options
MarkdownConverter(
    autolinks=True,
    bs4_options='html.parser',
    bullets='*+-',
    code_language='',
    code_language_callback=None,
    convert=None,
    default_title=False,
    escape_asterisks=True,
    escape_underscores=True,
    escape_misc=False,
    heading_style=UNDERLINED,
    keep_inline_images_in=[],
    newline_style=SPACES,
    strip=None,
    strip_document=STRIP,
    strip_pre=STRIP,
    strong_em_symbol=ASTERISK,
    sub_symbol='',
    sup_symbol='',
    table_infer_header=False,
    wrap=False,
    wrap_width=80,
).convert("")

# custom options
MarkdownConverter(
    strip_document=None,
    bullets="-",
    escape_asterisks=True,
    escape_underscores=True,
    escape_misc=True,
    autolinks=True,
    default_title=True,
    newline_style=BACKSLASH,
    sup_symbol='^',
    sub_symbol='^',
    keep_inline_images_in=['h3'],
    wrap=True,
    wrap_width=80,
    strong_em_symbol=UNDERSCORE,
    code_language='python',
    code_language_callback=None
).convert("")

html = '<b>test</b>'
soup = BeautifulSoup(html, 'html.parser')
MarkdownConverter().convert_soup(soup) == '**test**'


def callback(el: BeautifulSoup) -> Union[str, None]:
    return el['class'][0] if el.has_attr('class') else None


MarkdownConverter(code_language_callback=callback).convert("")
MarkdownConverter(code_language_callback=lambda el: None).convert("")

markdownify('<pre class="python">test\n    foo\nbar</pre>', code_language_callback=callback)
markdownify('<pre class="python">test\n    foo\nbar</pre>', code_language_callback=lambda el: None)
