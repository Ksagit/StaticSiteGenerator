import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: Mismatched delimiter {delimiter}")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images:
            current_text = node.text
            for image in images:
                markdown_string = f"![{image[0]}]({image[1]})"
                new_text = current_text.split(markdown_string, 1)
                if new_text[0]:
                    new_nodes.append(TextNode(text=new_text[0], text_type=TextType.TEXT))
                new_nodes.append(TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1]))
                current_text = new_text[1]
            if current_text:
                new_nodes.append(TextNode(text=current_text, text_type=TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links:
            current_text = node.text
            for link in links:
                markdown_string = f"[{link[0]}]({link[1]})"
                new_text = current_text.split(markdown_string, 1)
                if new_text[0]:
                    new_nodes.append(TextNode(text=new_text[0], text_type=TextType.TEXT))
                new_nodes.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
                current_text = new_text[1]
            if current_text:
                new_nodes.append(TextNode(text=current_text, text_type=TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
