from _typeshed import Incomplete
from typing import Callable

ATX: str
ATX_CLOSED: str
UNDERLINED: str
SETEXT = UNDERLINED
SPACES: str
BACKSLASH: str
ASTERISK: str
UNDERSCORE: str
LSTRIP: str
RSTRIP: str
STRIP: str
STRIP_ONE: str


def markdownify(
    html: str,
    autolinks: bool = ...,
    bs4_options: str = ...,
    bullets: str = ...,
    code_language: str = ...,
    code_language_callback: Callable[[Incomplete], str | None] | None = ...,
    convert: list[str] | None = ...,
    default_title: bool = ...,
    escape_asterisks: bool = ...,
    escape_underscores: bool = ...,
    escape_misc: bool = ...,
    heading_style: str = ...,
    keep_inline_images_in: list[str] = ...,
    newline_style: str = ...,
    strip: list[str] | None = ...,
    strip_document: str | None = ...,
    strip_pre: str = ...,
    strong_em_symbol: str = ...,
    sub_symbol: str = ...,
    sup_symbol: str = ...,
    table_infer_header: bool = ...,
    wrap: bool = ...,
    wrap_width: int = ...,
) -> str: ...


class MarkdownConverter:
    def __init__(
        self,
        autolinks: bool = ...,
        bs4_options: str = ...,
        bullets: str = ...,
        code_language: str = ...,
        code_language_callback: Callable[[Incomplete], str | None] | None = ...,
        convert: list[str] | None = ...,
        default_title: bool = ...,
        escape_asterisks: bool = ...,
        escape_underscores: bool = ...,
        escape_misc: bool = ...,
        heading_style: str = ...,
        keep_inline_images_in: list[str] = ...,
        newline_style: str = ...,
        strip: list[str] | None = ...,
        strip_document: str | None = ...,
        strip_pre: str = ...,
        strong_em_symbol: str = ...,
        sub_symbol: str = ...,
        sup_symbol: str = ...,
        table_infer_header: bool = ...,
        wrap: bool = ...,
        wrap_width: int = ...,
    ) -> None:
        ...
  
    def convert(self, html: str) -> str:
        ...

    def convert_soup(self, soup: Incomplete) -> str:
        ...