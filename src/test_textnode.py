import unittest
from textnode import TextNode, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq_1(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_not_eq_2(self):
        node = TextNode("This is a text node", "bold", "https://some-url.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is some text", "text")
        leaf_node = text_node.text_node_to_html_node()
        self.assertIsNone(leaf_node.tag)
        self.assertEqual(leaf_node.value, "This is some text")
        self.assertIsNone(leaf_node.props)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("This is some text", "bold")
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "This is some text")
        self.assertIsNone(leaf_node.props)

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("This is some text", "italic")
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "This is some text")
        self.assertIsNone(leaf_node.props)

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("This is some text", "code")
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "This is some text")
        self.assertIsNone(leaf_node.props)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("This is some text", "link", "https://example.com")
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "This is some text")
        self.assertEqual(leaf_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("This is some text", "image", "https://example.com")
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(leaf_node.props, {"src": "https://example.com", "alt": ""})

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", "text")
        self.assertEqual(
            split_nodes_delimiter([node], "`", "code"),
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ],
        )

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a *bold* word", "text")
        self.assertEqual(
            split_nodes_delimiter([node], "*", "bold"),
            [
                TextNode("This is text with a ", "text"),
                TextNode("bold", "bold"),
                TextNode(" word", "text"),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a **italic** word", "text")
        self.assertEqual(
            split_nodes_delimiter([node], "**", "italic"),
            [
                TextNode("This is text with a ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word", "text"),
            ],
        )

    def test_split_nodes_delimiter_non_text_type(self):
        nodes = [
            TextNode("This is text with a *bold* word", "text"),
            TextNode("This is a non text type node", "code"),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "*", "bold"),
            [
                TextNode("This is text with a ", "text"),
                TextNode("bold", "bold"),
                TextNode(" word", "text"),
                TextNode("This is a non text type node", "code"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
