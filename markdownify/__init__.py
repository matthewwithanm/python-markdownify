from bs4 import BeautifulSoup, NavigableString
import re


convert_heading_re = re.compile(r'convert_h(\d+)')
line_beginning_re = re.compile(r'^', re.MULTILINE)
whitespace_re = re.compile(r'[\r\n\s\t ]+')
FRAGMENT_ID = '__MARKDOWNIFY_WRAPPER__'
wrapped = '<div id="%s">%%s</div>' % FRAGMENT_ID


def escape(text):
    if not text:
        return ''
    return text.replace('_', r'\_')


class MarkdownConverter(object):
    def __init__(self, tags_to_strip=None, tags_to_convert=None):
        if tags_to_strip is not None and tags_to_convert is not None:
            raise ValueError('You may specify either tags to strip or tags to'
                             ' convert, but not both.')
        self.tags_to_strip = tags_to_strip
        self.tags_to_convert = tags_to_convert

    def convert(self, html):
        # We want to take advantage of the html5 parsing, but we don't actually
        # want a full document. Therefore, we'll mark our fragment with an id,
        # create the document, and extract the element with the id.
        html = wrapped % html
        soup = BeautifulSoup(html)
        return self.process_tag(soup.find(id=FRAGMENT_ID), children_only=True)

    def process_tag(self, node, children_only=False):
        text = ''

        # Convert the children first
        for el in node.children:
            if isinstance(el, NavigableString):
                text += self.process_text(unicode(el))
            else:
                text += self.process_tag(el)

        if not children_only:
            convert_fn = getattr(self, 'convert_%s' % node.name, None)
            if convert_fn and self.should_convert_tag(node.name):
                text = convert_fn(node, text)

        return text

    def process_text(self, text):
        return escape(whitespace_re.sub(' ', text or ''))

    def __getattr__(self, attr):
        # Handle heading levels > 2
        m = convert_heading_re.match(attr)
        if m:
            n = int(m.group(1))

            def convert_tag(el, text):
                return self.convert_hn(n, el, text)

            convert_tag.__name__ = 'convert_h%s' % n
            setattr(self, convert_tag.__name__, convert_tag)
            return convert_tag

        raise AttributeError(attr)

    def should_convert_tag(self, tag):
        tag = tag.lower()
        if self.tags_to_strip is not None:
            return tag not in self.tags_to_strip
        elif self.tags_to_convert is not None:
            return tag in self.tags_to_convert
        else:
            return True

    def underline(self, text, pad_char):
        text = (text or '').rstrip()
        return '%s\n%s\n\n' % (text, pad_char * len(text)) if text else ''

    def convert_a(self, el, text):
        href = el.get('href')
        title = el.get('title')
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        return '[%s](%s%s)' % (text or '', href, title_part) if href else text or ''

    def convert_b(self, el, text):
        return self.convert_strong(el, text)

    def convert_blockquote(self, el, text):
        return '\n' + line_beginning_re.sub('> ', text) if text else ''

    def convert_br(self, el, text):
        return '  \n'

    def convert_em(self, el, text):
        return '*%s*' % text if text else ''

    def convert_h1(self, el, text):
        return self.underline(text, '=')

    def convert_h2(self, el, text):
        return self.underline(text, '-')

    def convert_hn(self, n, el, text):
        return '%s %s\n\n' % ('#' * n, text.rstrip()) if text else ''

    def convert_i(self, el, text):
        return self.convert_em(el, text)

    def convert_li(self, el, text):
        parent = el.parent
        if parent is not None and parent.name == 'ol':
            bullet = '%s.' % (parent.index(el) + 1)
        else:
            bullet = '*'
        return '%s %s\n' % (bullet, text or '')

    def convert_p(self, el, text):
        return '%s\n\n' % text if text else ''

    def convert_strong(self, el, text):
        return '**%s**' % text if text else ''


def markdownify(html, strip=None, convert=None):
    converter = MarkdownConverter(strip, convert)
    return converter.convert(html)
