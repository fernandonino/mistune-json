import mistune


class JsonRenderer(mistune.HTMLRenderer):
    def render_tokens(self, tokens, state) -> list:
        result = []
        result.extend(self.iter_tokens(tokens, state))
        return result

    def iter_tokens(self, tokens, state):
        for tok in tokens:
            yield self.render_token(tok, state)

    def blank_line(self) -> dict:
        return dict()

    def link(self, text: str, url: str, title=None) -> dict:
        link = {"type": "a", "href": self.safe_url(url), "content": text}
        if title != None:
            link["title"] = title

        return link

    def paragraph(self, text: str) -> dict:
        return {"type": "p", "content": text}

    def heading(self, text: str, level: int) -> dict:
        return {"type": "h", "content": text, "level": level}

    def list(self, text: str, ordered: bool, **attrs) -> dict:
        if ordered:
            start = attrs.get("start")
            if start is not None:
                return {
                    "type": "ol",
                    "content": text,
                    "level": start,
                }
            else:
                return {"type": "ol", "content": text}
        else:
            return {"type": "ul", "content": text}

    def list_item(self, text: str) -> dict:
        return {
            "content": text,
        }

    def image(self, text: str, url: str, title: str = None) -> dict:
        return {
            "type": "img",
            "content": url,
            "title": title,
            "alt": text,
        }

    def emphasis(self, text) -> dict:
        return {"type": "em", "content": text}

    def block_quote(self, text: str) -> dict:
        return {"type": "blockquote", "content": text}

    def codespan(self, text: str) -> dict:
        return {"type": "codespan", "content": text}

    def strong(self, text: str) -> dict:
        return {"type": "strong", "content": text}
