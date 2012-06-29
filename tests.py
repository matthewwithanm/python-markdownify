import unittest
from markdownify import markdownify as md


class BasicTests(unittest.TestCase):

    def test_single_tag(self):
        self.assertEqual(md('<span>Hello</span>'), 'Hello')

    def test_soup(self):
        self.assertEqual(md('<div><span>Hello</div></span>'), 'Hello')

    def test_escape(self):
        self.assertEqual(md('_hey_dude_'), '\_hey\_dude\_')


class ConversionTests(unittest.TestCase):

    def test_em(self):
        self.assertEqual(md('<em>Hello</em>'), '_Hello_')

    def test_h1(self):
        self.assertEqual(md('<h1>Hello</h1>'), 'Hello\n=====\n\n')

    def test_h2(self):
        self.assertEqual(md('<h2>Hello</h2>'), 'Hello\n-----\n\n')

    def test_hn(self):
        self.assertEqual(md('<h3>Hello</h3>'), '### Hello\n\n')
        self.assertEqual(md('<h6>Hello</h6>'), '###### Hello\n\n')

    def test_i(self):
        self.assertEqual(md('<i>Hello</i>'), '_Hello_')
