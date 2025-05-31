from blocks import BlockType, block_to_block_type, markdown_to_blocks
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node
from node_processing import text_to_textnodes


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def block_to_paragraph_node(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def block_to_heading_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    if not (1 <= level <= 6) or block[level] != ' ':
        raise ValueError("Invalid heading block format")
    
    heading_text = block[level+1:].strip()
    children = text_to_children(heading_text)
    return ParentNode(f"h{level}", children)

def block_to_code_node(block):
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError("Invalid code block format")

    code_content = block[3:-3]
    code_node = LeafNode("code", code_content)
    return ParentNode("pre", [code_node])

def block_to_quote_node(block):
    lines = block.split('\n')
    cleaned_lines = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError("Invalid quote block format")
        cleaned_lines.append(line[1:].strip())
    
    quote_content = "\n".join(cleaned_lines)
    children = text_to_children(quote_content)
    return ParentNode("blockquote", children)

def block_to_unordered_list_node(block):
    lines = block.split('\n')
    list_items = []
    for line in lines:
        if line.startswith("- "):
            item_text = line[2:].strip()
        elif line.startswith("* "):
            item_text = line[2:].strip()
        else:
            raise ValueError("Invalid unordered list block format")
        
        list_items.append(ParentNode("li", text_to_children(item_text)))
    
    return ParentNode("ul", list_items)

def block_to_ordered_list_node(block):
    lines = block.split('\n')
    list_items = []
    for i, line in enumerate(lines):
        expected_start = f"{i + 1}."
        if not line.startswith(expected_start + " "):
            raise ValueError("Invalid ordered list block format: incorrect numbering")
        
        item_text = line[len(expected_start) + 1:].strip()
        list_items.append(ParentNode("li", text_to_children(item_text)))
    
    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    root_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            root_children.append(block_to_paragraph_node(block))
        elif block_type == BlockType.HEADING:
            root_children.append(block_to_heading_node(block))
        elif block_type == BlockType.CODE:
            root_children.append(block_to_code_node(block))
        elif block_type == BlockType.QUOTE:
            root_children.append(block_to_quote_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            root_children.append(block_to_unordered_list_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            root_children.append(block_to_ordered_list_node(block))
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode("div", root_children)

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            title = stripped_line[2:].strip()
            if not title:
                raise ValueError("Markdown has an empty H1 heading.")
            return title
    raise ValueError("Markdown has no H1 heading.")