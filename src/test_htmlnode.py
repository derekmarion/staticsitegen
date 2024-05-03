import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html1(self):
        htmlnode = HTMLNode(
            "a", "this is a link", "children", {"href": "https://example.com"}
        )
        self.assertEqual(htmlnode.props_to_html(), ' href="https://example.com"')

    def test_props_to_html2(self):
        htmlnode = HTMLNode(
            "a", "this is a link", "children", {"href": "https://google.com", "target": "_blank"}
        )
        self.assertEqual(htmlnode.props_to_html(), ' href="https://google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()
