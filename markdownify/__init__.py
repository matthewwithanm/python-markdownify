from bs4 import BeautifulSoup, NavigableString, Comment, Doctype
from textwrap import fill
import re
import six


convert_heading_re = re.compile(r'convert_h(\d+)')
line_beginning_re = re.compile(r'^', re.MULTILINE)
whitespace_re = re.compile(r'[\t ]+')
all_whitespace_re = re.compile(r'[\s]+')
html_heading_re = re.compile(r'h[1-6]')


# Heading styles
ATX = 'atx'
ATX_CLOSED = 'atx_closed'
UNDERLINED = 'underlined'
SETEXT = UNDERLINED

# Newline style
SPACES = 'spaces'
BACKSLASH = 'backslash'

# Strong and emphasis style
ASTERISK = '*'
UNDERSCORE = '_'


def chomp(text):
    """
    If the text in an inline tag like b, a, or em contains a leading or trailing
    space, strip the string and return a space as suffix of prefix, if needed.
    This function is used to prevent conversions like
        <b> foo</b> => ** foo**
    """
    prefix = ' ' if text and text[0] == ' ' else ''
    suffix = ' ' if text and text[-1] == ' ' else ''
    text = text.strip()
    return (prefix, suffix, text)


def abstract_inline_conversion(markup_fn):
    """
    This abstracts all simple inline tags like b, em, del, ...
    Returns a function that wraps the chomped text in a pair of the string
    that is returned by markup_fn. markup_fn is necessary to allow for
    references to self.strong_em_symbol etc.
    """
    def implementation(self, el, text, convert_as_inline):
        markup = markup_fn(self)
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        return '%s%s%s%s%s' % (prefix, markup, text, markup, suffix)
    return implementation


def _todict(obj):
    return dict((k, getattr(obj, k)) for k in dir(obj) if not k.startswith('_'))


class MarkdownConverter(object):
    class DefaultOptions:
        autolinks = True
        bullets = '*+-'  # An iterable of bullet types.
        code_language = ''
        code_language_callback = None
        convert = None
        default_title = False
        escape_asterisks = True
        escape_underscores = True
        heading_style = UNDERLINED
        keep_inline_images_in = []
        newline_style = SPACES
        strip = None
        strong_em_symbol = ASTERISK
        sub_symbol = ''
        sup_symbol = ''
        wrap = False
        wrap_width = 80

    class Options(DefaultOptions):
        pass

    def __init__(self, **options):
        # Create an options dictionary. Use DefaultOptions as a base so that
        # it doesn't have to be extended.
        self.options = _todict(self.DefaultOptions)
        self.options.update(_todict(self.Options))
        self.options.update(options)
        if self.options['strip'] is not None and self.options['convert'] is not None:
            raise ValueError('You may specify either tags to strip or tags to'
                             ' convert, but not both.')

    def convert(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return self.convert_soup(soup)

    def convert_soup(self, soup):
        return self.process_tag(soup, convert_as_inline=False, children_only=True)

    def process_tag(self, node, convert_as_inline, children_only=False):
        text = ''

        # markdown headings or cells can't include
        # block elements (elements w/newlines)
        isHeading = html_heading_re.match(node.name) is not None
        isCell = node.name in ['td', 'th']
        convert_children_as_inline = convert_as_inline

        if not children_only and (isHeading or isCell):
            convert_children_as_inline = True

        # Remove whitespace-only textnodes in purely nested nodes
        def is_nested_node(el):
            return el and el.name in ['ol', 'ul', 'li',
                                      'table', 'thead', 'tbody', 'tfoot',
                                      'tr', 'td', 'th']

        if is_nested_node(node):
            for el in node.children:
                # Only extract (remove) whitespace-only text node if any of the
                # conditions is true:
                # - el is the first element in its parent
                # - el is the last element in its parent
                # - el is adjacent to an nested node
                can_extract = (not el.previous_sibling
                               or not el.next_sibling
                               or is_nested_node(el.previous_sibling)
                               or is_nested_node(el.next_sibling))
                if (isinstance(el, NavigableString)
                        and six.text_type(el).strip() == ''
                        and can_extract):
                    el.extract()

        # Convert the children first
        for el in node.children:
            if isinstance(el, Comment) or isinstance(el, Doctype):
                continue
            elif isinstance(el, NavigableString):
                text += self.process_text(el)
            else:
                text += self.process_tag(el, convert_children_as_inline)

        if not children_only:
            convert_fn = getattr(self, 'convert_%s' % node.name, None)
            if convert_fn and self.should_convert_tag(node.name):
                text = convert_fn(node, text, convert_as_inline)

        return text

    def process_text(self, el):
        text = six.text_type(el) or ''

        # normalize whitespace if we're not inside a preformatted element
        if not el.find_parent('pre'):
            text = whitespace_re.sub(' ', text)

        # escape special characters if we're not inside a preformatted or code element
        if not el.find_parent(['pre', 'code', 'kbd', 'samp']):
            text = self.escape(text)

        # remove trailing whitespaces if any of the following condition is true:
        # - current text node is the last node in li
        # - current text node is followed by an embedded list
        if (el.parent.name == 'li'
                and (not el.next_sibling
                     or el.next_sibling.name in ['ul', 'ol'])):
            text = text.rstrip()

        return text

    def __getattr__(self, attr):
        # Handle headings
        m = convert_heading_re.match(attr)
        if m:
            n = int(m.group(1))

            def convert_tag(el, text, convert_as_inline):
                return self.convert_hn(n, el, text, convert_as_inline)

            convert_tag.__name__ = 'convert_h%s' % n
            setattr(self, convert_tag.__name__, convert_tag)
            return convert_tag

        raise AttributeError(attr)

    def should_convert_tag(self, tag):
        tag = tag.lower()
        strip = self.options['strip']
        convert = self.options['convert']
        if strip is not None:
            return tag not in strip
        elif convert is not None:
            return tag in convert
        else:
            return True

    def escape(self, text):
        if not text:
            return ''
        if self.options['escape_asterisks']:
            text = text.replace('*', r'\*')
        if self.options['escape_underscores']:
            text = text.replace('_', r'\_')
        return text

    def indent(self, text, level):
        return line_beginning_re.sub('\t' * level, text) if text else ''

    def underline(self, text, pad_char):
        text = (text or '').rstrip()
        return '%s\n%s\n\n' % (text, pad_char * len(text)) if text else ''

    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        href = el.get('href')
        title = el.get('title')
        # For the replacement see #29: text nodes underscores are escaped
        if (self.options['autolinks']
                and text.replace(r'\_', '_') == href
                and not title
                and not self.options['default_title']):
            # Shortcut syntax
            return '<%s>' % href
        if self.options['default_title'] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        return '%s[%s](%s%s)%s' % (prefix, text, href, title_part, suffix) if href else text

    convert_b = abstract_inline_conversion(lambda self: 2 * self.options['strong_em_symbol'])

    def convert_blockquote(self, el, text, convert_as_inline):

        if convert_as_inline:
            return text

        return '\n' + (line_beginning_re.sub('> ', text.strip()) + '\n\n') if text else ''

    def convert_br(self, el, text, convert_as_inline):
        if convert_as_inline:
            return ""

        if self.options['newline_style'].lower() == BACKSLASH:
            return '\\\n'
        else:
            return '  \n'

    def convert_code(self, el, text, convert_as_inline):
        if el.parent.name == 'pre':
            return text
        converter = abstract_inline_conversion(lambda self: '`')
        return converter(self, el, text, convert_as_inline)

    convert_del = abstract_inline_conversion(lambda self: '~~')

    convert_em = abstract_inline_conversion(lambda self: self.options['strong_em_symbol'])

    convert_kbd = convert_code

    def convert_hn(self, n, el, text, convert_as_inline):
        if convert_as_inline:
            return text

        style = self.options['heading_style'].lower()
        text = text.strip()
        if style == UNDERLINED and n <= 2:
            line = '=' if n == 1 else '-'
            return self.underline(text, line)
        hashes = '#' * n
        if style == ATX_CLOSED:
            return '%s %s %s\n\n' % (hashes, text, hashes)
        return '%s %s\n\n' % (hashes, text)

    def convert_hr(self, el, text, convert_as_inline):
        return '\n\n---\n\n'

    convert_i = convert_em

    def convert_img(self, el, text, convert_as_inline):
        alt = el.attrs.get('alt', None) or ''
        src = el.attrs.get('src', None) or ''
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        if (convert_as_inline
                and el.parent.name not in self.options['keep_inline_images_in']):
            return alt

        return '![%s](%s%s)' % (alt, src, title_part)

    def convert_list(self, el, text, convert_as_inline):

        # Converting a list to inline is undefined.
        # Ignoring convert_to_inline for list.

        nested = False
        before_paragraph = False
        if el.next_sibling and el.next_sibling.name not in ['ul', 'ol']:
            before_paragraph = True
        while el:
            if el.name == 'li':
                nested = True
                break
            el = el.parent
        if nested:
            # remove trailing newline if nested
            return '\n' + self.indent(text, 1).rstrip()
        return text + ('\n' if before_paragraph else '')

    convert_ul = convert_list
    convert_ol = convert_list

    def convert_li(self, el, text, convert_as_inline):
        parent = el.parent
        if parent is not None and parent.name == 'ol':
            if parent.get("start"):
                start = int(parent.get("start"))
            else:
                start = 1
            bullet = '%s.' % (start + parent.index(el))
        else:
            depth = -1
            while el:
                if el.name == 'ul':
                    depth += 1
                el = el.parent
            bullets = self.options['bullets']
            bullet = bullets[depth % len(bullets)]
        return '%s %s\n' % (bullet, (text or '').strip())

    def convert_p(self, el, text, convert_as_inline):
        if convert_as_inline:
            return text
        if self.options['wrap']:
            text = fill(text,
                        width=self.options['wrap_width'],
                        break_long_words=False,
                        break_on_hyphens=False)
        return '%s\n\n' % text if text else ''

    def convert_pre(self, el, text, convert_as_inline):
        if not text:
            return ''
        code_language = self.options['code_language']

        if self.options['code_language_callback']:
            code_language = self.options['code_language_callback'](el) or code_language

        return '\n```%s\n%s\n```\n' % (code_language, text)

    def convert_script(self, el, text, convert_as_inline):
        return ''

    def convert_style(self, el, text, convert_as_inline):
        return ''

    convert_s = convert_del

    convert_strong = convert_b

    convert_samp = convert_code

    convert_sub = abstract_inline_conversion(lambda self: self.options['sub_symbol'])

    convert_sup = abstract_inline_conversion(lambda self: self.options['sup_symbol'])

    def convert_table(self, el, text, convert_as_inline):
        return '\n\n' + text + '\n'

    def convert_caption(self, el, text, convert_as_inline):
        return text + '\n'

    def convert_figcaption(self, el, text, convert_as_inline):
        return '\n\n' + text + '\n\n'

    def convert_td(self, el, text, convert_as_inline):
        colspan = 1
        if 'colspan' in el.attrs:
            colspan = int(el['colspan'])
        return ' ' + text.strip().replace("\n", " ") + ' |' * colspan

    def convert_th(self, el, text, convert_as_inline):
        colspan = 1
        if 'colspan' in el.attrs:
            colspan = int(el['colspan'])
        return ' ' + text.strip().replace("\n", " ") + ' |' * colspan

    def convert_tr(self, el, text, convert_as_inline):
        cells = el.find_all(['td', 'th'])
        is_headrow = (
            all([cell.name == 'th' for cell in cells])
            or (not el.previous_sibling and not el.parent.name == 'tbody')
            or (not el.previous_sibling and el.parent.name == 'tbody' and len(el.parent.parent.find_all(['thead'])) < 1)
        )
        overline = ''
        underline = ''
        if is_headrow and not el.previous_sibling:
            # first row and is headline: print headline underline
            full_colspan = 0
            for cell in cells:
                if "colspan" in cell.attrs:
                    full_colspan += int(cell["colspan"])
                else:
                    full_colspan += 1
            underline += '| ' + ' | '.join(['---'] * full_colspan) + ' |' + '\n'
        elif (not el.previous_sibling
              and (el.parent.name == 'table'
                   or (el.parent.name == 'tbody'
                       and not el.parent.previous_sibling))):
            # first row, not headline, and:
            # - the parent is table or
            # - the parent is tbody at the beginning of a table.
            # print empty headline above this row
            overline += '| ' + ' | '.join([''] * len(cells)) + ' |' + '\n'
            overline += '| ' + ' | '.join(['---'] * len(cells)) + ' |' + '\n'
        return overline + '|' + text + '\n' + underline


def markdownify(html, **options):
    return MarkdownConverter(**options).convert(html)
