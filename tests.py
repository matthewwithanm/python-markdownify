import unittest
from markdownify import markdownify as md


class BasicTests(unittest.TestCase):

    def test_single_tag(self):
        self.assertEqual(md('<span>Hello</span>'), 'Hello')

    def test_soup(self):
        self.assertEqual(md('<div><span>Hello</div></span>'), 'Hello')
