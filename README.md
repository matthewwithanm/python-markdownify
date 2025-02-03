# html_to_markdown

This library is a refactored and modernized fork of [markdownify](https://pypi.org/project/markdownify/), supporting
Python 3.9 and above.

### Differences with the Markdownify

- The refactored codebase uses a strict functional approach - no classes are involved.
- There is full typing with strict MyPy strict adherence and a py.typed file included.
- The `convert_to_markdown` function allows passing a pre-configured instance of `BeautifulSoup` instead of html.
- This library releases follows standard semver. Its version v1.0.0 was branched from markdownify's v0.13.1, at which
  point versioning is no longer aligned.

## Installation

```shell
pip install html_to_markdown
```

## Usage

Convert an string HTML to Markdown:

```python
from html_to_markdown import convert_to_markdown

convert_to_markdown('<b>Yay</b> <a href="http://github.com">GitHub</a>')  # > '**Yay** [GitHub](http://github.com)'
```

Or pass a pre-configured instance of `BeautifulSoup`:

```python
from bs4 import BeautifulSoup
from html_to_markdown import convert_to_markdown

soup = BeautifulSoup('<b>Yay</b> <a href="http://github.com">GitHub</a>', 'lxml')  # lxml requires an extra dependency.

convert_to_markdown(soup)  # > '**Yay** [GitHub](http://github.com)'
```

### Options

The `convert_to_markdown` function accepts the following kwargs:

- autolinks (bool): Automatically convert valid URLs into Markdown links. Defaults to True.
- bullets (str): A string of characters to use for bullet points in lists. Defaults to '\*+-'.
- code_language (str): Default language identifier for fenced code blocks. Defaults to an empty string.
- code_language_callback (Callable[[Any], str] | None): Function to dynamically determine the language for code blocks.
- convert (Iterable[str] | None): A list of tag names to convert to Markdown. If None, all supported tags are converted.
- default_title (bool): Use the default title when converting certain elements (e.g., links). Defaults to False.
- escape_asterisks (bool): Escape asterisks (\*) to prevent unintended Markdown formatting. Defaults to True.
- escape_misc (bool): Escape miscellaneous characters to prevent conflicts in Markdown. Defaults to True.
- escape*underscores (bool): Escape underscores (*) to prevent unintended italic formatting. Defaults to True.
- heading_style (Literal["underlined", "atx", "atx_closed"]): The style to use for Markdown headings. Defaults to "
  underlined".
- keep_inline_images_in (Iterable[str] | None): Tags in which inline images should be preserved. Defaults to None.
- newline_style (Literal["spaces", "backslash"]): Style for handling newlines in text content. Defaults to "spaces".
- strip (Iterable[str] | None): Tags to strip from the output. Defaults to None.
- strong*em_symbol (Literal["\*", "*"]): Symbol to use for strong/emphasized text. Defaults to "\*".
- sub_symbol (str): Custom symbol for subscript text. Defaults to an empty string.
- sup_symbol (str): Custom symbol for superscript text. Defaults to an empty string.
- wrap (bool): Wrap text to the specified width. Defaults to False.
- wrap_width (int): The number of characters at which to wrap text. Defaults to 80.
- convert_as_inline (bool): Treat the content as inline elements (no block elements like paragraphs). Defaults to False.

## CLI

For compatibility with the original markdownify, a CLI is provided. Use `html_to_markdown example.html > example.md` or
pipe input from stdin:

```shell
cat example.html | html_to_markdown > example.md
```

Use `html_to_markdown -h` to see all available options. They are the same as listed above and take the same arguments.
