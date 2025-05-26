from _typeshed import Incomplete

def markdownify(
  html: str,
  strip: list[str] = ...,
  convert: list[str] = ...,
  autolinks: bool = ...,
  bullets: str = ...,  # An iterable of bullet types.
  code_language: str = ...,
  code_language_callback: Incomplete = ...,
  default_title: bool = ...,
  escape_asterisks: bool = ...,
  escape_underscores: bool = ...,
  escape_misc: bool = ...,
  heading_style: str = ...,
  keep_inline_images_in: list[str] = ...,
  newline_style: str = ...,
  strip_document: str = ...,
  strong_em_symbol: str = ...,
  sub_symbol: str = ...,
  sup_symbol: str = ...,
  table_infer_header: bool = ...,
  wrap: bool = ...,
  wrap_width: int = ...,
) -> str: ...
