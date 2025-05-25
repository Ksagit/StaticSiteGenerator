import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = HTMLNode("this", "should", "be", "equal")
        node2 = HTMLNode("this", "should", "be", "equal")
        self.assertEqual(node, node2)
    
    def test_eq_dif(self):
        node = HTMLNode("this", "shouldn't", "be", "equal")
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)
        
    def test_dif(self):
        node = HTMLNode("this", "shoudln't", "be", "equal")
        node2 = HTMLNode("Weee", "Wooo", "Weee", "Wooo")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

