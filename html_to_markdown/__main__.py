import argparse
import sys

from html_to_markdown import convert_to_markdown
from html_to_markdown.constants import ASTERISK, ATX, ATX_CLOSED, BACKSLASH, SPACES, UNDERLINED, UNDERSCORE


def cli(argv: list[str]) -> None:
    """Command-line interface for html_to_markdown."""
    parser = argparse.ArgumentParser(
        prog="html_to_markdown",
        description="Converts html to markdown.",
    )

    parser.add_argument(
        "html",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="The html file to convert. Defaults to STDIN if not " "provided.",
    )
    parser.add_argument(
        "-s",
        "--strip",
        nargs="*",
        help="A list of tags to strip. This option can't be used with " "the --convert option.",
    )
    parser.add_argument(
        "-c",
        "--convert",
        nargs="*",
        help="A list of tags to convert. This option can't be used with " "the --strip option.",
    )
    parser.add_argument(
        "-a",
        "--autolinks",
        action="store_true",
        help="A boolean indicating whether the 'automatic link' style "
        "should be used when a 'a' tag's contents match its href.",
    )
    parser.add_argument(
        "--default-title",
        action="store_false",
        help="A boolean to enable setting the title of a link to its " "href, if no title is given.",
    )
    parser.add_argument(
        "--heading-style",
        default=UNDERLINED,
        choices=(ATX, ATX_CLOSED, UNDERLINED),
        help="Defines how headings should be converted.",
    )
    parser.add_argument(
        "-b",
        "--bullets",
        default="*+-",
        help="A string of bullet styles to use; the bullet will " "alternate based on nesting level.",
    )
    (
        parser.add_argument(
            "--strong-em-symbol",
            default=ASTERISK,
            choices=(ASTERISK, UNDERSCORE),
            help="Use * or _ to convert strong and italics text",
        ),
    )
    parser.add_argument("--sub-symbol", default="", help="Define the chars that surround '<sub>'.")
    parser.add_argument("--sup-symbol", default="", help="Define the chars that surround '<sup>'.")
    parser.add_argument(
        "--newline-style",
        default=SPACES,
        choices=(SPACES, BACKSLASH),
        help="Defines the style of <br> conversions: two spaces "
        "or backslash at the and of the line thet should break.",
    )
    parser.add_argument(
        "--code-language", default="", help="Defines the language that should be assumed for all " "'<pre>' sections."
    )
    parser.add_argument(
        "--no-escape-asterisks",
        dest="escape_asterisks",
        action="store_false",
        help="Do not escape '*' to '\\*' in text.",
    )
    parser.add_argument(
        "--no-escape-underscores",
        dest="escape_underscores",
        action="store_false",
        help="Do not escape '_' to '\\_' in text.",
    )
    parser.add_argument(
        "-i",
        "--keep-inline-images-in",
        nargs="*",
        help="Images are converted to their alt-text when the images are "
        "located inside headlines or table cells. If some inline images "
        "should be converted to markdown images instead, this option can "
        "be set to a list of parent tags that should be allowed to "
        "contain inline images.",
    )
    parser.add_argument(
        "-w", "--wrap", action="store_true", help="Wrap all text paragraphs at --wrap-width characters."
    )
    parser.add_argument("--wrap-width", type=int, default=80)

    args = parser.parse_args(argv)

    result = convert_to_markdown(
        args.html.read(),
        strip=args.strip,
        convert=args.convert,
        autolinks=args.autolinks,
        default_title=args.default_title,
        heading_style=args.heading_style,
        bullets=args.bullets,
        strong_em_symbol=args.strong_em_symbol,
        sub_symbol=args.sub_symbol,
        sup_symbol=args.sup_symbol,
        newline_style=args.newline_style,
        code_language=args.code_language,
        escape_asterisks=args.escape_asterisks,
        escape_underscores=args.escape_underscores,
        keep_inline_images_in=args.keep_inline_images_in,
        wrap=args.wrap,
        wrap_width=args.wrap_width,
    )

    print(result)  # noqa: T201


if __name__ == "__main__":
    cli(sys.argv[1:])
