from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from html_to_markdown.constants import ASTERISK, SPACES, UNDERLINED
from html_to_markdown.converters import create_converters_map

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from bs4 import Tag


def _create_legacy_class(
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
) -> type:
    """Create a legacy class for Markdownify.

    Deprecated: Use the new hooks api instead.

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
        A class that can be used to convert HTML to Markdown.
    """
    return type(
        "Markdownify",
        (),
        {
            k.removeprefix("_"): v
            for k, v in create_converters_map(
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
            ).items()
        },
    )


Markdownify = _create_legacy_class(
    autolinks=True,
    bullets="*+-",
    code_language="",
    code_language_callback=None,
    default_title=False,
    heading_style=UNDERLINED,
    keep_inline_images_in=None,
    newline_style=SPACES,
    strong_em_symbol=ASTERISK,
    sub_symbol="",
    sup_symbol="",
    wrap=False,
    wrap_width=80,
)
