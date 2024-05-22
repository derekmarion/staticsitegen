import re

from constants import (
    heading_pattern,
    BLOCK_TYPE_CODE,
    BLOCK_TYPE_HEADING,
    BLOCK_TYPE_ORDERED_LIST,
    BLOCK_TYPE_PARAGRAPH,
    BLOCK_TYPE_QUOTE,
    BLOCK_TYPE_UNORDERED_LIST,
    TAG_TYPE_DIV,
    TAG_TYPE_HEADING,
    TAG_TYPE_ORDERED_LIST,
    TAG_TYPE_UNORDERED_LIST,
    TAG_TYPE_LIST_ITEM,
    TAG_TYPE_PARAGRAPH,
    TAG_TYPE_QUOTE,
    TAG_TYPE_PREFORMATTED_TEXT,
    TAG_TYPE_CODE,
)

from textnode import TextNode

from htmlnode import ParentNode


# Text processing functions
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
            if not line.strip().startswith("* ") and not line.strip().startswith("- "):
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


# Inline TextNode/HTMLNode processing functions
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


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.text_node_to_html_node()
        children.append(html_node)
    return children


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    # Create ParentNode based on block type
    if block_type == BLOCK_TYPE_QUOTE:
        return blockquote_to_html_node(block)
    elif block_type == BLOCK_TYPE_PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BLOCK_TYPE_HEADING:
        return heading_to_html_node(block)
    elif block_type == BLOCK_TYPE_CODE:
        return code_to_html_node(block)
    elif block_type == BLOCK_TYPE_UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BLOCK_TYPE_ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError("Invalid block type")


# HTML tag wrapping functions for inline children
def blockquote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    inline_children = text_to_children(content)
    return ParentNode(TAG_TYPE_QUOTE, inline_children)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    inline_children = text_to_children(paragraph)
    return ParentNode(TAG_TYPE_PARAGRAPH, inline_children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[3:-3]
    inline_children = text_to_children(text)
    code = ParentNode(TAG_TYPE_CODE, inline_children)
    return ParentNode(TAG_TYPE_PREFORMATTED_TEXT, [code])


def heading_to_html_node(block):
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break
    if heading_level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {heading_level}")
    text = block[heading_level + 1 :]
    inline_children = text_to_children(text)
    return ParentNode(TAG_TYPE_HEADING + str(heading_level), inline_children)


def unordered_list_to_html_node(text):
    child_list_items = []
    for list_item in text.split("\n"):
        # Remove any extra whitespace, bullet and space at list item start
        list_item = list_item.strip()
        list_item = list_item[2:]
        inline_children = text_to_children(list_item)
        child_list_items.append(ParentNode(TAG_TYPE_LIST_ITEM, inline_children))
    return ParentNode(TAG_TYPE_UNORDERED_LIST, child_list_items)

def ordered_list_to_html_node(text):
    child_list_items = []
    for list_item in text.split("\n"):
        # Remove any extra whitespace, number, period and space at list item start
        list_item = list_item.strip()
        list_item = list_item[3:]
        inline_children = text_to_children(list_item)
        child_list_items.append(ParentNode(TAG_TYPE_LIST_ITEM, inline_children))
    return ParentNode(TAG_TYPE_ORDERED_LIST, child_list_items)


# Convert full markdown text string to properly nested HTML nodes
def markdown_to_html_node(markdown):
    # Break markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # Convert blocks to HTMLNodes
    child_nodes = []
    for block in blocks:
        child_nodes.append(block_to_html_node(block))

    return ParentNode(TAG_TYPE_DIV, child_nodes)
