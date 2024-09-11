import sys

from html_to_markdown.cli import cli

if __name__ == "__main__":
    result = cli(sys.argv[1:])
    print(result)  # noqa: T201
