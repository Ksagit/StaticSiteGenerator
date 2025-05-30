from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(TextNode):
    if TextNode.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=TextNode.text)
    if TextNode.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=TextNode.text)
    if TextNode.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=TextNode.text)
    if TextNode.text_type == TextType.CODE:
        return LeafNode(tag="code", value=TextNode.text)
    if TextNode.text_type == TextType.LINK:
        return LeafNode(tag="a", value=TextNode.text, props={"href": TextNode.url})
    if TextNode.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": TextNode.url, "alt": TextNode.text})
    else:
        raise Exception("Invalid TextType")