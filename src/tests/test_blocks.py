import unittest
from blocks import markdown_to_blocks

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