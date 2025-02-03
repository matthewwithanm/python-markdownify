from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import partial
from inspect import getfullargspec
from textwrap import fill
from typing import Any, Callable, Literal, TypeVar, cast

from bs4.element import Tag

from html_to_markdown.constants import (
    ATX_CLOSED,
    BACKSLASH,
    UNDERLINED,
    line_beginning_re,
)
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

ConvertersMap = Mapping[SupportedElements, Callable[[str, Tag], str]]

T = TypeVar("T")


def _create_inline_converter(markup_prefix: str) -> Callable[[Tag, str], str]:
    """Create an inline converter for a markup pattern or tag.

    Args:
        markup_prefix: The markup prefix to insert.

    Returns:
        A function that can be used to convert HTML to Markdown.
    """

    def implementation(*, tag: Tag, text: str) -> str:
        if tag.find_parent(["pre", "code", "kbd", "samp"]):
            return text

        if not text.strip():
            return ""

        markup_suffix = markup_prefix
        if markup_prefix.startswith("<") and markup_prefix.endswith(">"):
            markup_suffix = "</" + markup_prefix[1:]

        prefix, suffix, text = chomp(text)

        return f"{prefix}{markup_prefix}{text}{markup_suffix}{suffix}"

    return cast(Callable[[Tag, str], str], implementation)


def _get_colspan(tag: Tag) -> int:
    colspan = 1

    if "colspan" in tag.attrs and isinstance(tag["colspan"], str) and tag["colspan"].isdigit():
        colspan = int(tag["colspan"])

    return colspan


def _convert_a(*, tag: Tag, text: str, autolinks: bool, default_title: bool) -> str:
    prefix, suffix, text = chomp(text)
    if not text:
        return ""

    href = tag.get("href")
    title = tag.get("title")

    if autolinks and text.replace(r"\_", "_") == href and not title and not default_title:
        return f"<{href}>"

    if default_title and not title:
        title = href

    title_part = ' "{}"'.format(title.replace('"', r"\"")) if isinstance(title, str) else ""
    return f"{prefix}[{text}]({href}{title_part}){suffix}" if href else text


def _convert_blockquote(*, text: str, convert_as_inline: bool) -> str:
    if convert_as_inline:
        return text
    return f"\n{line_beginning_re.sub('> ', text.strip())}\n\n" if text else ""


def _convert_br(*, convert_as_inline: bool, newline_style: str) -> str:
    if convert_as_inline:
        return ""
    return "\\\n" if newline_style.lower() == BACKSLASH else "  \n"


def _convert_hn(
    *,
    n: int,
    heading_style: Literal["atx", "atx_closed", "underlined"],
    text: str,
    convert_as_inline: bool,
) -> str:
    if convert_as_inline:
        return text

    text = text.strip()
    if heading_style == UNDERLINED and n <= 2:
        return underline(text=text, pad_char="=" if n == 1 else "-")

    hashes = "#" * n
    if heading_style == ATX_CLOSED:
        return f"{hashes} {text} {hashes}\n\n"

    return f"{hashes} {text}\n\n"


def _convert_img(*, tag: Tag, convert_as_inline: bool, keep_inline_images_in: Iterable[str] | None) -> str:
    alt = tag.attrs.get("alt", "")
    src = tag.attrs.get("src", "")
    title = tag.attrs.get("title", "")
    title_part = ' "{}"'.format(title.replace('"', r"\"")) if title else ""
    parent_name = tag.parent.name if tag.parent else ""
    if convert_as_inline and parent_name not in (keep_inline_images_in or []):
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

        if not tag.parent:
            break

        tag = tag.parent

    if nested:
        return "\n" + indent(text=text, level=1).rstrip()

    return text + ("\n" if before_paragraph else "")


def _convert_li(*, tag: Tag, text: str, bullets: str) -> str:
    parent = tag.parent
    if parent is not None and parent.name == "ol":
        start = (
            int(cast(str, parent["start"]))
            if isinstance(parent.get("start"), str) and str(parent.get("start")).isnumeric()
            else 1
        )
        bullet = "%s." % (start + parent.index(tag))
    else:
        depth = -1
        while tag:
            if tag.name == "ul":
                depth += 1
            if not tag.parent:
                break

            tag = tag.parent

        bullet = bullets[depth % len(bullets)]
    return "{} {}\n".format(bullet, (text or "").strip())


def _convert_p(*, wrap: bool, text: str, convert_as_inline: bool, wrap_width: int) -> str:
    if convert_as_inline:
        return text

    if wrap:
        text = fill(
            text,
            width=wrap_width,
            break_long_words=False,
            break_on_hyphens=False,
        )

    return f"{text}\n\n" if text else ""


def _convert_pre(
    *,
    tag: Tag,
    text: str,
    code_language: str,
    code_language_callback: Callable[[Tag], str] | None,
) -> str:
    if not text:
        return ""

    if code_language_callback:
        code_language = code_language_callback(tag) or code_language

    return f"\n```{code_language}\n{text}\n```\n"


def _convert_td(*, tag: Tag, text: str) -> str:
    colspan = _get_colspan(tag)
    return " " + text.strip().replace("\n", " ") + " |" * colspan


def _convert_th(*, tag: Tag, text: str) -> str:
    colspan = _get_colspan(tag)
    return " " + text.strip().replace("\n", " ") + " |" * colspan


def _convert_tr(*, tag: Tag, text: str) -> str:
    cells = tag.find_all(["td", "th"])
    parent_name = tag.parent.name if tag.parent else ""
    tag_grand_parent = tag.parent.parent if tag.parent else None
    is_headrow = (
        all(cell.name == "th" for cell in cells)
        or (not tag.previous_sibling and parent_name != "tbody")
        or (
            not tag.previous_sibling
            and parent_name == "tbody"
            and (not tag_grand_parent or len(tag_grand_parent.find_all(["thead"])) < 1)
        )
    )
    overline = ""
    underline = ""
    if is_headrow and not tag.previous_sibling:
        # first row and is headline: print headline underline
        full_colspan = 0
        for cell in cells:
            if "colspan" in cell.attrs and cell["colspan"].isdigit():
                full_colspan += int(cell["colspan"])
            else:
                full_colspan += 1
        underline += "| " + " | ".join(["---"] * full_colspan) + " |" + "\n"
    elif not tag.previous_sibling and (
        parent_name == "table" or (parent_name == "tbody" and not cast(Tag, tag.parent).previous_sibling)
    ):
        # first row, not headline, and:
        # - the parent is table or
        # - the parent is tbody at the beginning of a table.
        # print empty headline above this row
        overline += "| " + " | ".join([""] * len(cells)) + " |" + "\n"
        overline += "| " + " | ".join(["---"] * len(cells)) + " |" + "\n"
    return overline + "|" + text + "\n" + underline


def create_converters_map(
    autolinks: bool,
    bullets: str,
    code_language: str,
    code_language_callback: Callable[[Tag], str] | None,
    default_title: bool,
    heading_style: Literal["atx", "atx_closed", "underlined"],
    keep_inline_images_in: Iterable[str] | None,
    newline_style: str,
    strong_em_symbol: str,
    sub_symbol: str,
    sup_symbol: str,
    wrap: bool,
    wrap_width: int,
) -> ConvertersMap:
    """Create a mapping of HTML elements to their corresponding conversion functions.

    Args:
        autolinks: Whether to convert URLs into links.
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

    Returns:
        A mapping of HTML elements to their corresponding conversion functions
    """

    def _wrapper(func: Callable[..., T]) -> Callable[[str, Tag], T]:
        spec = getfullargspec(func)

        def _inner(*, text: str, tag: Tag, convert_as_inline: bool) -> T:
            if spec.kwonlyargs:
                kwargs: dict[str, Any] = {}
                if "tag" in spec.kwonlyargs:
                    kwargs["tag"] = tag
                if "text" in spec.kwonlyargs:
                    kwargs["text"] = text
                if "convert_as_inline" in spec.kwonlyargs:
                    kwargs["convert_as_inline"] = convert_as_inline
                return func(**kwargs)
            return func(text)

        return cast(Callable[[str, Tag], T], _inner)

    return {
        "a": _wrapper(partial(_convert_a, autolinks=autolinks, default_title=default_title)),
        "b": _wrapper(partial(_create_inline_converter(2 * strong_em_symbol))),
        "blockquote": _wrapper(partial(_convert_blockquote)),
        "br": _wrapper(partial(_convert_br, newline_style=newline_style)),
        "code": _wrapper(_create_inline_converter("`")),
        "del": _wrapper(_create_inline_converter("~~")),
        "em": _wrapper(_create_inline_converter(strong_em_symbol)),
        "h1": _wrapper(partial(_convert_hn, n=1, heading_style=heading_style)),
        "h2": _wrapper(partial(_convert_hn, n=2, heading_style=heading_style)),
        "h3": _wrapper(partial(_convert_hn, n=3, heading_style=heading_style)),
        "h4": _wrapper(partial(_convert_hn, n=4, heading_style=heading_style)),
        "h5": _wrapper(partial(_convert_hn, n=5, heading_style=heading_style)),
        "h6": _wrapper(partial(_convert_hn, n=6, heading_style=heading_style)),
        "hr": _wrapper(lambda _: "\n\n---\n\n"),
        "i": _wrapper(partial(_create_inline_converter(strong_em_symbol))),
        "img": _wrapper(partial(_convert_img, keep_inline_images_in=keep_inline_images_in)),
        "list": _wrapper(_convert_list),
        "ul": _wrapper(_convert_list),
        "ol": _wrapper(_convert_list),
        "li": _wrapper(partial(_convert_li, bullets=bullets)),
        "p": _wrapper(partial(_convert_p, wrap=wrap, wrap_width=wrap_width)),
        "pre": _wrapper(
            partial(
                _convert_pre,
                code_language=code_language,
                code_language_callback=code_language_callback,
            )
        ),
        "script": _wrapper(lambda _: ""),
        "style": _wrapper(lambda _: ""),
        "s": _wrapper(_create_inline_converter("~~")),
        "strong": _wrapper(_create_inline_converter(strong_em_symbol * 2)),
        "samp": _wrapper(_create_inline_converter("`")),
        "sub": _wrapper(_create_inline_converter(sub_symbol)),
        "sup": _wrapper(_create_inline_converter(sup_symbol)),
        "table": _wrapper(lambda text: f"\n\n{text}\n"),
        "caption": _wrapper(lambda text: f"{text}\n"),
        "figcaption": _wrapper(lambda text: f"\n\n{text}\n\n"),
        "td": _wrapper(_convert_td),
        "th": _wrapper(_convert_th),
        "tr": _wrapper(_convert_tr),
        "kbd": _wrapper(_create_inline_converter("`")),
    }
