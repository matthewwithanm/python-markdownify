from markdownify import markdownify as md


def test_preprocess_all_tags():

    def preprocess(node, text, convert_as_inline):
        alignment = ""
        if 'style' in node.attrs and 'text-align' in node.attrs['style']:
            style = node.attrs['style']
            alignment = style.split("text-align:")[1].split(";")[0].strip()

        if alignment:
            return f"[align={alignment}]{text}[/align]"
        return text

    assert md(
        '<p style="text-align: center;">para</p><b style="text-align: left;">bold</b>',
        preprocess_fn=preprocess) == '\n\n[align=center]para[/align]\n\n**[align=left]bold[/align]**'


def test_postprocess_all_tags():

    def postprocess(node, text, convert_as_inline):
        alignment = ""
        if 'style' in node.attrs and 'text-align' in node.attrs['style']:
            style = node.attrs['style']
            alignment = style.split("text-align:")[1].split(";")[0].strip()

        if alignment:
            return f"[align={alignment}]{text}[/align]"
        return text
    b = md(
        '<p style="text-align: center;">para</p><b style="text-align: left;">bold</b>',
        postprocess_fn=postprocess)
    print(b)
    assert md(
        '<p style="text-align: center;">para</p><b style="text-align: left;">bold</b>',
        postprocess_fn=postprocess) == '[align=center]\n\npara\n\n[/align][align=left]**bold**[/align]'


def test_preprocess_runs_before_conversion():

    def preprocess(node, text, convert_as_inline):
        if node.name == 'b':
            return f"PRE_{text}_PRE"
        return text

    # Default conversion would make this "**bold**"
    # With preprocessing it should become "**PRE_bold_PRE**"
    assert md('<b>bold</b>', preprocess_fn=preprocess) == '**PRE_bold_PRE**'


def test_postprocess_runs_after_conversion():

    def postprocess(node, text, convert_as_inline):
        if node.name == 'b':
            return f"POST_{text}_POST"
        return text

    # Default conversion makes this "**bold**"
    # With postprocessing it should become "POST_**bold**_POST"
    assert md(
        '<b>bold</b>',
        postprocess_fn=postprocess) == 'POST_**bold**_POST'


def test_preprocess_doesnt_prevent_conversion():

    def preprocess(node, text, convert_as_inline):
        return text.upper()  # Just modify the text, don't prevent conversion

    # Should still get converted to markdown, just with uppercase content
    assert md('<b>bold</b>', preprocess_fn=preprocess) == '**BOLD**'


def test_postprocess_doesnt_prevent_conversion():

    def postprocess(node, text, convert_as_inline):
        return text.upper()  # Just modify the result, don't prevent conversion

    # Should get normal markdown conversion but then uppercased
    assert md('<b>bold</b>', postprocess_fn=postprocess) == '**BOLD**'


def test_combined_pre_and_post_processing():

    def preprocess(node, text, convert_as_inline):
        return f"({text})"

    def postprocess(node, text, convert_as_inline):
        return f"[{text}]"

    # <b>bold</b> normally becomes "**bold**"
    # With preprocessing: "(bold)" -> "**(bold)**"
    # Then postprocessing: "[**(bold)**]"
    assert md('<b>bold</b>',
              preprocess_fn=preprocess,
              postprocess_fn=postprocess) == '[**(bold)**]'


def test_processing_with_multiple_tags():

    def preprocess(node, text, convert_as_inline):
        if node.name == 'b':
            return f"B:{text}"
        elif node.name == 'i':
            return f"I:{text}"
        return text

    # <p><b>bold</b> and <i>italic</i></p>
    # Should become "**B:bold** and *I:italic*"
    assert md('<p><b>bold</b> and <i>italic</i></p>',
              preprocess_fn=preprocess) == '\n\n**B:bold** and *I:italic*\n\n'


def test_processing_with_nested_tags():

    def postprocess(node, text, convert_as_inline):
        if node.name == 'p':
            return f"P:{text}"
        return text

    # <p><b>bold</b> text</p> normally becomes "**bold** text"
    # With postprocessing becomes "P:**bold** text"
    assert md('<p><b>bold</b> text</p>',
              postprocess_fn=postprocess) == 'P:\n\n**bold** text\n\n'
