from htmlnode import LeafNode


class TextNode:
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

    def text_node_to_html_node(text_node):
        types = {
            "text": {"tag": None, "value": text_node.text},
            "bold": {"tag": "b", "value": text_node.text},
            "italic": {"tag": "i", "value": text_node.text},
            "code": {"tag": "code", "value": text_node.text},
            "link": {
                "tag": "a",
                "props": {"href": text_node.url},
                "value": text_node.text,
            },
            "image": {
                "tag": "img",
                "value": "",
                "props": {"src": text_node.url, "alt": ""},
            },
        }

        if text_node.text_type not in types:
            raise Exception("Text type not found")

        kwargs = types[text_node.text_type]
        return LeafNode(**kwargs)
