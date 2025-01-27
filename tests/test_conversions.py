from markdownify import ATX, ATX_CLOSED, BACKSLASH, SPACES, UNDERSCORE
from .utils import md


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


def test_a_in_code():
    assert md('<code><a href="https://google.com">Google</a></code>') == '`Google`'
    assert md('<pre><a href="https://google.com">Google</a></pre>') == '\n\n```\nGoogle\n```\n\n'


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
    assert md('<blockquote><p>Hello</p><p>Hello again</p></blockquote>') == '\n> Hello\n>\n> Hello again\n\n'


def test_blockquote_with_paragraph():
    assert md('<blockquote>Hello</blockquote><p>handsome</p>') == '\n> Hello\n\nhandsome\n\n'


def test_blockquote_nested():
    text = md('<blockquote>And she was like <blockquote>Hello</blockquote></blockquote>')
    assert text == '\n> And she was like\n> > Hello\n\n'


def test_br():
    assert md('a<br />b<br />c') == 'a  \nb  \nc'
    assert md('a<br />b<br />c', newline_style=BACKSLASH) == 'a\\\nb\\\nc'


def test_code():
    inline_tests('code', '`')
    assert md('<code>*this_should_not_escape*</code>') == '`*this_should_not_escape*`'
    assert md('<kbd>*this_should_not_escape*</kbd>') == '`*this_should_not_escape*`'
    assert md('<samp>*this_should_not_escape*</samp>') == '`*this_should_not_escape*`'
    assert md('<code><span>*this_should_not_escape*</span></code>') == '`*this_should_not_escape*`'
    assert md('<code>this  should\t\tnormalize</code>') == '`this should normalize`'
    assert md('<code><span>this  should\t\tnormalize</span></code>') == '`this should normalize`'
    assert md('<code>foo<b>bar</b>baz</code>') == '`foobarbaz`'
    assert md('<kbd>foo<i>bar</i>baz</kbd>') == '`foobarbaz`'
    assert md('<samp>foo<del> bar </del>baz</samp>') == '`foo bar baz`'
    assert md('<samp>foo <del>bar</del> baz</samp>') == '`foo bar baz`'
    assert md('<code>foo<em> bar </em>baz</code>') == '`foo bar baz`'
    assert md('<code>foo<code> bar </code>baz</code>') == '`foo bar baz`'
    assert md('<code>foo<strong> bar </strong>baz</code>') == '`foo bar baz`'
    assert md('<code>foo<s> bar </s>baz</code>') == '`foo bar baz`'
    assert md('<code>foo<sup>bar</sup>baz</code>', sup_symbol='^') == '`foobarbaz`'
    assert md('<code>foo<sub>bar</sub>baz</code>', sub_symbol='^') == '`foobarbaz`'


def test_dl():
    assert md('<dl><dt>term</dt><dd>definition</dd></dl>') == '\nterm\n:   definition\n'
    assert md('<dl><dt><p>te</p><p>rm</p></dt><dd>definition</dd></dl>') == '\nte rm\n:   definition\n'
    assert md('<dl><dt>term</dt><dd><p>definition-p1</p><p>definition-p2</p></dd></dl>') == '\nterm\n:   definition-p1\n\n    definition-p2\n'
    assert md('<dl><dt>term</dt><dd><p>definition 1</p></dd><dd><p>definition 2</p></dd></dl>') == '\nterm\n:   definition 1\n:   definition 2\n'
    assert md('<dl><dt>term 1</dt><dd>definition 1</dd><dt>term 2</dt><dd>definition 2</dd></dl>') == '\nterm 1\n:   definition 1\nterm 2\n:   definition 2\n'
    assert md('<dl><dt>term</dt><dd><blockquote><p>line 1</p><p>line 2</p></blockquote></dd></dl>') == '\nterm\n:   > line 1\n    >\n    > line 2\n'
    assert md('<dl><dt>term</dt><dd><ol><li><p>1</p><ul><li>2a</li><li>2b</li></ul></li><li><p>3</p></li></ol></dd></dl>') == '\nterm\n:   1. 1\n\n       * 2a\n       * 2b\n    2. 3\n'


def test_del():
    inline_tests('del', '~~')


def test_div():
    assert md('Hello</div> World') == 'Hello World'


def test_em():
    inline_tests('em', '*')


def test_figcaption():
    assert (md("TEXT<figure><figcaption>\nCaption\n</figcaption><span>SPAN</span></figure>") == "TEXT\n\nCaption\n\nSPAN")
    assert (md("<figure><span>SPAN</span><figcaption>\nCaption\n</figcaption></figure>TEXT") == "SPAN\n\nCaption\n\nTEXT")


def test_header_with_space():
    assert md('<h3>\n\nHello</h3>') == '\n\n### Hello\n\n'
    assert md('<h3>Hello\n\n\nWorld</h3>') == '\n\n### Hello World\n\n'
    assert md('<h4>\n\nHello</h4>') == '\n\n#### Hello\n\n'
    assert md('<h5>\n\nHello</h5>') == '\n\n##### Hello\n\n'
    assert md('<h5>\n\nHello\n\n</h5>') == '\n\n##### Hello\n\n'
    assert md('<h5>\n\nHello   \n\n</h5>') == '\n\n##### Hello\n\n'


def test_h1():
    assert md('<h1>Hello</h1>') == '\n\nHello\n=====\n\n'


def test_h2():
    assert md('<h2>Hello</h2>') == '\n\nHello\n-----\n\n'


def test_hn():
    assert md('<h3>Hello</h3>') == '\n\n### Hello\n\n'
    assert md('<h4>Hello</h4>') == '\n\n#### Hello\n\n'
    assert md('<h5>Hello</h5>') == '\n\n##### Hello\n\n'
    assert md('<h6>Hello</h6>') == '\n\n###### Hello\n\n'
    assert md('<h10>Hello</h10>') == md('<h6>Hello</h6>')
    assert md('<hn>Hello</hn>') == md('Hello')


def test_hn_chained():
    assert md('<h1>First</h1>\n<h2>Second</h2>\n<h3>Third</h3>', heading_style=ATX) == '\n\n# First\n\n## Second\n\n### Third\n\n'
    assert md('X<h1>First</h1>', heading_style=ATX) == 'X\n\n# First\n\n'
    assert md('X<h1>First</h1>', heading_style=ATX_CLOSED) == 'X\n\n# First #\n\n'
    assert md('X<h1>First</h1>') == 'X\n\nFirst\n=====\n\n'


def test_hn_nested_tag_heading_style():
    assert md('<h1>A <p>P</p> C </h1>', heading_style=ATX_CLOSED) == '\n\n# A P C #\n\n'
    assert md('<h1>A <p>P</p> C </h1>', heading_style=ATX) == '\n\n# A P C\n\n'


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
        assert md('<h3>A <' + tag + '>' + tag + '</' + tag + '> B</h3>') == '\n\n### A ' + markdown + ' B\n\n'

    assert md('<h3>A <br>B</h3>', heading_style=ATX) == '\n\n### A B\n\n'

    # Nested lists not supported
    # assert md('<h3>A <ul><li>li1</i><li>l2</li></ul></h3>', heading_style=ATX) == '\n### A li1 li2 B\n\n'


def test_hn_nested_img():
    image_attributes_to_markdown = [
        ("", "", ""),
        ("alt='Alt Text'", "Alt Text", ""),
        ("alt='Alt Text' title='Optional title'", "Alt Text", " \"Optional title\""),
    ]
    for image_attributes, markdown, title in image_attributes_to_markdown:
        assert md('<h3>A <img src="/path/to/img.jpg" ' + image_attributes + '/> B</h3>') == '\n\n### A' + (' ' + markdown + ' ' if markdown else ' ') + 'B\n\n'
        assert md('<h3>A <img src="/path/to/img.jpg" ' + image_attributes + '/> B</h3>', keep_inline_images_in=['h3']) == '\n\n### A ![' + markdown + '](/path/to/img.jpg' + title + ') B\n\n'


def test_hn_atx_headings():
    assert md('<h1>Hello</h1>', heading_style=ATX) == '\n\n# Hello\n\n'
    assert md('<h2>Hello</h2>', heading_style=ATX) == '\n\n## Hello\n\n'


def test_hn_atx_closed_headings():
    assert md('<h1>Hello</h1>', heading_style=ATX_CLOSED) == '\n\n# Hello #\n\n'
    assert md('<h2>Hello</h2>', heading_style=ATX_CLOSED) == '\n\n## Hello ##\n\n'


def test_hn_newlines():
    assert md("<h1>H1-1</h1>TEXT<h2>H2-2</h2>TEXT<h1>H1-2</h1>TEXT", heading_style=ATX) == '\n\n# H1-1\n\nTEXT\n\n## H2-2\n\nTEXT\n\n# H1-2\n\nTEXT'
    assert md('<h1>H1-1</h1>\n<p>TEXT</p>\n<h2>H2-2</h2>\n<p>TEXT</p>\n<h1>H1-2</h1>\n<p>TEXT</p>', heading_style=ATX) == '\n\n# H1-1\n\nTEXT\n\n## H2-2\n\nTEXT\n\n# H1-2\n\nTEXT\n\n'


def test_head():
    assert md('<head>head</head>') == 'head'


def test_hr():
    assert md('Hello<hr>World') == 'Hello\n\n---\n\nWorld'
    assert md('Hello<hr />World') == 'Hello\n\n---\n\nWorld'
    assert md('<p>Hello</p>\n<hr>\n<p>World</p>') == '\n\nHello\n\n---\n\nWorld\n\n'


def test_i():
    assert md('<i>Hello</i>') == '*Hello*'


def test_img():
    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />') == '![Alt text](/path/to/img.jpg "Optional title")'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />') == '![Alt text](/path/to/img.jpg)'


def test_kbd():
    inline_tests('kbd', '`')


def test_p():
    assert md('<p>hello</p>') == '\n\nhello\n\n'
    assert md("<p><p>hello</p></p>") == "\n\nhello\n\n"
    assert md('<p>123456789 123456789</p>') == '\n\n123456789 123456789\n\n'
    assert md('<p>123456789\n\n\n123456789</p>') == '\n\n123456789\n123456789\n\n'
    assert md('<p>123456789\n\n\n123456789</p>', wrap=True, wrap_width=80) == '\n\n123456789 123456789\n\n'
    assert md('<p>123456789\n\n\n123456789</p>', wrap=True, wrap_width=None) == '\n\n123456789 123456789\n\n'
    assert md('<p>123456789 123456789</p>', wrap=True, wrap_width=10) == '\n\n123456789\n123456789\n\n'
    assert md('<p><a href="https://example.com">Some long link</a></p>', wrap=True, wrap_width=10) == '\n\n[Some long\nlink](https://example.com)\n\n'
    assert md('<p>12345<br />67890</p>', wrap=True, wrap_width=10, newline_style=BACKSLASH) == '\n\n12345\\\n67890\n\n'
    assert md('<p>12345<br />67890</p>', wrap=True, wrap_width=50, newline_style=BACKSLASH) == '\n\n12345\\\n67890\n\n'
    assert md('<p>12345<br />67890</p>', wrap=True, wrap_width=10, newline_style=SPACES) == '\n\n12345  \n67890\n\n'
    assert md('<p>12345<br />67890</p>', wrap=True, wrap_width=50, newline_style=SPACES) == '\n\n12345  \n67890\n\n'
    assert md('<p>12345678901<br />12345</p>', wrap=True, wrap_width=10, newline_style=BACKSLASH) == '\n\n12345678901\\\n12345\n\n'
    assert md('<p>12345678901<br />12345</p>', wrap=True, wrap_width=50, newline_style=BACKSLASH) == '\n\n12345678901\\\n12345\n\n'
    assert md('<p>12345678901<br />12345</p>', wrap=True, wrap_width=10, newline_style=SPACES) == '\n\n12345678901  \n12345\n\n'
    assert md('<p>12345678901<br />12345</p>', wrap=True, wrap_width=50, newline_style=SPACES) == '\n\n12345678901  \n12345\n\n'
    assert md('<p>1234 5678 9012<br />67890</p>', wrap=True, wrap_width=10, newline_style=BACKSLASH) == '\n\n1234 5678\n9012\\\n67890\n\n'
    assert md('<p>1234 5678 9012<br />67890</p>', wrap=True, wrap_width=10, newline_style=SPACES) == '\n\n1234 5678\n9012  \n67890\n\n'
    assert md('First<p>Second</p><p>Third</p>Fourth') == 'First\n\nSecond\n\nThird\n\nFourth'


def test_pre():
    assert md('<pre>test\n    foo\nbar</pre>') == '\n\n```\ntest\n    foo\nbar\n```\n\n'
    assert md('<pre><code>test\n    foo\nbar</code></pre>') == '\n\n```\ntest\n    foo\nbar\n```\n\n'
    assert md('<pre>*this_should_not_escape*</pre>') == '\n\n```\n*this_should_not_escape*\n```\n\n'
    assert md('<pre><span>*this_should_not_escape*</span></pre>') == '\n\n```\n*this_should_not_escape*\n```\n\n'
    assert md('<pre>\t\tthis  should\t\tnot  normalize</pre>') == '\n\n```\n\t\tthis  should\t\tnot  normalize\n```\n\n'
    assert md('<pre><span>\t\tthis  should\t\tnot  normalize</span></pre>') == '\n\n```\n\t\tthis  should\t\tnot  normalize\n```\n\n'
    assert md('<pre>foo<b>\nbar\n</b>baz</pre>') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<i>\nbar\n</i>baz</pre>') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo\n<i>bar</i>\nbaz</pre>') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<i>\n</i>baz</pre>') == '\n\n```\nfoo\nbaz\n```\n\n'
    assert md('<pre>foo<del>\nbar\n</del>baz</pre>') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<em>\nbar\n</em>baz</pre>') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<code>\nbar\n</code>baz</pre>') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<strong>\nbar\n</strong>baz</pre>') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<s>\nbar\n</s>baz</pre>') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<sup>\nbar\n</sup>baz</pre>', sup_symbol='^') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<sub>\nbar\n</sub>baz</pre>', sub_symbol='^') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'
    assert md('<pre>foo<sub>\nbar\n</sub>baz</pre>', sub_symbol='^') == '\n\n```\nfoo\nbar\nbaz\n```\n\n'

    assert md('foo<pre>bar</pre>baz', sub_symbol='^') == 'foo\n\n```\nbar\n```\n\nbaz'
    assert md("<p>foo</p>\n<pre>bar</pre>\n</p>baz</p>", sub_symbol="^") == "\n\nfoo\n\n```\nbar\n```\n\nbaz"


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
    assert md('<sub>foo</sub>', sub_symbol='<sub>') == '<sub>foo</sub>'


def test_sup():
    assert md('<sup>foo</sup>') == 'foo'
    assert md('<sup>foo</sup>', sup_symbol='^') == '^foo^'
    assert md('<sup>foo</sup>', sup_symbol='<sup>') == '<sup>foo</sup>'


def test_lang():
    assert md('<pre>test\n    foo\nbar</pre>', code_language='python') == '\n\n```python\ntest\n    foo\nbar\n```\n\n'
    assert md('<pre><code>test\n    foo\nbar</code></pre>', code_language='javascript') == '\n\n```javascript\ntest\n    foo\nbar\n```\n\n'


def test_lang_callback():
    def callback(el):
        return el['class'][0] if el.has_attr('class') else None

    assert md('<pre class="python">test\n    foo\nbar</pre>', code_language_callback=callback) == '\n\n```python\ntest\n    foo\nbar\n```\n\n'
    assert md('<pre class="javascript"><code>test\n    foo\nbar</code></pre>', code_language_callback=callback) == '\n\n```javascript\ntest\n    foo\nbar\n```\n\n'
    assert md('<pre class="javascript"><code class="javascript">test\n    foo\nbar</code></pre>', code_language_callback=callback) == '\n\n```javascript\ntest\n    foo\nbar\n```\n\n'


def test_spaces():
    assert md('<p> a b </p> <p> c d </p>') == '\n\na b\n\nc d\n\n'
    assert md('<p> <i>a</i> </p>') == '\n\n*a*\n\n'
    assert md('test <p> again </p>') == 'test\n\nagain\n\n'
    assert md('test <blockquote> text </blockquote> after') == 'test\n> text\n\nafter'
    assert md(' <ol> <li> x </li> <li> y </li> </ol> ') == '\n\n1. x\n2. y\n'
    assert md(' <ul> <li> x </li> <li> y </li> </ol> ') == '\n\n* x\n* y\n'
    assert md('test <pre> foo </pre> bar') == 'test\n\n```\n foo \n```\n\nbar'
