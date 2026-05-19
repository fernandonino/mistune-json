from typing import Any, Dict, Iterable, List, Optional

import mistune

from .exceptions import MistuneJSONValidationError


class JsonRenderer(mistune.HTMLRenderer):
    """
    A renderer for Mistune that outputs Markdown as JSON structures
    instead of HTML.
    """

    def __init__(self, output: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the JSON renderer.

        Args:
            output: Optional dictionary to update with rendered content

        Raises:
            MistuneJSONValidationError: If output is not a dictionary
        """
        if output is not None and not isinstance(output, dict):
            raise MistuneJSONValidationError(
                f"output must be a dictionary, got {type(output).__name__}"
            )
        super().__init__(escape=False, allow_harmful_protocols=False)
        self._output: Dict[str, Any] = output if output is not None else {}

    def render_tokens(self, tokens: Iterable[Dict[str, Any]], state: Any) -> List[Dict[str, Any]]:
        """
        Render a list of tokens into JSON structures.

        Args:
            tokens: Iterable of tokens to render
            state: State object from Mistune parser

        Returns:
            List of rendered JSON structures
        """
        return list(self.iter_tokens(tokens, state))

    def iter_tokens(self, tokens: Iterable[Dict[str, Any]], state: Any) -> Iterable[Dict[str, Any]]:
        """
        Iterate through tokens and yield rendered JSON structures.

        Args:
            tokens: Iterable of tokens to render
            state: State object from Mistune parser

        Yields:
            Rendered JSON structures
        """
        for tok in tokens:
            yield self.render_token(tok, state)

    def create_node(
        self, node_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a node dictionary. Override to customize node structure.

        Args:
            node_type: The type of the node (e.g., 'p', 'h', 'code')
            data: The node data dictionary

        Returns:
            The node dictionary with type field added
        """
        data["type"] = node_type
        return data

    def finalize_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Finalize the output. Override to transform the final output.

        Args:
            output: The output dictionary

        Returns:
            The finalized output dictionary
        """
        return output

    def __call__(self, tokens: Iterable[Dict[str, Any]], state: Any) -> Dict[str, Any]:
        """
        Main entry point for rendering.

        Args:
            tokens: Iterable of tokens to render
            state: State object from Mistune parser

        Returns:
            Dictionary with rendered content
        """
        content = self.render_tokens(tokens, state)
        filtered_content = [item for item in content if item]
        self._output.update({"content": filtered_content})
        return self.finalize_output(self._output)

    # Block level tokens

    def blank_line(self) -> Dict[str, Any]:
        """Render a blank line."""
        return {}

    def paragraph(self, text: str) -> Dict[str, Any]:
        """Render a paragraph."""
        return self.create_node("p", {"content": text})

    def heading(self, text: str, level: int) -> Dict[str, Any]:
        """Render a heading."""
        return self.create_node("h", {"content": text, "level": level})

    def block_code(self, code: str, info: Optional[str] = None) -> Dict[str, Any]:
        """Render a code block."""
        result = {"content": code.strip()}
        if info:
            result["lang"] = info.strip()
        return self.create_node("code", result)

    def block_quote(self, text: str) -> Dict[str, Any]:
        """Render a block quote."""
        return self.create_node("blockquote", {"content": text})

    def list(self, text: str, ordered: bool, **attrs: int) -> Dict[str, Any]:
        """Render an ordered or unordered list."""
        node_type = "ol" if ordered else "ul"
        result = {"content": text}
        if ordered:
            start = attrs.get("start")
            if start is not None:
                result["start"] = start
        return self.create_node(node_type, result)

    def list_item(self, text: str) -> Dict[str, Any]:
        """Render a list item."""
        return self.create_node("item", {"content": text})

    def thematic_break(self) -> Dict[str, Any]:
        """Render a thematic break (horizontal rule)."""
        return self.create_node("hr", {})

    # Span level tokens

    def strong(self, text: str) -> Dict[str, Any]:
        """Render strong emphasis."""
        return self.create_node("strong", {"content": text})

    def emphasis(self, text: str) -> Dict[str, Any]:
        """Render emphasis."""
        return self.create_node("em", {"content": text})

    def codespan(self, text: str) -> Dict[str, Any]:
        """Render inline code."""
        return self.create_node("codespan", {"content": text})

    def link(self, text: str, url: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Render a link."""
        link = {"href": self.safe_url(url), "content": text}
        if title:
            link["title"] = title
        return self.create_node("a", link)

    def image(self, text: str, url: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Render an image."""
        img = {"src": self.safe_url(url), "alt": text}
        if title:
            img["title"] = title
        return self.create_node("img", img)

    def linebreak(self) -> Dict[str, Any]:
        """Render a line break."""
        return self.create_node("br", {})

    def text(self, text: str) -> Dict[str, Any]:
        """Render plain text."""
        return self.create_node("text", {"content": text})
