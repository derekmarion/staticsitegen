import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    blockquote_to_html_node,
    paragraph_to_html_node,
    code_to_html_node,
    heading_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
)
from constants import (
    TAG_TYPE_CODE,
    TAG_TYPE_PREFORMATTED_TEXT,
    TAG_TYPE_PARAGRAPH,
    TAG_TYPE_QUOTE,
    TAG_TYPE_LIST_ITEM,
    TAG_TYPE_UNORDERED_LIST,
    TAG_TYPE_ORDERED_LIST,
    TAG_TYPE_HEADING,
    TAG_TYPE_BOLD,
    TAG_TYPE_ITALIC,
    TAG_TYPE_DIV,
)


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

    def test_eq(self):
        htmlnode1 = HTMLNode(
            "a", "this is a link", "children", {"href": "https://example.com"}
        )
        htmlnode2 = HTMLNode(
            "a", "this is a link", "children", {"href": "https://example.com"}
        )
        self.assertEqual(htmlnode1.__eq__(htmlnode2), True)


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


class TestBlockToHTML(unittest.TestCase):
    def test_block_blockquote_to_html_node(self):
        block = "> Every line in a quote block\n> has to start with a '> ' sequence"
        html_node = blockquote_to_html_node(block)
        comp_node = LeafNode(TAG_TYPE_QUOTE, block)
        self.assertEqual(html_node, comp_node)

    def test_paragraph_to_html_node(self):
        block = "This is just a plain old paragraph block.\nIt's got two lines in it"
        html_node = paragraph_to_html_node(block)
        comp_node = LeafNode(TAG_TYPE_PARAGRAPH, block)
        self.assertEqual(html_node, comp_node)

    def test_code_to_html_node(self):
        block = "```This is a code block```"
        child_node = LeafNode(TAG_TYPE_CODE, block)
        comp_node = ParentNode(TAG_TYPE_PREFORMATTED_TEXT, [child_node])
        html_node = code_to_html_node(block)
        self.assertEqual(html_node, comp_node)

    def test_heading_to_html_node(self):
        block = "## This is markdown heading that should result in an <h2> tag"
        comp_node = LeafNode("h2", block)
        html_node = heading_to_html_node(block)
        self.assertEqual(html_node, comp_node)

    def test_unordered_list_to_html_node(self):
        block = "- This is \n* a list\n- with multiple types of\n* bullets"
        child_node_1 = LeafNode(TAG_TYPE_LIST_ITEM, "This is")
        child_node_2 = LeafNode(TAG_TYPE_LIST_ITEM, "a list")
        child_node_3 = LeafNode(TAG_TYPE_LIST_ITEM, "with multiple types of")
        child_node_4 = LeafNode(TAG_TYPE_LIST_ITEM, "bullets")
        comp_node = ParentNode(
            TAG_TYPE_UNORDERED_LIST,
            [child_node_1, child_node_2, child_node_3, child_node_4],
        )
        html_node = unordered_list_to_html_node(block)
        self.assertEqual(html_node, comp_node)

    def test_ordered_list_to_html_node(self):
        block = "1. This is \n2. an ordered list\n3. of multiple lines"
        child_node_1 = LeafNode(TAG_TYPE_LIST_ITEM, "1. This is")
        child_node_2 = LeafNode(TAG_TYPE_LIST_ITEM, "2. an ordered list")
        child_node_3 = LeafNode(TAG_TYPE_LIST_ITEM, "3. of multiple lines")
        comp_node = ParentNode(
            TAG_TYPE_ORDERED_LIST, [child_node_1, child_node_2, child_node_3]
        )
        html_node = ordered_list_to_html_node(block)
        self.assertEqual(html_node, comp_node)

    def test_markdown_to_html_node(self):
        markdown_string = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is a list item
            * This is another list item
        """
        child_node_1 = LeafNode(TAG_TYPE_HEADING, "This is a heading")
        child_node_2 = LeafNode(TAG_TYPE_BOLD, "bold")
        child_node_3 = LeafNode(TAG_TYPE_ITALIC, "italic")
        child_node_4 = LeafNode(
            TAG_TYPE_PARAGRAPH, "This is a paragraph of text. It has some "
        )
        child_node_5 = LeafNode(TAG_TYPE_BOLD, "bold")
        child_node_6 = LeafNode(TAG_TYPE_PARAGRAPH, " and ")
        child_node_7 = LeafNode(TAG_TYPE_ITALIC, "italic")
        child_node_8 = LeafNode(TAG_TYPE_PARAGRAPH, " words inside of it.")
        child_node_10 = LeafNode(TAG_TYPE_LIST_ITEM, "This is a list item")
        child_node_11 = LeafNode(TAG_TYPE_LIST_ITEM, "This is another list item")
        child_node_9 = ParentNode(
            TAG_TYPE_UNORDERED_LIST,
            [child_node_10, child_node_11],
        )
        html_node = markdown_to_html_node(markdown_string)
        comp_node = ParentNode(
            TAG_TYPE_DIV,
            [
                child_node_1,
                child_node_2,
                child_node_3,
                child_node_4,
                child_node_5,
                child_node_6,
                child_node_7,
                child_node_8,
                child_node_9,
            ],
        )
        self.assertEqual(html_node, comp_node)


if __name__ == "__main__":
    unittest.main()
