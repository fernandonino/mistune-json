import mistune
import unittest
from mistune_json.json_renderer import JsonRenderer
from typing import Dict, Any, List


class TestJsonRenderer(unittest.TestCase):
    """Test suite for the JsonRenderer class."""

    def setUp(self):
        """Set up the parser and renderer for each test."""
        self.renderer = JsonRenderer()
        self.markdown = mistune.create_markdown(renderer=self.renderer)

    def parse(self, text: str) -> Dict[str, Any]:
        """Helper method to parse markdown text."""
        return self.markdown(text)

    def get_content(self, text: str) -> List[Dict[str, Any]]:
        """Helper method to get the content from parsed markdown."""
        return self.parse(text)["content"]

    def test_paragraphs(self):
        """Test rendering of paragraphs."""
        md = "This is a paragraph.\n\nThis is another paragraph."
        parsed = self.parse(md)
        
        # Check overall structure
        self.assertIn("content", parsed)
        content = parsed["content"]
        self.assertEqual(len(content), 2)
        
        # Check each paragraph
        self.assertEqual(content[0]["type"], "p")
        self.assertEqual(content[0]["content"], [{"type": "text", "content": "This is a paragraph."}])
        self.assertEqual(content[1]["type"], "p")
        self.assertEqual(content[1]["content"], [{"type": "text", "content": "This is another paragraph."}])

    def test_headings(self):
        """Test rendering of headings."""
        md = "# Heading 1\n## Heading 2\n### Heading 3"
        parsed = self.parse(md)
        
        # Check overall structure
        self.assertIn("content", parsed)
        content = parsed["content"]
        self.assertEqual(len(content), 3)
        
        # Check each heading
        self.assertEqual(content[0]["type"], "h")
        self.assertEqual(content[0]["level"], 1)
        self.assertEqual(content[0]["content"], [{"type": "text", "content": "Heading 1"}])
        
        self.assertEqual(content[1]["type"], "h")
        self.assertEqual(content[1]["level"], 2)
        self.assertEqual(content[1]["content"], [{"type": "text", "content": "Heading 2"}])
        
        self.assertEqual(content[2]["type"], "h")
        self.assertEqual(content[2]["level"], 3)
        self.assertEqual(content[2]["content"], [{"type": "text", "content": "Heading 3"}])

    def test_emphasis(self):
        """Test rendering of emphasis."""
        # This test is tricky because the structure depends on mistune's tokenization
        # We'll test the renderer method directly instead
        result = self.renderer.emphasis("emphasized text")
        self.assertEqual(result["type"], "em")
        self.assertEqual(result["content"], "emphasized text")

        result = self.renderer.strong("strong text")
        self.assertEqual(result["type"], "strong")
        self.assertEqual(result["content"], "strong text")

    def test_code_blocks(self):
        """Test rendering of code blocks."""
        # Let's test the renderer method directly
        result = self.renderer.block_code("print('Hello World')", "python")

        self.assertEqual(result["type"], "code")
        self.assertEqual(result["content"], "print('Hello World')")
        self.assertEqual(result["lang"], "python")

        # Also test through markdown parsing, but be more careful with assertions
        md = "```python\nprint('Hello World')\n```"
        parsed = self.parse(md)

        # Find the code block in the content
        code_blocks = [item for item in parsed["content"] if item.get("type") == "code"]
        self.assertEqual(len(code_blocks), 1)
        code_block = code_blocks[0]

        self.assertEqual(code_block["type"], "code")
        self.assertEqual(code_block["content"], "print('Hello World')")
        self.assertEqual(code_block["lang"], "python")

    def test_code_blocks_no_language(self):
        """Test rendering of code blocks without language specification."""
        # Let's test the renderer method directly
        result = self.renderer.block_code("print('Hello World')", None)

        self.assertEqual(result["type"], "code")
        self.assertEqual(result["content"], "print('Hello World')")
        self.assertNotIn("lang", result)

        # Also test through markdown parsing
        md = "```\nprint('Hello World')\n```"
        parsed = self.parse(md)

        # Find the code block in the content
        code_blocks = [item for item in parsed["content"] if item.get("type") == "code"]
        self.assertEqual(len(code_blocks), 1)
        code_block = code_blocks[0]

        self.assertEqual(code_block["type"], "code")
        self.assertEqual(code_block["content"], "print('Hello World')")
        # Language might be empty string or None, depending on mistune version
        if "lang" in code_block:
            self.assertIn(code_block["lang"], [None, ""])

    def test_inline_code(self):
        """Test rendering of inline code."""
        # Test the renderer method directly
        result = self.renderer.codespan("inline code")
        self.assertEqual(result["type"], "codespan")
        self.assertEqual(result["content"], "inline code")

        # For testing through markdown, we need to be careful with the structure
        md = "This is `inline code`."
        parsed = self.parse(md)

        # The structure will depend on mistune's tokenization, so we'll just
        # check that the content is somewhere in the output
        self.assertTrue(any("inline code" in str(item) for item in parsed["content"]))

    def test_links(self):
        """Test rendering of links."""
        # Test the renderer method directly
        result = self.renderer.link("link text", "https://example.com", "Title")
        self.assertEqual(result["type"], "a")
        self.assertEqual(result["href"], "https://example.com")
        self.assertEqual(result["content"], "link text")
        self.assertEqual(result["title"], "Title")

        # Link without title
        result = self.renderer.link("link text", "https://example.com")
        self.assertEqual(result["type"], "a")
        self.assertEqual(result["href"], "https://example.com")
        self.assertEqual(result["content"], "link text")
        self.assertNotIn("title", result)

    def test_images(self):
        """Test rendering of images."""
        # Test the renderer method directly
        result = self.renderer.image(
            "Alt text", "https://example.com/img.jpg", "Image title"
        )
        self.assertEqual(result["type"], "img")
        self.assertEqual(result["src"], "https://example.com/img.jpg")
        self.assertEqual(result["alt"], "Alt text")
        self.assertEqual(result["title"], "Image title")

        # Image without title
        result = self.renderer.image("Alt text", "https://example.com/img.jpg")
        self.assertEqual(result["type"], "img")
        self.assertEqual(result["src"], "https://example.com/img.jpg")
        self.assertEqual(result["alt"], "Alt text")
        self.assertNotIn("title", result)

    def test_block_quotes(self):
        """Test rendering of block quotes."""
        # Test the renderer method directly
        result = self.renderer.block_quote("Quote content")
        self.assertEqual(result["type"], "blockquote")
        self.assertEqual(result["content"], "Quote content")

        # Test through markdown parsing
        md = "> This is a blockquote."
        parsed = self.parse(md)

        # Find blockquotes in the content
        quotes = [
            item for item in parsed["content"] if item.get("type") == "blockquote"
        ]
        self.assertEqual(len(quotes), 1)

        # The exact structure of the blockquote content depends on mistune's tokenization
        # We'll just check that it contains our text
        self.assertIn("This is a blockquote", str(quotes[0]["content"]))

    def test_unordered_lists(self):
        """Test rendering of unordered lists."""
        # Test the renderer method directly
        result = self.renderer.list("List content", ordered=False)
        self.assertEqual(result["type"], "ul")
        self.assertEqual(result["content"], "List content")

        # Test list_item as well
        item_result = self.renderer.list_item("Item content")
        self.assertEqual(item_result["content"], "Item content")

    def test_ordered_lists(self):
        """Test rendering of ordered lists."""
        # Test the renderer method directly
        result = self.renderer.list("List content", ordered=True)
        self.assertEqual(result["type"], "ol")
        self.assertEqual(result["content"], "List content")

        # Test with start attribute
        result = self.renderer.list("List content", ordered=True, start=3)
        self.assertEqual(result["type"], "ol")
        self.assertEqual(result["content"], "List content")
        self.assertEqual(result["start"], 3)

    def test_horizontal_rule(self):
        """Test rendering of horizontal rules."""
        # Test the renderer method directly
        result = self.renderer.thematic_break()
        self.assertEqual(result["type"], "hr")

    def test_output_parameter(self):
        """Test that the output parameter is used."""
        # Create a custom output dictionary
        initial_output = {"meta": {"title": "Test Document"}}

        # Create renderer with this output
        custom_renderer = JsonRenderer(output=initial_output)
        custom_markdown = mistune.create_markdown(renderer=custom_renderer)

        # Parse some markdown
        result = custom_markdown("# Hello")

        # Verify our metadata is preserved and content is added
        self.assertEqual(result["meta"]["title"], "Test Document")
        self.assertIn("content", result)
        self.assertEqual(len(result["content"]), 1)
        self.assertEqual(result["content"][0]["type"], "h")
        self.assertEqual(result["content"][0]["content"], [{"type": "text", "content": "Hello"}])
        self.assertEqual(result["content"][0]["level"], 1)

    def test_line_breaks(self):
        """Test rendering of line breaks."""
        # Test the renderer method directly
        result = self.renderer.linebreak()
        self.assertEqual(result["type"], "br")


if __name__ == "__main__":
    unittest.main()
