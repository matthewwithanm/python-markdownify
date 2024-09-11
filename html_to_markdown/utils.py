from __future__ import annotations

import re

from html_to_markdown.constants import line_beginning_re


def chomp(text: str) -> tuple[str, str, str]:
    """If the text in an inline tag like b, a, or em contains a leading or trailing
    space, strip the string and return a space as suffix of prefix, if needed.

    Args:
        text: The text to chomp.

    Returns:
        A tuple containing the prefix, suffix, and the stripped text.
    """
    prefix = " " if text and text[0] == " " else ""
    suffix = " " if text and text[-1] == " " else ""
    text = text.strip()
    return prefix, suffix, text


def escape(*, text: str, escape_misc: bool, escape_asterisks: bool, escape_underscores: bool) -> str:
    """Escape special characters in text.

    Args:
        text: The text to escape.
        escape_misc: Whether to escape miscellaneous characters.
        escape_asterisks: Whether to escape asterisks.
        escape_underscores: Whether to escape underscores.

    Returns:
        The escaped text.
    """
    if not text:
        return ""
    if escape_misc:
        text = re.sub(r"([\\&<`[>~#=+|-])", r"\\\1", text)
        text = re.sub(r"([0-9])([.)])", r"\1\\\2", text)
    if escape_asterisks:
        text = text.replace("*", r"\*")
    if escape_underscores:
        text = text.replace("_", r"\_")
    return text


def indent(*, text: str, level: int) -> str:
    """Indent text by a given level.

    Args:
        text: The text to indent.
        level: The level of indentation.

    Returns:
        The indented text.
    """
    return line_beginning_re.sub("\t" * level, text) if text else ""


def underline(*, text: str, pad_char: str) -> str:
    """Underline text with a given character.

    Args:
        text: The text to underline.
        pad_char: The character to use for underlining.

    Returns:
        The underlined text.
    """
    text = (text or "").rstrip()
    return f"{text}\n{pad_char * len(text)}\n\n" if text else ""
