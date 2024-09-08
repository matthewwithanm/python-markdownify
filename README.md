# html_to_markdown

This library is a refactored and modernized fork of [markdownify](https://pypi.org/project/markdownify/), supporting
Python 3.9 and offering strong typing.

### Differences from the Markdownify

- The refactored codebase uses a strict functional approach - no classes are involved.
- There is full typing with strict MyPy adherence in place.
- All original tests pass.
- This library releases follows standard semver. Its version v1.0.0 was branched from markdownify's v0.13.1, at which
  point versioning is no longer aligned.

## Installation

```shell
pip install html_to_markdown
```

## Usage

Convert some HTML to Markdown:

```python
from html_to_markdown import convert_to_markdown

convert_to_markdown('<b>Yay</b> <a href="http://github.com">GitHub</a>')  # > '**Yay** [GitHub](http://github.com)'
```

Specify tags to exclude:

```python
from html_to_markdown import convert_to_markdown

convert_to_markdown('<b>Yay</b> <a href="http://github.com">GitHub</a>', strip=['a'])  # > '**Yay** GitHub'
```

\...or specify the tags you want to include:

```python
from html_to_markdown import convert_to_markdown

convert_to_markdown('<b>Yay</b> <a href="http://github.com">GitHub</a>', convert=['b'])  # > '**Yay** GitHub'
```

# Options

html_to_markdown supports the following options:

strip

:   A list of tags to strip. This option can\'t be used with the
`convert` option.

convert

:   A list of tags to convert. This option can\'t be used with the
`strip` option.

autolinks

:   A boolean indicating whether the \"automatic link\" style should be
used when a `a` tag\'s contents match its href. Defaults to `True`.

default_title

:   A boolean to enable setting the title of a link to its href, if no
title is given. Defaults to `False`.

heading_style

:   Defines how headings should be converted. Accepted values are `ATX`,
`ATX_CLOSED`, `SETEXT`, and `UNDERLINED` (which is an alias for
`SETEXT`). Defaults to `UNDERLINED`.

bullets

:   An iterable (string, list, or tuple) of bullet styles to be used. If
the iterable only contains one item, it will be used regardless of
how deeply lists are nested. Otherwise, the bullet will alternate
based on nesting level. Defaults to `'*+-'`.

strong_em_symbol

:   In markdown, both `*` and `_` are used to encode **strong** or
*emphasized* texts. Either of these symbols can be chosen by the
options `ASTERISK` (default) or `UNDERSCORE` respectively.

sub_symbol, sup_symbol

:   Define the chars that surround `<sub>` and `<sup>` text. Defaults to
an empty string, because this is non-standard behavior. Could be
something like `~` and `^` to result in `~sub~` and `^sup^`. If the
value starts with `<` and ends with `>`, it is treated as an HTML
tag and a `/` is inserted after the `<` in the string used after the
text; this allows specifying `<sub>` to use raw HTML in the output
for subscripts, for example.

newline_style

:   Defines the style of marking linebreaks (`<br>`) in markdown. The
default value `SPACES` of this option will adopt the usual two
spaces and a newline, while `BACKSLASH` will convert a linebreak to
`\\n` (a backslash and a newline). While the latter convention is
non-standard, it is commonly preferred and supported by a lot of
interpreters.

code_language

:   Defines the language that should be assumed for all `<pre>`
sections. Useful, if all code on a page is in the same programming
language and should be annotated with ``[python]{.title-ref}[ or
similar. Defaults to ]{.title-ref}[\'\']{.title-ref}\` (empty
string) and can be any string.

code_language_callback

:   When the HTML code contains `pre` tags that in some way provide the
code language, for example as class, this callback can be used to
extract the language from the tag and prefix it to the converted
`pre` tag. The callback gets one single argument, an BeautifylSoup
object, and returns a string containing the code language, or
`None`. An example to use the class name as code language could be:

        def callback(el):
            return el['class'][0] if el.has_attr('class') else None

    Defaults to `None`.

escape_asterisks

:   If set to `False`, do not escape `*` to `\*` in text. Defaults to
`True`.

escape_underscores

:   If set to `False`, do not escape `_` to `\_` in text. Defaults to
`True`.

escape_misc

:   If set to `False`, do not escape miscellaneous punctuation
characters that sometimes have Markdown significance in text.
Defaults to `True`.

keep_inline_images_in

:   Images are converted to their alt-text when the images are located
inside headlines or table cells. If some inline images should be
converted to markdown images instead, this option can be set to a
list of parent tags that should be allowed to contain inline images,
for example `['td']`. Defaults to an empty list.

wrap, wrap_width

:   If `wrap` is set to `True`, all text paragraphs are wrapped at
`wrap_width` characters. Defaults to `False` and `80`. Use with
`newline_style=BACKSLASH` to keep line breaks in paragraphs.

Options may be specified as kwargs to the `html_to_markdown` function, or as
a nested `Options` class in `MarkdownConverter` subclasses.

# CLI

Use `html_to_markdown example.html > example.md` or pipe input from stdin
(`cat example.html | html_to_markdown > example.md`). Call `html_to_markdown -h`
to see all available options. They are the same as listed above and take
the same arguments.
