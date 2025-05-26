import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node =LeafNode("h1", "Sample text")
        node2 = LeafNode("h1", "Sample text")
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = LeafNode("a", "www.youtube.com", {"href": "https://www.youtube.com"})
        node2 = LeafNode("a", "www.youtube.com", {"href": "https://www.youtube.com"})
        self.assertEqual(node, node2)
    
    def test_eq_dif(self):
        node = LeafNode("a", "www.youtube.com", {"href": "https://www.youtube.com"})
        node2 = LeafNode("h1", "Sample text")
        self.assertNotEqual(node, node2)
        

if __name__ == "__main__":
    unittest.main()

