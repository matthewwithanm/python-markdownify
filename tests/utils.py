from markdownify import MarkdownConverter
from selectolax.lexbor import LexborHTMLParser


# for unit testing, disable document-level stripping by default so that
# separation newlines are included in testing
def md(html: str, **options):
    options = {"strip_document": None, **options}

    return MarkdownConverter(**options).convert_soup(LexborHTMLParser(html).body)
