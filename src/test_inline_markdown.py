import unittest
import re

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        # Test that text with a single bolded word is correctly split into text and bold nodes
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        # Test that text with two bolded segments is correctly split into text and bold nodes
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        # Test that text with a multi-word bolded segment is correctly split into text and bold nodes
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        # Test that text with a single italicized word is correctly split into text and italic nodes
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        # Test that text with a single code block is correctly split into text and code nodes
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

class TestMarkdownExtraction(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        # Test with a string containing two markdown images
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)
        
        # Test with a string that contains no images
        text = "No images here!"
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)
        
        # Test with a string containing multiple markdown images
        text = "![image1](url1) ![image2](url2)"
        expected = [
            ("image1", "url1"),
            ("image2", "url2")
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        # Test with a string containing two markdown links
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another")
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
        
        # Test with a string that contains no links
        text = "No links here!"
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
        
        # Test with a string containing multiple markdown links
        text = "[link1](url1) [link2](url2)"
        expected = [
            ("link1", "url1"),
            ("link2", "url2")
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_image(self):
        # Test with text containing two images
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ]
        self.assertEqual(new_nodes, expected)

        # Test with text containing no images
        node = TextNode(
            "This is text with no images.",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

        # Test with text containing an image at the start
        node = TextNode(
            "![start](url1) some text",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start", text_type_image, "url1"),
            TextNode(" some text", text_type_text)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link(self):
        # Test with text containing two links
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and another ", text_type_text),
            TextNode("second link", text_type_link, "https://www.example.com/another"),
        ]
        self.assertEqual(new_nodes, expected)

        # Test with text containing no links
        node = TextNode(
            "This is text with no links.",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

        # Test with text containing a link at the start
        node = TextNode(
            "[start](url1) some text",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start", text_type_link, "url1"),
            TextNode(" some text", text_type_text)
        ]
        self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()
