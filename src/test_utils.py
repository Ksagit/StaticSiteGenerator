import unittest
from textnode import TextNode, TextType
from utils import split_nodes_delimiter, split_nodes_image, split_nodes_link


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

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_image_various_scenarios(self):
        nodes_with_image = [TextNode("This is some text with an ![image](img.jpg) and more.", TextType.TEXT)]
        expected_image_split = [
            TextNode("This is some text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and more.", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_image(nodes_with_image), expected_image_split
        )

        nodes_multiple_images = [
            TextNode("![img1](url1) text ![img2](url2) end", TextType.TEXT)
        ]
        expected_multiple_images_split = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" text ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_image(nodes_multiple_images),
            expected_multiple_images_split,
        )

        nodes_no_image = [TextNode("No images here.", TextType.TEXT)]
        expected_no_image_split = [
            TextNode("No images here.", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_image(nodes_no_image), expected_no_image_split
        )

        nodes_image_start = [TextNode("![image](img.png) starts here.", TextType.TEXT)]
        expected_image_start = [
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" starts here.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes_image_start), expected_image_start)

        nodes_image_end = [TextNode("Ends with ![image](img.gif)", TextType.TEXT)]
        expected_image_end = [
            TextNode("Ends with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.gif"),
        ]
        self.assertEqual(split_nodes_image(nodes_image_end), expected_image_end)

        nodes_image_only = [TextNode("![image](img.svg)", TextType.TEXT)]
        expected_image_only = [TextNode("image", TextType.IMAGE, "img.svg")]
        self.assertEqual(split_nodes_image(nodes_image_only), expected_image_only)

        nodes_mixed_types = [
            TextNode("plain text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("![img](url)", TextType.TEXT),
        ]
        expected_mixed_types = [
            TextNode("plain text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("img", TextType.IMAGE, "url"),
        ]
        self.assertEqual(split_nodes_image(nodes_mixed_types), expected_mixed_types)

    def test_split_nodes_link_various_scenarios(self):
        nodes_with_link = [
            TextNode("This is some text with a [link](link.html) and more.", TextType.TEXT)
        ]
        expected_link_split = [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "link.html"),
            TextNode(" and more.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes_with_link), expected_link_split)

        nodes_multiple_links = [
            TextNode("[link1](url1) text [link2](url2) end", TextType.TEXT)
        ]
        expected_multiple_links_split = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" text ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_link(nodes_multiple_links), expected_multiple_links_split
        )

        nodes_no_link = [TextNode("No links here.", TextType.TEXT)]
        expected_no_link_split = [TextNode("No links here.", TextType.TEXT)]
        self.assertEqual(split_nodes_link(nodes_no_link), expected_no_link_split)

        nodes_link_start = [TextNode("[link](page.html) starts here.", TextType.TEXT)]
        expected_link_start = [
            TextNode("link", TextType.LINK, "page.html"),
            TextNode(" starts here.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes_link_start), expected_link_start)

        nodes_link_end = [TextNode("Ends with [link](end.org)", TextType.TEXT)]
        expected_link_end = [
            TextNode("Ends with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "end.org"),
        ]
        self.assertEqual(split_nodes_link(nodes_link_end), expected_link_end)

        nodes_link_only = [TextNode("[link](only.com)", TextType.TEXT)]
        expected_link_only = [TextNode("link", TextType.LINK, "only.com")]
        self.assertEqual(split_nodes_link(nodes_link_only), expected_link_only)

        nodes_with_image_and_link_text = [
            TextNode("An image ![img](i.png) and a link [link](l.html).", TextType.TEXT)
        ]
        # split_nodes_link should ignore the image part
        expected_link_only_from_mixed = [
            TextNode("An image ![img](i.png) and a link ", TextType.TEXT),
            TextNode("link", TextType.LINK, "l.html"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_link(nodes_with_image_and_link_text),
            expected_link_only_from_mixed,
        )

        nodes_mixed_types_link = [
            TextNode("plain text", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("[link](url)", TextType.TEXT),
        ]
        expected_mixed_types_link = [
            TextNode("plain text", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(
            split_nodes_link(nodes_mixed_types_link), expected_mixed_types_link
        )

if __name__ == "__main__":
    unittest.main()