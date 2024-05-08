from constants import (
    BLOCK_TYPE_PARAGRAPH,
    BLOCK_TYPE_CODE,
    BLOCK_TYPE_HEADING,
    BLOCK_TYPE_ORDERED_LIST,
    BLOCK_TYPE_QUOTE,
    BLOCK_TYPE_UNORDERED_LIST,
    heading_pattern,
)
from htmlnode import LeafNode
import re


class TextNode:
    text_type_text = "text"
    text_type_code = "code"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_image = "image"
    text_type_link = "link"

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textnode):
        if (
            self.text == textnode.text
            and self.text_type == textnode.text_type
            and self.url == textnode.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self):
        types = {
            "text": {"tag": None, "value": self.text},
            "bold": {"tag": "b", "value": self.text},
            "italic": {"tag": "i", "value": self.text},
            "code": {"tag": "code", "value": self.text},
            "link": {
                "tag": "a",
                "props": {"href": self.url},
                "value": self.text,
            },
            "image": {
                "tag": "img",
                "value": "",
                "props": {"src": self.url, "alt": ""},
            },
        }

        if self.text_type not in types:
            raise Exception("Text type not found")

        kwargs = types[self.text_type]
        return LeafNode(**kwargs)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextNode.text_type_text:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Input nodes have bad Markdown syntax")
        else:
            split_string = node.text.split(delimiter)
            for idx, string in enumerate(split_string):
                if idx == 1:
                    new_nodes.append(TextNode(string, text_type))
                else:
                    new_nodes.append(TextNode(string, TextNode.text_type_text))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextNode.text_type_text:
            new_nodes.append(node)
        else:
            image_strings = extract_markdown_images(node.text)
            text = node.text
            if len(image_strings) > 0:
                for image_tup in image_strings:
                    split_string = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                    for idx, string in enumerate(split_string):
                        if idx == 0:
                            new_nodes.append(TextNode(string, TextNode.text_type_text))
                            new_nodes.append(
                                TextNode(
                                    image_tup[0], TextNode.text_type_image, image_tup[1]
                                )
                            )
                        elif idx == len(split_string) - 1:
                            text = string
                if text != "":
                    new_nodes.append(TextNode(text, TextNode.text_type_text))
            else:
                new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextNode.text_type_text:
            new_nodes.append(node)
        else:
            link_strings = extract_markdown_links(node.text)
            text = node.text
            if len(link_strings) > 0:
                for link_tup in link_strings:
                    split_string = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                    for idx, string in enumerate(split_string):
                        if idx == 0:
                            new_nodes.append(TextNode(string, TextNode.text_type_text))
                            new_nodes.append(
                                TextNode(
                                    link_tup[0], TextNode.text_type_link, link_tup[1]
                                )
                            )
                        elif idx == len(split_string) - 1:
                            text = string
                if text != "":
                    new_nodes.append(TextNode(text, TextNode.text_type_text))
            else:
                new_nodes.append(node)

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextNode.text_type_text)
    extracted_nodes = split_nodes_delimiter([node], "`", TextNode.text_type_code)
    extracted_nodes = split_nodes_delimiter(
        extracted_nodes, "**", TextNode.text_type_bold
    )
    extracted_nodes = split_nodes_delimiter(
        extracted_nodes, "*", TextNode.text_type_italic
    )
    extracted_nodes = split_nodes_image(extracted_nodes)
    extracted_nodes = split_nodes_link(extracted_nodes)
    return extracted_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def markdown_to_blocks(markdown):
    blocks = re.split(r"\n[ \t]*\n", markdown)
    for idx, block in enumerate(blocks):
        blocks[idx] = block.strip()
    return blocks


def block_to_block_type(block):
    if heading_pattern.search(block):
        return BLOCK_TYPE_HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BLOCK_TYPE_CODE
    elif block.startswith("> "):
        for line in block.split("\n"):
            if not line.startswith("> "):
                return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_QUOTE
    elif block.startswith("* ") or block.startswith("- "):
        for line in block.split("\n"):
            if not line.startswith("* ") and not line.startswith("- "):
                return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_UNORDERED_LIST
    elif block.startswith("1. "):
        list_count = 1
        for line in block.split("\n"):
            if not line.startswith(f"{str(list_count)}. "):
                return BLOCK_TYPE_PARAGRAPH
            list_count += 1
        return BLOCK_TYPE_ORDERED_LIST
    else:
        return BLOCK_TYPE_PARAGRAPH
