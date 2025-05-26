class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self, properties):
        string = ""
        for key, value in properties.items():
            string += f"{key}=\"{value}\" "
        return string
    
    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag}, "
            f"value={self.value}, "
            f"children={self.children}, "
            f"props={self.props})"
        )

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented

        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )