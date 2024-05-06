import unittest
from textnode import TextNode
from htmlnode import LeafNode


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


if __name__ == "__main__":
    unittest.main()
