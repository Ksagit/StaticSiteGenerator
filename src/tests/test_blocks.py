import unittest
from blocks import BlockType, block_to_block_type, markdown_to_blocks

class TestSplitBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_multiple_paragraphs(self):
        markdown = "This is block one.\n\nThis is block two.\n\nThis is block three."
        expected = ["This is block one.", "This is block two.", "This is block three."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_with_extra_newlines(self):
        markdown = "Block 1\n\n\n\nBlock 2\n\n  \nBlock 3  "
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_with_heading_list_code(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item\n\n```python\nprint('hello')\n```\n\nAnother paragraph."
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            "```python\nprint('hello')\n```",
            "Another paragraph."
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_only_newlines_and_whitespace(self):
        markdown = "\n\n  \n\t\n \n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_single_block_no_trailing_newline(self):
        markdown = "Just a single block of text."
        expected = ["Just a single block of text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_single_block_trailing_newline(self):
        markdown = "Single block with trailing newline.\n"
        expected = ["Single block with trailing newline."]
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_paragraph(self):
        block = "This is a regular paragraph of text.\nIt spans multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##No space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_code(self):
        block = "```python\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("`single backtick`"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code without closing"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("code without opening```"), BlockType.PARAGRAPH)


    def test_quote(self):
        block = "> This is a quote.\n> It spans multiple lines.\n> With more quoted text."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block_mixed = "> Line 1\nLine 2 not a quote"
        self.assertEqual(block_to_block_type(block_mixed), BlockType.PARAGRAPH)
        block_empty_line = "> Line 1\n>\n> Line 2"
        self.assertEqual(block_to_block_type(block_empty_line), BlockType.QUOTE)

    def test_unordered_list(self):
        block_dash = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block_dash), BlockType.UNORDERED_LIST)
        block_asterisk = "* Item A\n* Item B"
        self.assertEqual(block_to_block_type(block_asterisk), BlockType.UNORDERED_LIST)
        block_mixed_markers = "- Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(block_mixed_markers), BlockType.UNORDERED_LIST)
        block_no_space = "-Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block_no_space), BlockType.PARAGRAPH)
        block_mixed_with_paragraph = "- Item 1\nRegular paragraph line"
        self.assertEqual(block_to_block_type(block_mixed_with_paragraph), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block_start_not_one = "2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block_start_not_one), BlockType.PARAGRAPH)
        block_non_sequential = "1. Item\n3. Another item"
        self.assertEqual(block_to_block_type(block_non_sequential), BlockType.PARAGRAPH)
        block_no_space = "1.Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block_no_space), BlockType.PARAGRAPH)
        block_only_numbers = "1.\n2."
        self.assertEqual(block_to_block_type(block_only_numbers), BlockType.PARAGRAPH)

    def test_mixed_types_order_of_checks(self):
        self.assertEqual(block_to_block_type("# > Quote Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```# Code Heading\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> 1. List Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("1. # Heading List"), BlockType.ORDERED_LIST)

    def test_empty_block(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_leading_trailing_whitespace(self):
        self.assertEqual(block_to_block_type("  # Heading  "), BlockType.HEADING)
        self.assertEqual(block_to_block_type("  ```code```  "), BlockType.CODE)
        self.assertEqual(block_to_block_type("  > quote  "), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("  - list  "), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("  1. list  "), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("  paragraph  "), BlockType.PARAGRAPH)