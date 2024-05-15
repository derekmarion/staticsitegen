from constants import (
    TAG_TYPE_HEADING,
    TAG_TYPE_LIST_ITEM,
    TAG_TYPE_UNORDERED_LIST,
    TAG_TYPE_ORDERED_LIST,
    TAG_TYPE_DIV,
)

from constants import BLOCK_TYPE_QUOTE

from textnode import markdown_to_blocks, block_to_block_type, text_to_textnodes


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props = []
        if self.props is not None:
            for k, v in self.props.items():
                prop = f' {k}="{v}"'
                props.append(prop)
            return "".join(props)
        return ""

    def __eq__(self, htmlnode):
        if (
            self.tag == htmlnode.tag
            and self.value == htmlnode.value
            and self.children == htmlnode.children
            and self.props == htmlnode.props
        ):
            return True
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node requires a value")
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"{self.value}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parentnode requires a tag")
        if self.children is None:
            raise ValueError("Parentnode requires children")
        output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            output += child.to_html()
        return f"{output}</{self.tag}>"


def blockquote_to_html_node(text):
    return LeafNode("blockquote", text)


def paragraph_to_html_node(text):
    return LeafNode("p", text)


def code_to_html_node(text):
    child_node = LeafNode("code", text)
    return ParentNode("pre", [child_node])


def heading_to_html_node(text):
    tag = TAG_TYPE_HEADING + str(text.count("#"))
    return LeafNode(tag, text)


def unordered_list_to_html_node(text):
    child_list_items = []
    for list_item in text.split("\n"):
        list_item = list_item[1:]
        list_item = list_item.strip()
        child_list_items.append(LeafNode(TAG_TYPE_LIST_ITEM, list_item))
    return ParentNode(TAG_TYPE_UNORDERED_LIST, child_list_items)


def ordered_list_to_html_node(text):
    child_list_items = []
    for list_item in text.split("\n"):
        list_item = list_item.strip()
        child_list_items.append(LeafNode(TAG_TYPE_LIST_ITEM, list_item))
    return ParentNode(TAG_TYPE_ORDERED_LIST, child_list_items)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        if block_to_block_type(block) == BLOCK_TYPE_QUOTE:
            text_nodes = text_to_textnodes(block)
    return ParentNode(TAG_TYPE_DIV, child_nodes)
