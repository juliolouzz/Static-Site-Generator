class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children = children if children is not None else []
        self.props = props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Child classes will override this method to render themselves as HTML")

    def props_to_html(self):
        return ''.join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self) -> str:
        return (f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={self.children}, props={self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode requires a value")

        super().__init__(tag=tag, value=value, children=None, props=props)
        self.children = None

    def to_html(self):
        # This Exception is handled on __init__ method, but I added to cover all possibilities.
        if self.value is None:
            raise ValueError("Value is required to render HTML")
        if self.tag is None:
            return self.value

        attributes = self.props_to_html()
        return f'<{self.tag}{attributes}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode requires a tag")
        if not self.children or not isinstance(self.children, list):
            raise ValueError("ParentNode requires a list of children")

        attributes = self.props_to_html()
        children_html = ''.join(child.to_html() for child in self.children)

        return f'<{self.tag}{attributes}>{children_html}</{self.tag}>'

    def __repr__(self) -> str:
        return f"tag={self.tag}, children={self.children}, props={self.props}"
        
