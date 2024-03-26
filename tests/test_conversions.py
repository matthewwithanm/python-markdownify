from markdownify import markdownify as md, ATX, ATX_CLOSED, BACKSLASH, UNDERSCORE


def inline_tests(tag, markup):
    # test template for different inline tags
    assert md(f'<{tag}>Hello</{tag}>') == f'{markup}Hello{markup}'
    assert md(f'foo <{tag}>Hello</{tag}> bar') == f'foo {markup}Hello{markup} bar'
    assert md(f'foo<{tag}> Hello</{tag}> bar') == f'foo {markup}Hello{markup} bar'
    assert md(f'foo <{tag}>Hello </{tag}>bar') == f'foo {markup}Hello{markup} bar'
    assert md(f'foo <{tag}></{tag}> bar') in ['foo  bar', 'foo bar']  # Either is OK


def test_a():
    assert md('<a href="https://google.com">Google</a>') == '[Google](https://google.com)'
    assert md('<a href="https://google.com">https://google.com</a>') == '<https://google.com>'
    assert md('<a href="https://community.kde.org/Get_Involved">https://community.kde.org/Get_Involved</a>') == '<https://community.kde.org/Get_Involved>'
    assert md('<a href="https://community.kde.org/Get_Involved">https://community.kde.org/Get_Involved</a>', autolinks=False) == '[https://community.kde.org/Get\\_Involved](https://community.kde.org/Get_Involved)'


def test_a_spaces():
    assert md('foo <a href="http://google.com">Google</a> bar') == 'foo [Google](http://google.com) bar'
    assert md('foo<a href="http://google.com"> Google</a> bar') == 'foo [Google](http://google.com) bar'
    assert md('foo <a href="http://google.com">Google </a>bar') == 'foo [Google](http://google.com) bar'
    assert md('foo <a href="http://google.com"></a> bar') == 'foo  bar'


def test_a_with_title():
    text = md('<a href="http://google.com" title="The &quot;Goog&quot;">Google</a>')
    assert text == r'[Google](http://google.com "The \"Goog\"")'
    assert md('<a href="https://google.com">https://google.com</a>', default_title=True) == '[https://google.com](https://google.com "https://google.com")'


def test_a_shortcut():
    text = md('<a href="http://google.com">http://google.com</a>')
    assert text == '<http://google.com>'


def test_a_no_autolinks():
    assert md('<a href="https://google.com">https://google.com</a>', autolinks=False) == '[https://google.com](https://google.com)'


def test_b():
    assert md('<b>Hello</b>') == '**Hello**'


def test_b_spaces():
    assert md('foo <b>Hello</b> bar') == 'foo **Hello** bar'
    assert md('foo<b> Hello</b> bar') == 'foo **Hello** bar'
    assert md('foo <b>Hello </b>bar') == 'foo **Hello** bar'
    assert md('foo <b></b> bar') == 'foo  bar'


def test_blockquote():
    assert md('<blockquote>Hello</blockquote>') == '\n> Hello\n\n'
    assert md('<blockquote>\nHello\n</blockquote>') == '\n> Hello\n\n'


def test_blockquote_with_nested_paragraph():
    assert md('<blockquote><p>Hello</p></blockquote>') == '\n> Hello\n\n'
    assert md('<blockquote><p>Hello</p><p>Hello again</p></blockquote>') == '\n> Hello\n> \n> Hello again\n\n'


def test_blockquote_with_paragraph():
    assert md('<blockquote>Hello</blockquote><p>handsome</p>') == '\n> Hello\n\nhandsome\n\n'


def test_blockquote_nested():
    text = md('<blockquote>And she was like <blockquote>Hello</blockquote></blockquote>')
    assert text == '\n> And she was like \n> > Hello\n\n'


def test_br():
    assert md('a<br />b<br />c') == 'a  \nb  \nc'
    assert md('a<br />b<br />c', newline_style=BACKSLASH) == 'a\\\nb\\\nc'


def test_caption():
    assert md('TEXT<figure><figcaption>Caption</figcaption><span>SPAN</span></figure>') == 'TEXT\n\nCaption\n\nSPAN'
    assert md('<figure><span>SPAN</span><figcaption>Caption</figcaption></figure>TEXT') == 'SPAN\n\nCaption\n\nTEXT'


def test_code():
    inline_tests('code', '`')
    assert md('<code>*this_should_not_escape*</code>') == '`*this_should_not_escape*`'
    assert md('<kbd>*this_should_not_escape*</kbd>') == '`*this_should_not_escape*`'
    assert md('<samp>*this_should_not_escape*</samp>') == '`*this_should_not_escape*`'
    assert md('<code><span>*this_should_not_escape*</span></code>') == '`*this_should_not_escape*`'
    assert md('<code>this  should\t\tnormalize</code>') == '`this should normalize`'
    assert md('<code><span>this  should\t\tnormalize</span></code>') == '`this should normalize`'


def test_del():
    inline_tests('del', '~~')


def test_div():
    assert md('Hello</div> World') == 'Hello World'


def test_em():
    inline_tests('em', '*')


def test_header_with_space():
    assert md('<h3>\n\nHello</h3>') == '### Hello\n\n'
    assert md('<h4>\n\nHello</h4>') == '#### Hello\n\n'
    assert md('<h5>\n\nHello</h5>') == '##### Hello\n\n'
    assert md('<h5>\n\nHello\n\n</h5>') == '##### Hello\n\n'
    assert md('<h5>\n\nHello   \n\n</h5>') == '##### Hello\n\n'


def test_h1():
    assert md('<h1>Hello</h1>') == 'Hello\n=====\n\n'


def test_h2():
    assert md('<h2>Hello</h2>') == 'Hello\n-----\n\n'


def test_hn():
    assert md('<h3>Hello</h3>') == '### Hello\n\n'
    assert md('<h4>Hello</h4>') == '#### Hello\n\n'
    assert md('<h5>Hello</h5>') == '##### Hello\n\n'
    assert md('<h6>Hello</h6>') == '###### Hello\n\n'


def test_hn_chained():
    assert md('<h1>First</h1>\n<h2>Second</h2>\n<h3>Third</h3>', heading_style=ATX) == '# First\n\n\n## Second\n\n\n### Third\n\n'
    assert md('X<h1>First</h1>', heading_style=ATX) == 'X# First\n\n'


def test_hn_nested_tag_heading_style():
    assert md('<h1>A <p>P</p> C </h1>', heading_style=ATX_CLOSED) == '# A P C #\n\n'
    assert md('<h1>A <p>P</p> C </h1>', heading_style=ATX) == '# A P C\n\n'


def test_hn_nested_simple_tag():
    tag_to_markdown = [
        ("strong", "**strong**"),
        ("b", "**b**"),
        ("em", "*em*"),
        ("i", "*i*"),
        ("p", "p"),
        ("a", "a"),
        ("div", "div"),
        ("blockquote", "blockquote"),
    ]

    for tag, markdown in tag_to_markdown:
        assert md('<h3>A <' + tag + '>' + tag + '</' + tag + '> B</h3>') == '### A ' + markdown + ' B\n\n'

    assert md('<h3>A <br>B</h3>', heading_style=ATX) == '### A B\n\n'

    # Nested lists not supported
    # assert md('<h3>A <ul><li>li1</i><li>l2</li></ul></h3>', heading_style=ATX) == '### A li1 li2 B\n\n'


def test_hn_nested_img():
    image_attributes_to_markdown = [
        ("", "", ""),
        ("alt='Alt Text'", "Alt Text", ""),
        ("alt='Alt Text' title='Optional title'", "Alt Text", " \"Optional title\""),
    ]
    for image_attributes, markdown, title in image_attributes_to_markdown:
        assert md('<h3>A <img src="/path/to/img.jpg" ' + image_attributes + '/> B</h3>') == '### A ' + markdown + ' B\n\n'
        assert md('<h3>A <img src="/path/to/img.jpg" ' + image_attributes + '/> B</h3>', keep_inline_images_in=['h3']) == '### A ![' + markdown + '](/path/to/img.jpg' + title + ') B\n\n'


def test_hn_atx_headings():
    assert md('<h1>Hello</h1>', heading_style=ATX) == '# Hello\n\n'
    assert md('<h2>Hello</h2>', heading_style=ATX) == '## Hello\n\n'


def test_hn_atx_closed_headings():
    assert md('<h1>Hello</h1>', heading_style=ATX_CLOSED) == '# Hello #\n\n'
    assert md('<h2>Hello</h2>', heading_style=ATX_CLOSED) == '## Hello ##\n\n'


def test_head():
    assert md('<head>head</head>') == 'head'


def test_hr():
    assert md('Hello<hr>World') == 'Hello\n\n---\n\nWorld'
    assert md('Hello<hr />World') == 'Hello\n\n---\n\nWorld'
    assert md('<p>Hello</p>\n<hr>\n<p>World</p>') == 'Hello\n\n\n\n\n---\n\n\nWorld\n\n'


def test_i():
    assert md('<i>Hello</i>') == '*Hello*'


def test_img():
    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />') == '![Alt text](/path/to/img.jpg "Optional title")'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />') == '![Alt text](/path/to/img.jpg)'


def test_kbd():
    inline_tests('kbd', '`')


def test_p():
    assert md('<p>hello</p>') == 'hello\n\n'
    assert md('<p>123456789 123456789</p>') == '123456789 123456789\n\n'
    assert md('<p>123456789 123456789</p>', wrap=True, wrap_width=10) == '123456789\n123456789\n\n'
    assert md('<p><a href="https://example.com">Some long link</a></p>', wrap=True, wrap_width=10) == '[Some long\nlink](https://example.com)\n\n'
    assert md('<p>12345<br />67890</p>', wrap=True, wrap_width=10, newline_style=BACKSLASH) == '12345\\\n67890\n\n'
    assert md('<p>12345678901<br />12345</p>', wrap=True, wrap_width=10, newline_style=BACKSLASH) == '12345678901\\\n12345\n\n'


def test_pre():
    assert md('<pre>test\n    foo\nbar</pre>') == '\n```\ntest\n    foo\nbar\n```\n'
    assert md('<pre><code>test\n    foo\nbar</code></pre>') == '\n```\ntest\n    foo\nbar\n```\n'
    assert md('<pre>*this_should_not_escape*</pre>') == '\n```\n*this_should_not_escape*\n```\n'
    assert md('<pre><span>*this_should_not_escape*</span></pre>') == '\n```\n*this_should_not_escape*\n```\n'
    assert md('<pre>\t\tthis  should\t\tnot  normalize</pre>') == '\n```\n\t\tthis  should\t\tnot  normalize\n```\n'
    assert md('<pre><span>\t\tthis  should\t\tnot  normalize</span></pre>') == '\n```\n\t\tthis  should\t\tnot  normalize\n```\n'


def test_script():
    assert md('foo <script>var foo=42;</script> bar') == 'foo  bar'


def test_style():
    assert md('foo <style>h1 { font-size: larger }</style> bar') == 'foo  bar'


def test_s():
    inline_tests('s', '~~')


def test_samp():
    inline_tests('samp', '`')


def test_strong():
    assert md('<strong>Hello</strong>') == '**Hello**'


def test_strong_em_symbol():
    assert md('<strong>Hello</strong>', strong_em_symbol=UNDERSCORE) == '__Hello__'
    assert md('<b>Hello</b>', strong_em_symbol=UNDERSCORE) == '__Hello__'
    assert md('<em>Hello</em>', strong_em_symbol=UNDERSCORE) == '_Hello_'
    assert md('<i>Hello</i>', strong_em_symbol=UNDERSCORE) == '_Hello_'


def test_sub():
    assert md('<sub>foo</sub>') == 'foo'
    assert md('<sub>foo</sub>', sub_symbol='~') == '~foo~'


def test_sup():
    assert md('<sup>foo</sup>') == 'foo'
    assert md('<sup>foo</sup>', sup_symbol='^') == '^foo^'


def test_lang():
    assert md('<pre>test\n    foo\nbar</pre>', code_language='python') == '\n```python\ntest\n    foo\nbar\n```\n'
    assert md('<pre><code>test\n    foo\nbar</code></pre>', code_language='javascript') == '\n```javascript\ntest\n    foo\nbar\n```\n'


def test_lang_callback():
    def callback(el):
        return el['class'][0] if el.has_attr('class') else None

    assert md('<pre class="python">test\n    foo\nbar</pre>', code_language_callback=callback) == '\n```python\ntest\n    foo\nbar\n```\n'
    assert md('<pre class="javascript"><code>test\n    foo\nbar</code></pre>', code_language_callback=callback) == '\n```javascript\ntest\n    foo\nbar\n```\n'
    assert md('<pre class="javascript"><code class="javascript">test\n    foo\nbar</code></pre>', code_language_callback=callback) == '\n```javascript\ntest\n    foo\nbar\n```\n'
