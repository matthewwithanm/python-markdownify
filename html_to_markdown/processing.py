from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Literal, cast

from bs4 import BeautifulSoup, Comment, Doctype, NavigableString, Tag

from html_to_markdown.constants import (
    ASTERISK,
    SPACES,
    UNDERLINED,
    html_heading_re,
    whitespace_re,
)
from html_to_markdown.converters import ConverterssMap, create_converters_map
from html_to_markdown.utils import escape

if TYPE_CHECKING:
    from collections.abc import Iterable

    from bs4 import PageElement

SupportedTag = Literal[
    "a",
    "b",
    "blockquote",
    "br",
    "code",
    "del",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "list",
    "ul",
    "ol",
    "li",
    "p",
    "pre",
    "script",
    "style",
    "s",
    "strong",
    "samp",
    "sub",
    "sup",
    "table",
    "caption",
    "figcaption",
    "td",
    "th",
    "tr",
    "kbd",
]


def _is_nested_tag(el: PageElement) -> bool:
    return isinstance(el, Tag) and el.name in {
        "ol",
        "ul",
        "li",
        "table",
        "thead",
        "tbody",
        "tfoot",
        "tr",
        "td",
        "th",
    }


def _process_tag(
    tag: Tag,
    converters_map: ConverterssMap,
    *,
    convert: Iterable[str] | None,
    convert_as_inline: bool = False,
    escape_asterisks: bool,
    escape_misc: bool,
    escape_underscores: bool,
    strip: Iterable[str] | None,
) -> str:
    text = ""
    is_heading = html_heading_re.match(tag.name) is not None
    is_cell = tag.name in {"td", "th"}
    convert_children_as_inline = convert_as_inline or is_heading or is_cell

    if _is_nested_tag(tag):
        for el in tag.children:
            can_extract = (
                not el.previous_sibling
                or not el.next_sibling
                or _is_nested_tag(el.previous_sibling)
                or _is_nested_tag(el.next_sibling)
            )
            if can_extract and isinstance(el, NavigableString) and not el.strip():
                el.extract()

    for el in filter(lambda value: not isinstance(value, (Comment, Doctype)), tag.children):
        if isinstance(el, NavigableString):
            text += _process_text(
                el=el,
                escape_misc=escape_misc,
                escape_asterisks=escape_asterisks,
                escape_underscores=escape_underscores,
            )
        elif isinstance(el, Tag):
            text += _process_tag(
                el,
                converters_map,
                convert_as_inline=convert_children_as_inline,
                convert=convert,
                escape_asterisks=escape_asterisks,
                escape_misc=escape_misc,
                escape_underscores=escape_underscores,
                strip=strip,
            )

    tag_name: SupportedTag | None = cast(SupportedTag, tag.name.lower()) if tag.name.lower() in converters_map else None

    if tag_name and _should_convert_tag(tag_name=tag.name, strip=strip, convert=convert):
        return converters_map[tag_name](  # type: ignore[call-arg]
            tag=tag, text=text, convert_as_inline=convert_as_inline
        )

    return text


def _process_text(
    *,
    el: NavigableString,
    escape_misc: bool,
    escape_asterisks: bool,
    escape_underscores: bool,
) -> str:
    text = str(el) or ""

    # normalize whitespace if we're not inside a preformatted element
    if not el.find_parent("pre"):
        text = whitespace_re.sub(" ", text)

    # escape special characters if we're not inside a preformatted or code element
    if not el.find_parent(["pre", "code", "kbd", "samp"]):
        text = escape(
            text=text,
            escape_misc=escape_misc,
            escape_asterisks=escape_asterisks,
            escape_underscores=escape_underscores,
        )

    # remove trailing whitespaces if any of the following condition is true:
    # - current text node is the last node in li
    # - current text node is followed by an embedded list
    if (
        el.parent
        and el.parent.name == "li"
        and (not el.next_sibling or getattr(el.next_sibling, "name", None) in {"ul", "ol"})
    ):
        text = text.rstrip()

    return text


def _should_convert_tag(*, tag_name: str, strip: Iterable[str] | None, convert: Iterable[str] | None) -> bool:
    if strip is not None:
        return tag_name not in strip
    if convert is not None:
        return tag_name in convert
    return True


def convert_to_markdown(
    source: str | BeautifulSoup,
    *,
    autolinks: bool = True,
    bullets: str = "*+-",
    code_language: str = "",
    code_language_callback: Callable[[Any], str] | None = None,
    convert: Iterable[str] | None = None,
    default_title: bool = False,
    escape_asterisks: bool = True,
    escape_misc: bool = True,
    escape_underscores: bool = True,
    heading_style: Literal["underlined", "atx", "atx_closed"] = UNDERLINED,
    keep_inline_images_in: Iterable[str] | None = None,
    newline_style: Literal["spaces", "backslash"] = SPACES,
    strip: Iterable[str] | None = None,
    strong_em_symbol: Literal["*", "_"] = ASTERISK,
    sub_symbol: str = "",
    sup_symbol: str = "",
    wrap: bool = False,
    wrap_width: int = 80,
    convert_as_inline: bool = False,
) -> str:
    """Convert HTML to Markdown.

    Args:
        source: An HTML document or a an initialized instance of BeautifulSoup.
        autolinks: Automatically convert valid URLs into Markdown links. Defaults to True.
        bullets: A string of characters to use for bullet points in lists. Defaults to '*+-'.
        code_language: Default language identifier for fenced code blocks. Defaults to an empty string.
        code_language_callback: Function to dynamically determine the language for code blocks.
        convert: A list of tag names to convert to Markdown. If None, all supported tags are converted.
        default_title: Use the default title when converting certain elements (e.g., links). Defaults to False.
        escape_asterisks: Escape asterisks (*) to prevent unintended Markdown formatting. Defaults to True.
        escape_misc: Escape miscellaneous characters to prevent conflicts in Markdown. Defaults to True.
        escape_underscores: Escape underscores (_) to prevent unintended italic formatting. Defaults to True.
        heading_style: The style to use for Markdown headings. Defaults to "underlined".
        keep_inline_images_in: Tags in which inline images should be preserved. Defaults to None.
        newline_style: Style for handling newlines in text content. Defaults to "spaces".
        strip: Tags to strip from the output. Defaults to None.
        strong_em_symbol: Symbol to use for strong/emphasized text. Defaults to "*".
        sub_symbol: Custom symbol for subscript text. Defaults to an empty string.
        sup_symbol: Custom symbol for superscript text. Defaults to an empty string.
        wrap: Wrap text to the specified width. Defaults to False.
        wrap_width: The number of characters at which to wrap text. Defaults to 80.
        convert_as_inline: Treat the content as inline elements (no block elements like paragraphs). Defaults to False.

    Returns:
        str: A string of Markdown-formatted text converted from the given HTML.
    """
    if isinstance(source, str):
        from bs4 import BeautifulSoup

        source = BeautifulSoup(source, "html.parser")

    converters_map = create_converters_map(
        autolinks=autolinks,
        bullets=bullets,
        code_language=code_language,
        code_language_callback=code_language_callback,
        default_title=default_title,
        heading_style=heading_style,
        keep_inline_images_in=keep_inline_images_in,
        newline_style=newline_style,
        strong_em_symbol=strong_em_symbol,
        sub_symbol=sub_symbol,
        sup_symbol=sup_symbol,
        wrap=wrap,
        wrap_width=wrap_width,
    )

    return _process_tag(
        source,
        converters_map,
        convert=convert,
        convert_as_inline=convert_as_inline,
        escape_asterisks=escape_asterisks,
        escape_misc=escape_misc,
        escape_underscores=escape_underscores,
        strip=strip,
    )
