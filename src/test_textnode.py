import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Test that two TextNode objects with the same text and text_type (and no URL) are equal
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        # Test that two TextNode objects with different text but the same text_type are not equal
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node1, node2)

    def test_neq_text_type(self):
        # Test that two TextNode objects with the same text but different text_type are not equal
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node1, node2)

    def test_neq_url(self):
        # Test that two TextNode objects with the same text and text_type but different URLs are not equal
        node1 = TextNode("This is a text node", "bold", "https://www.example.com")
        node2 = TextNode("This is a text node", "bold", "https://www.different.com")
        self.assertNotEqual(node1, node2)

    def test_eq_with_url(self):
        # Test that two TextNode objects with the same text, text_type, and URL are equal
        node1 = TextNode("This is a text node", "bold", "https://www.example.com")
        node2 = TextNode("This is a text node", "bold", "https://www.example.com")
        self.assertEqual(node1, node2)

    def test_repr(self):
        # Test that the __repr__ method returns the expected string representation
        node = TextNode("This is a text node", "bold", "https://www.example.com")
        expected_repr = "TextNode(This is a text node, bold, https://www.example.com)"
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()

