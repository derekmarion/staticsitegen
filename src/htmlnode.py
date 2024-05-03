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
        return None

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
