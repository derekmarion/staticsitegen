import unittest
from helpers import (
    blockquote_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    code_to_html_node,
    heading_to_html_node,
    markdown_to_html_node,
    paragraph_to_html_node,
    ordered_list_to_html_node,
    unordered_list_to_html_node,
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links,
    block_to_block_type,
    markdown_to_blocks,
)
from constants import (
    BLOCK_TYPE_CODE,
    BLOCK_TYPE_HEADING,
    BLOCK_TYPE_ORDERED_LIST,
    BLOCK_TYPE_PARAGRAPH,
    BLOCK_TYPE_QUOTE,
    BLOCK_TYPE_UNORDERED_LIST,
    TAG_TYPE_PARAGRAPH,
    TAG_TYPE_LIST_ITEM,
    TAG_TYPE_UNORDERED_LIST,
    TAG_TYPE_HEADING,
    TAG_TYPE_BOLD,
    TAG_TYPE_ITALIC,
    TAG_TYPE_DIV,
    TAG_TYPE_PREFORMATTED_TEXT,
    TAG_TYPE_CODE,
    TAG_TYPE_ORDERED_LIST,
    TAG_TYPE_QUOTE,
)
from htmlnode import ParentNode, LeafNode
from textnode import TextNode


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown_string = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is a list item
            * This is another list item
        """
        self.assertEqual(
            markdown_to_blocks(markdown_string),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n            * This is another list item",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# This is a heading block"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_HEADING)

    def test_block_to_block_type_code(self):
        block = "```This is \n some \n code```"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_CODE)

    def test_block_to_block_type_quote(self):
        block = "> Every line in a quote block\n> has to start with a '> ' sequence"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_QUOTE)

    def test_block_to_block_type_not_quote(self):
        block = "> Every line in a quote block\n has to start with a '> ' sequence"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "* This is a list item\n            * This is another list item"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is \n2. an ordered list\n3. of multiple lines"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_ORDERED_LIST)

    def test_block_to_block_type_not_ordered_list(self):
        block = "1. This is \n3. an ordered list\n3. that is incorrectly formatted"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown_string = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is a list item
            * This is another list item
        """
        child_node_1 = ParentNode(
            TAG_TYPE_HEADING + "1", [LeafNode(None, "This is a heading")]
        )
        child_node_2 = ParentNode(
            TAG_TYPE_PARAGRAPH,
            [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode(TAG_TYPE_BOLD, "bold"),
                LeafNode(None, " and "),
                LeafNode(TAG_TYPE_ITALIC, "italic"),
                LeafNode(None, " words inside of it.")
            ],
        )
        child_node_3 = ParentNode(
            TAG_TYPE_UNORDERED_LIST,
            [
                ParentNode(TAG_TYPE_LIST_ITEM, [LeafNode(None, "This is a list item")]),
                ParentNode(TAG_TYPE_LIST_ITEM, [LeafNode(None, "This is another list item")])
            ]
        )
        result_node = markdown_to_html_node(markdown_string)
        expected_node = ParentNode(TAG_TYPE_DIV, [child_node_1, child_node_2, child_node_3])
        self.assertEqual(result_node, expected_node)


class TestSplitNodesDelimiter(unittest.TestCase):
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


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    # need to test multiple nodes passed in
    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNode.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextNode.text_type_text),
                TextNode(
                    "image",
                    TextNode.text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextNode.text_type_text),
                TextNode(
                    "second image",
                    TextNode.text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_split_nodes_image_single(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            TextNode.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextNode.text_type_text),
                TextNode(
                    "image",
                    TextNode.text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
            ],
        )

    def test_split_nodes_image_single_with_ending_node(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and some additional text",
            TextNode.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextNode.text_type_text),
                TextNode(
                    "image",
                    TextNode.text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and some additional text", TextNode.text_type_text),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNode.text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNode.text_type_text),
                TextNode(
                    "link",
                    TextNode.text_type_link,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextNode.text_type_text),
                TextNode(
                    "second link",
                    TextNode.text_type_link,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_split_nodes_link_single(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            TextNode.text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNode.text_type_text),
                TextNode(
                    "link",
                    TextNode.text_type_link,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
            ],
        )

    def test_split_nodes_link_single_with_ending_node(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and some additional text",
            TextNode.text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNode.text_type_text),
                TextNode(
                    "link",
                    TextNode.text_type_link,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and some additional text", TextNode.text_type_text),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextNode.text_type_text),
                TextNode("text", TextNode.text_type_bold),
                TextNode(" with an ", TextNode.text_type_text),
                TextNode("italic", TextNode.text_type_italic),
                TextNode(" word and a ", TextNode.text_type_text),
                TextNode("code block", TextNode.text_type_code),
                TextNode(" and an ", TextNode.text_type_text),
                TextNode(
                    "image",
                    TextNode.text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", TextNode.text_type_text),
                TextNode("link", TextNode.text_type_link, "https://boot.dev"),
            ],
        )


class TestBlockToHTML(unittest.TestCase):
    # print(f"result node: {result_node}")
    # print(f"expected node: {expected_node}")
    def test_blockquote_to_html_node_no_inline_elements(self):
        block = "> This is a quote.\n> And each line starts with a >"
        inline_children = LeafNode(
            None, "This is a quote. And each line starts with a >"
        )
        result_node = blockquote_to_html_node(block)
        expected_node = ParentNode(TAG_TYPE_QUOTE, [inline_children])
        self.assertEqual(result_node, expected_node)

    def test_paragraph_to_html_node_no_inline_elements(self):
        block = "This is just a regular paragraph with no nested elements."
        inline_children = LeafNode(
            None, "This is just a regular paragraph with no nested elements."
        )
        result_node = paragraph_to_html_node(block)
        expected_node = ParentNode(TAG_TYPE_PARAGRAPH, [inline_children])
        self.assertEqual(result_node, expected_node)

    def test_code_to_html_node_no_inline_elements(self):
        block = "```This is a code block with no nested elements```"
        inline_children = LeafNode(None, "This is a code block with no nested elements")
        result_node = code_to_html_node(block)
        expected_node = ParentNode(
            TAG_TYPE_PREFORMATTED_TEXT, [ParentNode(TAG_TYPE_CODE, [inline_children])]
        )
        self.assertEqual(result_node, expected_node)

    def test_heading_to_html_node_no_inline_elements(self):
        block = "## This is a heading which should result in an h2 tag"
        inline_children = LeafNode(
            None, "This is a heading which should result in an h2 tag"
        )
        result_node = heading_to_html_node(block)
        expected_node = ParentNode(TAG_TYPE_HEADING + "2", [inline_children])
        self.assertEqual(result_node, expected_node)

    def test_unordered_list_to_html_node_no_inline_elements(self):
        block = "- This is \n* a list\n- with multiple types of\n* bullets\n     * and some extraneous whitespace"
        child_node_1 = ParentNode(TAG_TYPE_LIST_ITEM, [LeafNode(None, "This is")])
        child_node_2 = ParentNode(TAG_TYPE_LIST_ITEM, [LeafNode(None, "a list")])
        child_node_3 = ParentNode(
            TAG_TYPE_LIST_ITEM, [LeafNode(None, "with multiple types of")]
        )
        child_node_4 = ParentNode(TAG_TYPE_LIST_ITEM, [LeafNode(None, "bullets")])
        child_node_5 = ParentNode(
            TAG_TYPE_LIST_ITEM, [LeafNode(None, "and some extraneous whitespace")]
        )
        expected_node = ParentNode(
            TAG_TYPE_UNORDERED_LIST,
            [child_node_1, child_node_2, child_node_3, child_node_4, child_node_5],
        )
        result_node = unordered_list_to_html_node(block)
        self.assertEqual(result_node, expected_node)

    def test_ordered_list_to_html_node_no_inline_elements(self):
        block = "1. This is \n2. an ordered list\n3. of multiple lines"
        child_node_1 = ParentNode(TAG_TYPE_LIST_ITEM, [LeafNode(None, "This is")])
        child_node_2 = ParentNode(
            TAG_TYPE_LIST_ITEM, [LeafNode(None, "an ordered list")]
        )
        child_node_3 = ParentNode(
            TAG_TYPE_LIST_ITEM, [LeafNode(None, "of multiple lines")]
        )
        expected_node = ParentNode(
            TAG_TYPE_ORDERED_LIST, [child_node_1, child_node_2, child_node_3]
        )
        result_node = ordered_list_to_html_node(block)
        self.assertEqual(result_node, expected_node)


if __name__ == "__main__":
    unittest.main()
