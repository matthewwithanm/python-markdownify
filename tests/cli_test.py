from collections.abc import Generator
from io import StringIO
from unittest.mock import Mock, mock_open, patch

import pytest

from html_to_markdown.cli import main


@pytest.fixture
def mock_convert_to_markdown() -> Generator[Mock, None, None]:
    with patch("html_to_markdown.processing.convert_to_markdown") as mock:
        mock.return_value = "Mocked Markdown Output"
        yield mock


@pytest.fixture
def mock_stdin() -> Generator[None, None, None]:
    with patch("sys.stdin", new=StringIO("<html><body><p>Test from stdin</p></body></html>")):
        yield


def test_main_with_file_input(mock_convert_to_markdown: Mock) -> None:
    test_html = "<html><body><h1>Test</h1></body></html>"
    with patch("builtins.open", mock_open(read_data=test_html)):
        result = main(["input.html"])

    assert result == "Mocked Markdown Output"
    mock_convert_to_markdown.assert_called_once_with(
        test_html,
        strip=None,
        convert=None,
        autolinks=False,
        default_title=True,
        heading_style="underlined",
        bullets="*+-",
        strong_em_symbol="*",
        sub_symbol="",
        sup_symbol="",
        newline_style="spaces",
        code_language="",
        escape_asterisks=True,
        escape_underscores=True,
        keep_inline_images_in=None,
        wrap=False,
        wrap_width=80,
    )


def test_main_with_stdin_input(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    result = main([])

    assert result == "Mocked Markdown Output"
    mock_convert_to_markdown.assert_called_once_with(
        "<html><body><p>Test from stdin</p></body></html>",
        strip=None,
        convert=None,
        autolinks=False,
        default_title=True,
        heading_style="underlined",
        bullets="*+-",
        strong_em_symbol="*",
        sub_symbol="",
        sup_symbol="",
        newline_style="spaces",
        code_language="",
        escape_asterisks=True,
        escape_underscores=True,
        keep_inline_images_in=None,
        wrap=False,
        wrap_width=80,
    )


def test_main_with_strip_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--strip", "div", "span"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["strip"] == ["div", "span"]


def test_main_with_convert_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--convert", "p", "h1"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["convert"] == ["p", "h1"]


def test_main_with_autolinks_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--autolinks"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["autolinks"] is True


def test_main_with_default_title_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--default-title"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["default_title"] is False


def test_main_with_heading_style_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--heading-style", "atx"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["heading_style"] == "atx"


def test_main_with_bullets_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--bullets", "+-*"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["bullets"] == "+-*"


def test_main_with_strong_em_symbol_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--strong-em-symbol", "_"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["strong_em_symbol"] == "_"


def test_main_with_sub_and_sup_symbol_options(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--sub-symbol", "~", "--sup-symbol", "^"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["sub_symbol"] == "~"
    assert mock_convert_to_markdown.call_args[1]["sup_symbol"] == "^"


def test_main_with_newline_style_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--newline-style", "backslash"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["newline_style"] == "backslash"


def test_main_with_code_language_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--code-language", "python"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["code_language"] == "python"


def test_main_with_no_escape_options(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--no-escape-asterisks", "--no-escape-underscores"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["escape_asterisks"] is False
    assert mock_convert_to_markdown.call_args[1]["escape_underscores"] is False


def test_main_with_keep_inline_images_in_option(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--keep-inline-images-in", "p", "div"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["keep_inline_images_in"] == ["p", "div"]


def test_main_with_wrap_options(mock_convert_to_markdown: Mock, mock_stdin: Mock) -> None:
    main(["--wrap", "--wrap-width", "100"])
    mock_convert_to_markdown.assert_called_once()
    assert mock_convert_to_markdown.call_args[1]["wrap"] is True
    assert mock_convert_to_markdown.call_args[1]["wrap_width"] == 100
