from __future__ import annotations

from collections.abc import Mapping
from functools import partial
from inspect import getfullargspec
from textwrap import fill
from typing import Any, Callable, Literal

from bs4.element import Tag

from html_to_markdown.constants import ATX_CLOSED, BACKSLASH, UNDERLINED, line_beginning_re
from html_to_markdown.utils import chomp, indent, underline

SupportedElements = Literal[
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

ConvertsMap = Mapping[SupportedElements, Callable[[str, Tag], str]]


def _create_inline_converter(markup_prefix: str) -> Callable[[Tag, str], str]:
    """This abstracts all simple inline tags like b, em, del, ...
    Returns a function that wraps the chomped text in a pair of the string
    that is returned by markup_fn, with '/' inserted in the string used after
    the text if it looks like an HTML tag. markup_fn is necessary to allow for
    references to self.strong_em_symbol etc.
    """

    def implementation(*, tag: Tag, text: str) -> str:
        if not text:
            return ""

        if tag.find_parent(["pre", "code", "kbd", "samp"]):
            return text

        markup_suffix = markup_prefix
        if markup_prefix.startswith("<") and markup_prefix.endswith(">"):
            markup_suffix = "</" + markup_prefix[1:]

        prefix, suffix, text = chomp(text)

        return f"{prefix}{markup_prefix}{text}{markup_suffix}{suffix}"

    return implementation


def _convert_a(*, tag: Tag, text: str, auto_links: bool, default_title: str) -> str:
    prefix, suffix, text = chomp(text)
    if not text:
        return ""

    href = tag.get("href")
    title = tag.get("title")

    if auto_links and text.replace(r"\_", "_") == href and not title and not default_title:
        return f"<{href}>"

    if default_title and not title:
        title = href

    title_part = ' "{}"'.format(title.replace('"', r"\"")) if title else ""
    return f"{prefix}[{text}]({href}{title_part}){suffix}" if href else text


def _convert_blockquote(*, text: str, convert_as_inline: bool) -> str:
    if convert_as_inline:
        return text
    return f"\n{line_beginning_re.sub('> ', text.strip())}\n\n" if text else ""


def _convert_br(*, convert_as_inline: bool, newline_style: str) -> str:
    if convert_as_inline:
        return ""
    return "\\\n" if newline_style.lower() == BACKSLASH else "  \n"


def _convert_hn(*, n: int, heading_style: str, text: str, convert_as_inline: bool) -> str:
    if convert_as_inline:
        return text

    style = heading_style.lower()
    text = text.strip()
    if style == UNDERLINED and n <= 2:
        line = "=" if n == 1 else "-"
        return underline(text=text, pad_char=line)

    hashes = "#" * n
    return f"{hashes} {text} {hashes}\n\n" if style == ATX_CLOSED else f"{hashes} {text}\n\n"


def _convert_img(*, tag: Tag, convert_as_inline: bool, keep_inline_images_in: list) -> str:
    alt = tag.attrs.get("alt", None) or ""
    src = tag.attrs.get("src", None) or ""
    title = tag.attrs.get("title", None) or ""
    title_part = ' "{}"'.format(title.replace('"', r"\"")) if title else ""
    if convert_as_inline and tag.parent.name not in keep_inline_images_in:
        return alt

    return f"![{alt}]({src}{title_part})"


def _convert_list(*, tag: Tag, text: str) -> str:
    nested = False
    before_paragraph = False
    if tag.next_sibling and getattr(tag.next_sibling, "name", None) not in {"ul", "ol"}:
        before_paragraph = True
    while tag:
        if tag.name == "li":
            nested = True
            break
        tag = tag.parent
    return f"\n{indent(text=text, level=1).rstrip()}" if nested else text + ("\n" if before_paragraph else "")


def _convert_li(*, tag: Tag, text: str, bullets: str) -> str:
    parent = tag.parent
    if parent and parent.name == "ol":
        start = int(parent.get("start", "1"))
        bullet = f"{start + parent.index(tag)}."
    else:
        depth = -1
        while tag:
            if tag.name == "ul":
                depth += 1
            tag = tag.parent
        bullet = bullets[depth % len(bullets)]
    return f"{bullet} {text.strip()}\n"


def _convert_p(*, wrap: bool, text: str, convert_as_inline: bool, wrap_width: int) -> str:
    if convert_as_inline:
        return text
    if wrap:
        text = fill(text, width=wrap_width, break_long_words=False, break_on_hyphens=False)
    return f"{text}\n\n" if text else ""


def _convert_pre(*, tag: Tag, text: str, code_language: str, code_language_callback: Callable) -> str:
    if not text:
        return ""

    if code_language_callback:
        code_language = code_language_callback(tag) or code_language

    return f"\n```{code_language}\n{text}\n```\n"


def _convert_sub(*, text: str, sub_symbol: str) -> str:
    prefix, suffix, text = chomp(text)
    if not text:
        return ""
    return f"{prefix}{sub_symbol}{text}{sub_symbol}{suffix}"


def _convert_sup(*, text: str, sup_symbol: str) -> str:
    prefix, suffix, text = chomp(text)
    if not text:
        return ""
    return f"{prefix}{sup_symbol}{text}{sup_symbol}{suffix}"


def _convert_td(*, tag: Tag, text: str) -> str:
    colspan = int(tag.get("colspan", "1"))
    return (" " + text.strip().replace("\n", " ") + " |") * colspan


def _convert_th(*, tag: Tag, text: str) -> str:
    colspan = int(tag.get("colspan", "1"))
    return (" " + text.strip().replace("\n", " ") + " |") * colspan


def _convert_tr(*, tag: Tag, text: str) -> str:
    cells = tag.find_all(["td", "th"])
    is_head_row = all(cell.name == "th" for cell in cells)
    overline = underline = ""
    if is_head_row and not tag.previous_sibling:
        full_colspan = sum(int(cell.get("colspan", 1)) for cell in cells)
        underline = f"| {' | '.join(['---'] * full_colspan)} |\n"
    elif not tag.previous_sibling and tag.parent.name in {"table", "tbody"}:
        overline = f"| {' | '.join([''] * len(cells))} |\n| {' | '.join(['---'] * len(cells))} |\n"
    return f"{overline}|{text}\n{underline}"


def create_converters_map(
    auto_links: bool,
    bullets: str,
    code_language: str,
    code_language_callback: Callable[[Any], str] | None,
    default_title: bool,
    heading_style: str,
    keep_inline_images_in: list[str] | None,
    newline_style: str,
    strong_em_symbol: str,
    sub_symbol: str,
    sup_symbol: str,
    wrap: bool,
    wrap_width: int,
    convert_as_inline: bool,
) -> ConvertsMap:
    """Create a mapping of HTML elements to their corresponding conversion functions.

    Args:
        auto_links: Whether to convert URLs into links.
        bullets: The bullet characters to use for unordered lists.
        code_language: The default code language to use.
        code_language_callback: A callback to get the code language.
        default_title: Whether to use the URL as the title for links.
        heading_style: The style of headings.
        keep_inline_images_in: The tags to keep inline images in.
        newline_style: The style of newlines.
        strong_em_symbol: The symbol to use for strong and emphasis text.
        sub_symbol: The symbol to use for subscript text.
        sup_symbol: The symbol to use for superscript text.
        wrap: Whether to wrap text.
        wrap_width: The width to wrap text at.
        convert_as_inline: Whether to convert elements as inline elements.

    Returns:
        A mapping of HTML elements to their corresponding conversion functions
    """

    def _wrapper(func: Callable) -> Callable[[str, Tag], str]:
        spec = getfullargspec(func)

        def _inner(*, text: str, tag: Tag) -> str:
            if spec.kwonlyargs:
                kwargs = {}
                if "tag" in spec.kwonlyargs:
                    kwargs["tag"] = tag
                if "text" in spec.kwonlyargs:
                    kwargs["text"] = text
                return func(**kwargs)
            return func(text)

        return _inner

    return {
        "a": partial(_convert_a, auto_links=auto_links, default_title=default_title),
        "b": _wrapper(partial(_create_inline_converter(2 * strong_em_symbol))),
        "blockquote": _wrapper(partial(_convert_blockquote, convert_as_inline=convert_as_inline)),
        "br": _wrapper(partial(_convert_br, convert_as_inline=convert_as_inline, newline_style=newline_style)),
        "code": _create_inline_converter("`"),
        "del": _create_inline_converter("~~"),
        "em": _create_inline_converter(strong_em_symbol),
        "h1": _wrapper(partial(_convert_hn, n=1, heading_style=heading_style, convert_as_inline=convert_as_inline)),
        "h2": _wrapper(partial(_convert_hn, n=2, heading_style=heading_style, convert_as_inline=convert_as_inline)),
        "h3": _wrapper(partial(_convert_hn, n=3, heading_style=heading_style, convert_as_inline=convert_as_inline)),
        "h4": _wrapper(partial(_convert_hn, n=4, heading_style=heading_style, convert_as_inline=convert_as_inline)),
        "h5": _wrapper(partial(_convert_hn, n=5, heading_style=heading_style, convert_as_inline=convert_as_inline)),
        "h6": _wrapper(partial(_convert_hn, n=6, heading_style=heading_style, convert_as_inline=convert_as_inline)),
        "hr": _wrapper(lambda _: "\n\n---\n\n"),
        "i": _wrapper(partial(_create_inline_converter(strong_em_symbol))),
        "img": _wrapper(
            partial(_convert_img, convert_as_inline=convert_as_inline, keep_inline_images_in=keep_inline_images_in)
        ),
        "list": _convert_list,
        "ul": _convert_list,
        "ol": _convert_list,
        "li": partial(_convert_li, bullets=bullets),
        "p": _wrapper(partial(_convert_p, wrap=wrap, wrap_width=wrap_width, convert_as_inline=convert_as_inline)),
        "pre": partial(_convert_pre, code_language=code_language, code_language_callback=code_language_callback),
        "script": _wrapper(lambda _: ""),
        "style": _wrapper(lambda _: ""),
        "s": _create_inline_converter("~~"),
        "strong": _create_inline_converter(strong_em_symbol * 2),
        "samp": _create_inline_converter("`"),
        "sub": _create_inline_converter(sub_symbol),
        "sup": _create_inline_converter(sup_symbol),
        "table": _wrapper(lambda text: f"\n\n{text}\n"),
        "caption": _wrapper(lambda text: f"{text}\n"),
        "figcaption": _wrapper(lambda text: f"\n\n{text}\n\n"),
        "td": _convert_td,
        "th": _convert_th,
        "tr": _convert_tr,
        "kbd": _create_inline_converter("`"),
    }