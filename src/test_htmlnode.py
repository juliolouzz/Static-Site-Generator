import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        # Test that the object is initialized with the correct values
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})

    def test_initialization_defaults(self):
        # Test that the default values for tag, value, children, and props are None, None, [], and {}, respectively
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_props_to_html(self):
        # Test that the props_to_html method correctly converts the props dictionary into a string of HTML attributes
        node = HTMLNode(props={"href": "https://www.example.com", "target": "_blank"})
        expected_props_html = ' href="https://www.example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_props_html)

    def test_repr(self):
        # Test that the __repr__ method returns the expected string representation of the HTMLNode object
        node = HTMLNode(tag="a", value="Click here", children=[], props={"href": "https://www.example.com"})
        expected_repr = ("HTMLNode(tag=a, value=Click here, "
                        "children=[], props={'href': 'https://www.example.com'})")
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()
