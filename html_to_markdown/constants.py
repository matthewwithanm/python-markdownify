from __future__ import annotations

import re
from re import Pattern
from typing import Final, Literal

convert_heading_re: Final[Pattern[str]] = re.compile(r"convert_h(\d+)")
line_beginning_re: Final[Pattern[str]] = re.compile(r"^", re.MULTILINE)
whitespace_re: Final[Pattern[str]] = re.compile(r"[\t ]+")
html_heading_re: Final[Pattern[str]] = re.compile(r"h[1-6]")

ASTERISK: Final[Literal["*"]] = "*"
ATX: Final[Literal["atx"]] = "atx"
ATX_CLOSED: Final[Literal["atx_closed"]] = "atx_closed"
BACKSLASH: Final[Literal["backslash"]] = "backslash"
UNDERLINED: Final[Literal["underlined"]] = "underlined"
SPACES: Final[Literal["spaces"]] = "spaces"
UNDERSCORE: Final[Literal["_"]] = "_"
