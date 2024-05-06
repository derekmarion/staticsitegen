import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        parentnode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parentnode.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        parentnode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "some_css"},
        )

        self.assertEqual(
            parentnode.to_html(),
            '<p class="some_css"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        )

    def test_parent_in_parent(self):
        parentnode = ParentNode(
            "h1",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
            ],
        )
        self.assertEqual(
            parentnode.to_html(),
            "<h1><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></h1>",
        )

    def test_parent_in_parent_in_parent(self):
        parentnode = ParentNode(
            "title",
            [
                ParentNode(
                    "h1",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
                    ],
                ),
            ],
        )
        self.assertEqual(
            parentnode.to_html(),
            "<title><h1><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></h1></title>",
        )

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            parentnode = ParentNode(None, LeafNode("b", "Bold text"))
            parentnode.to_html()

    def test_no_children(self):
        with self.assertRaises(ValueError):
            parentnode = ParentNode("p", None)
            parentnode.to_html()


if __name__ == "__main__":
    unittest.main()
