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
