import unittest
from markdown_converter import block_to_code_node, block_to_heading_node, block_to_paragraph_node, block_to_quote_node, block_to_unordered_list_node, text_to_children


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_text_to_children_simple(self):
        text = "This is **bold** and *italic* text."
        children = text_to_children(text)
        self.assertEqual(len(children), 5)
        self.assertEqual(children[0].to_html(), "This is ")
        self.assertEqual(children[1].to_html(), "<b>bold</b>")
        self.assertEqual(children[2].to_html(), " and ")
        self.assertEqual(children[3].to_html(), "<i>italic</i>")
        self.assertEqual(children[4].to_html(), " text.")

    def test_paragraph_block_conversion(self):
        block = "This is a simple paragraph.\nIt continues on a new line."
        node = block_to_paragraph_node(block)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.to_html(), "<p>This is a simple paragraph.\nIt continues on a new line.</p>")
        block_inline = "This is **bold** text."
        node_inline = block_to_paragraph_node(block_inline)
        self.assertEqual(node_inline.to_html(), "<p>This is <b>bold</b> text.</p>")


    def test_heading_block_conversion(self):
        block1 = "# Heading One"
        node1 = block_to_heading_node(block1)
        self.assertEqual(node1.tag, "h1")
        self.assertEqual(node1.to_html(), "<h1>Heading One</h1>")

        block3 = "### Heading Three with `code`"
        node3 = block_to_heading_node(block3)
        self.assertEqual(node3.tag, "h3")
        self.assertEqual(node3.to_html(), "<h3>Heading Three with <code>code</code></h3>")

    def test_code_block_conversion(self):
        block = "```python\nprint('hello')\n```"
        node = block_to_code_node(block)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "code")
        self.assertEqual(node.children[0].value, "python\nprint('hello')\n")
        self.assertEqual(node.to_html(), "<pre><code>python\nprint('hello')\n</code></pre>")

    def test_quote_block_conversion(self):
        block = "> This is a quote.\n> Second line.\n> Third line."
        node = block_to_quote_node(block)
        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(node.to_html(), "<blockquote>This is a quote.\nSecond line.\nThird line.</blockquote>")

    def test_unordered_list_block_conversion(self):
        block = "- Item 1\n* Item 2\n- Item 3"
        node = block_to_unordered_list_node(block)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[0].to_html(), "<li>Item 1</li>")
        self.assertEqual(node.to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

if __name__ == "main":
    unittest.main()