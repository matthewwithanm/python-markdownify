from markdownify import MarkdownConverter


# for unit testing, disable document-level stripping by default so that
# separation newlines are included in testing
def md(html, **options):
    options = {"strip_document": None, **options}

    return MarkdownConverter(**options).convert(html)
