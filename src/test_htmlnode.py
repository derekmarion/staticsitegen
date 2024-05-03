import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html1(self):
        htmlnode = HTMLNode(
            "a", "this is a link", "children", {"href": "https://example.com"}
        )
        self.assertEqual(htmlnode.props_to_html(), ' href="https://example.com"')

    def test_props_to_html2(self):
        htmlnode = HTMLNode(
            "a",
            "this is a link",
            "children",
            {"href": "https://google.com", "target": "_blank"},
        )
        self.assertEqual(
            htmlnode.props_to_html(), ' href="https://google.com" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leafnode = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leafnode.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        leafnode = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertEqual(
            leafnode.to_html(), '<a href="https://google.com">Click me!</a>'
        )

    def test_no_value(self):
        with self.assertRaises(ValueError):
            leafnode = LeafNode("p", None)
            leafnode.to_html()


if __name__ == "__main__":
    unittest.main()
