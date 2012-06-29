import unittest
from markdownify import markdownify as md


class BasicTests(unittest.TestCase):

    def test_single_tag(self):
        self.assertEqual(md('<span>Hello</span>'), 'Hello')

    def test_soup(self):
        self.assertEqual(md('<div><span>Hello</div></span>'), 'Hello')


class ConversionTests(unittest.TestCase):

    def test_h1(self):
        self.assertEqual(md('<h1>Hello</h1>'), 'Hello\n=====\n\n')

    def test_h2(self):
        self.assertEqual(md('<h2>Hello</h2>'), 'Hello\n-----\n\n')
