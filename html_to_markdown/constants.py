from __future__ import annotations

import re
from re import Pattern
from typing import Final

convert_heading_re: Final[Pattern[str]] = re.compile(r"convert_h(\d+)")
line_beginning_re: Final[Pattern[str]] = re.compile(r"^", re.MULTILINE)
whitespace_re: Final[Pattern[str]] = re.compile(r"[\t ]+")
html_heading_re: Final[Pattern[str]] = re.compile(r"h[1-6]")

ASTERISK: Final = "*"
ATX: Final = "atx"
ATX_CLOSED: Final = "atx_closed"
BACKSLASH: Final = "backslash"
UNDERLINED: Final = "underlined"
SPACES: Final = "spaces"
UNDERSCORE: Final = "_"
