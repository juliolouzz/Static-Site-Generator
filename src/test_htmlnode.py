import unittest
from unittest.case import TestCase
from unittest.suite import TestSuite

from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestLeafNode(unittest.TestCase):
    def test_html_rendering(self):
        # Test that a LeafNode with a tag and value renders correctly as HTML
        leaf1 = LeafNode("p", "This is a paragraph of text.")
        leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(leaf2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_raw_text_rendering(self):
        # Test that a LeafNode without a tag renders its value as raw text
        leaf = LeafNode(None, "Just some text")
        self.assertEqual(leaf.to_html(), "Just some text")

    def test_raises_value_error_if_no_value(self):
        # Test that creating a LeafNode without a value raises a ValueError
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_raises_value_error_if_no_value_on_render(self):
        # Test that calling to_html on a LeafNode without a value raises a ValueError
        # This is just to test the raise Exception, athough the is redundant to me.
        leaf = LeafNode("p", "Some Value", props={"class": "test"})
        leaf.value = None
        with self.assertRaises(ValueError):
            leaf.to_html()

class TestParentNode(unittest.TestCase):
    def test_initialization(self):
        # Test that the object is initialized with the correct values
        child1 = LeafNode("p", "This is a paragraph.")
        child2 = LeafNode("a", "Click here", {"href": "https://www.google.com"})
        parent = ParentNode("div", [child1, child2], {"class": "container"})
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child1, child2])
        self.assertEqual(parent.props, {"class": "container"})
        self.assertIsNone(parent.value)

    def test_raises_value_error_if_no_tag(self):
        # Test that rendering a ParentNode without a tag raises a ValueError
        child1 = LeafNode("p", "This is a paragraph.")
        parent = ParentNode(None, [child1])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_raises_value_error_if_no_children(self):
        # Test that rendering a ParentNode without children raises a ValueError
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_raises_value_error_if_children_not_list(self):
        # Test that rendering a ParentNode with children not being a list raises a ValueError
        parent = ParentNode("div", "Not a list")
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_html_rendering(self):
        # Test that a ParentNode with children renders correctly as HTML
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "italic text")
        parent = ParentNode("p", [child1, child2, child3])
        expected_html = '<p><b>Bold text</b>Normal text<i>italic text</i></p>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_nested_parentnode_rendering(self):
        # Test that nested ParentNode objects render correctly as HTML
        inner_child1 = LeafNode("b", "Bold text")
        inner_child2 = LeafNode(None, "Normal text")
        inner_parent = ParentNode("span", [inner_child1, inner_child2])
        outer_child1 = LeafNode("i", "Italic text")
        outer_parent = ParentNode("div", [inner_parent, outer_child1])
        expected_html = '<div><span><b>Bold text</b>Normal text</span><i>Italic text</i></div>'
        self.assertEqual(outer_parent.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()
