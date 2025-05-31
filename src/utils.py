from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if delimiter in node.text:
                result = node.text.split(delimiter)
                if len(result) % 2 == 0:
                    raise Exception("Odd delimiter number")
                for i, res in enumerate(result):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(text=res, text_type=TextType.TEXT))
                    elif res and i % 2 == 1:
                        new_nodes.append(TextNode(text=res, text_type=text_type))   
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes