from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        elif self.children == None or len(self.children) == 0:
            raise ValueError("No children")
        else:
            return f"<{self.tag}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"