import sys

if __name__ == "__main__":
    from html_to_markdown.cli import main

    try:
        result = main(sys.argv[1:])
        print(result)  # noqa: T201
    except ValueError as e:
        print(str(e), file=sys.stderr)  # noqa: T201
        sys.exit(1)
