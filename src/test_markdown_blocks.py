import unittest

from markdown_blocks import (
  markdown_to_blocks,
  block_to_block_type,
  block_type_paragraph,
  block_type_heading,
  block_type_code,
  block_type_quote,
  block_type_olist,
  block_type_ulist,
  )

class TestMarkdownToHTML(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        # This test checks if the function correctly processes a simple markdown input with bold, italic, code, and lists.
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",  # Check if the first paragraph is correctly identified and kept intact.
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",  # Check if the second paragraph with a new line is correctly combined.
                "* This is a list\n* with items",  # Check if the list items are correctly combined into one block.
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        # This test checks if the function correctly processes markdown input with multiple newlines between paragraphs.
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",  # Check if the first paragraph is correctly identified and multiple newlines are handled.
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",  # Check if the second paragraph with a new line is correctly combined.
                "* This is a list\n* with items",  # Check if the list items are correctly combined into one block.
            ],
        )

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        # Test with various heading levels
        self.assertEqual(block_to_block_type("# Heading 1"), block_type_heading)
        self.assertEqual(block_to_block_type("## Heading 2"), block_type_heading)
        self.assertEqual(block_to_block_type("### Heading 3"), block_type_heading)

    def test_code_block(self):
        # Test with code block
        code_block = """```
def example():
    pass
```"""
        self.assertEqual(block_to_block_type(code_block), block_type_code)

    def test_quote_block(self):
        # Test with quote block
        quote_block = """> This is a quote
> continued quote"""
        self.assertEqual(block_to_block_type(quote_block), block_type_quote)

    def test_unordered_list(self):
        # Test with unordered list
        ulist_block = """* Item 1
* Item 2"""
        self.assertEqual(block_to_block_type(ulist_block), block_type_ulist)

        ulist_block_dash = """- Item 1
- Item 2"""
        self.assertEqual(block_to_block_type(ulist_block_dash), block_type_ulist)

    def test_ordered_list(self):
        # Test with ordered list
        olist_block = """1. Item 1
2. Item 2"""
        self.assertEqual(block_to_block_type(olist_block), block_type_olist)

    def test_paragraph(self):
        # Test with paragraph
        paragraph = "This is a regular paragraph."
        self.assertEqual(block_to_block_type(paragraph), block_type_paragraph)

        # Test with a block that looks like a quote but has an unquoted line
        not_a_quote = """> This is a quote
Not a quote"""
        self.assertEqual(block_to_block_type(not_a_quote), block_type_paragraph)

        # Test with a block that looks like a list but has a non-list item
        not_a_list = """* Item 1
Not an item"""
        self.assertEqual(block_to_block_type(not_a_list), block_type_paragraph)

if __name__ == "__main__":
    unittest.main()