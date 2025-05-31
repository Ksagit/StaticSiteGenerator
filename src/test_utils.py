import unittest
from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_bold_delimiter(self):
        node = TextNode("This is a **bold** text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_multiple_bold_delimiters(self):
        node = TextNode(
            "This is **bold** and also **very bold** text.", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and also ", TextType.TEXT),
            TextNode("very bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_single_italic_delimiter(self):
        node = TextNode("This is *italic* text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_single_code_delimiter(self):
        node = TextNode("This is `code` text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_no_delimiter(self):
        node = TextNode("This is regular text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [TextNode("This is regular text.", TextType.TEXT)]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        self.assertEqual(new_nodes[0], expected_nodes[0])

    def test_odd_delimiter_number_raises_exception(self):
        node = TextNode("This is a **bold text.", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(cm.exception), "Odd delimiter number")

    def test_mixed_nodes_input(self):
        node1 = TextNode("Normal text.", TextType.TEXT)
        node2 = TextNode("`code` snippet.", TextType.CODE)
        node3 = TextNode("This is **bold** text.", TextType.TEXT)
        node4 = TextNode("Another normal node.", TextType.TEXT)

        old_nodes = [node1, node2, node3, node4]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Normal text.", TextType.TEXT),
            TextNode("`code` snippet.", TextType.CODE),
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("Another normal node.", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_delimiter_inside_non_text_node(self):
        node = TextNode("This is `code` with **bold** inside.", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [TextNode("This is `code` with **bold** inside.", TextType.CODE)]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        self.assertEqual(new_nodes[0], expected_nodes[0])


if __name__ == "__main__":
    unittest.main()