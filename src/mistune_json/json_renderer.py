from typing import Any, Dict, Iterable, List, Optional

import mistune


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
        """
        # No need for escape HTML or skip style in JSON renderer
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
        # Filter out empty items
        filtered_content = [item for item in content if item]
        self._output.update({"content": filtered_content})
        return self._output

    # Block level tokens

    def blank_line(self) -> Dict[str, Any]:
        """Render a blank line."""
        return {}

    def paragraph(self, text: str) -> Dict[str, Any]:
        """Render a paragraph."""
        return {"type": "p", "content": text}

    def heading(self, text: str, level: int) -> Dict[str, Any]:
        """Render a heading."""
        return {"type": "h", "content": text, "level": level}

    def block_code(self, code: str, info: Optional[str] = None) -> Dict[str, Any]:
        """Render a code block."""
        result = {"type": "code", "content": code.strip()}
        if info:
            result["lang"] = info.strip()
        return result

    def block_quote(self, text: str) -> Dict[str, Any]:
        """Render a block quote."""
        return {"type": "blockquote", "content": text}

    def list(self, text: str, ordered: bool, **attrs: int) -> Dict[str, Any]:
        """Render an ordered or unordered list."""
        if ordered:
            result = {"type": "ol", "content": text}
            start = attrs.get("start")
            if start is not None:
                result["start"] = start
            return result
        else:
            return {"type": "ul", "content": text}

    def list_item(self, text: str) -> Dict[str, Any]:
        """Render a list item."""
        return {"content": text}

    def thematic_break(self) -> Dict[str, Any]:
        """Render a thematic break (horizontal rule)."""
        return {"type": "hr"}

    # Span level tokens

    def strong(self, text: str) -> Dict[str, Any]:
        """Render strong emphasis."""
        return {"type": "strong", "content": text}

    def emphasis(self, text: str) -> Dict[str, Any]:
        """Render emphasis."""
        return {"type": "em", "content": text}

    def codespan(self, text: str) -> Dict[str, Any]:
        """Render inline code."""
        return {"type": "codespan", "content": text}

    def link(self, text: str, url: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Render a link."""
        link = {"type": "a", "href": self.safe_url(url), "content": text}
        if title:
            link["title"] = title
        return link

    def image(self, text: str, url: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Render an image."""
        return {
            "type": "img",
            "src": self.safe_url(url),
            "alt": text,
            **({"title": title} if title else {}),
        }

    def linebreak(self) -> Dict[str, Any]:
        """Render a line break."""
        return {"type": "br"}

    def text(self, text: str) -> Dict[str, Any]:
        """Render plain text."""
        return {"type": "text", "content": text}
