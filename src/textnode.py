from htmlnode import LeafNode


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
