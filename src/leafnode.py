from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
        if self.value is None and self.tag is not None:
             raise ValueError("LeafNode with a tag must have a non-None value")

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None for rendering.")
        elif not self.tag:
            return self.value
        else:
            props_list = []
            if self.props:
                for key, value in self.props.items():
                    props_list.append(f"{key}=\"{value}\"")
                props_str = " ".join(props_list)
            else:
                props_str = ""
            space_and_props = " " + props_str if props_str else ""
            return f"<{self.tag}{space_and_props}>{self.value}</{self.tag}>"
        
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return NotImplemented

        return (
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )