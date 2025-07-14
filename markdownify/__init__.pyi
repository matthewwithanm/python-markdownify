from _typeshed import Incomplete
from typing import TypedDict, Unpack

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


class Options(TypedDict, total=False):
  autolinks: bool
  bs4_options: str
  bullets: str  # An iterable of bullet types.
  code_language: str
  code_language_callback: Incomplete | None
  convert: list[str] | None
  default_title: bool
  escape_asterisks: bool
  escape_underscores: bool
  escape_misc: bool
  heading_style: str
  keep_inline_images_in: list[str]
  newline_style: str
  strip: list[str] | None
  strip_document: str | None
  strip_pre: str
  strong_em_symbol: str
  sub_symbol: str
  sup_symbol: str
  table_infer_header: bool
  wrap: bool
  wrap_width: int


def markdownify(html: str, **kwargs: Unpack[Options]) -> str: ...


class MarkdownConverter:
  def __init__(self, **kwargs: Unpack[Options]) -> None:
    ...
  
  def convert(self, html: str) -> str:
    ...
