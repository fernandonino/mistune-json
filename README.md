# Mistune JSON

A JSON renderer for the [Mistune](https://github.com/lepture/mistune) Markdown parser.

## Supported HTML elements

So far, the HTML elements supported by this renderer are limited to:

* Paragraph, `<p>`
* Image, `<img>`
* Ordered lists, `<ol>`
* Unordered lists, `<ul>`
* All heading elements, `<h1>` through `<h6>`
* Links, `<a>`
* Emphasis, `<em>`
* Strong, `<strong>`
* Blockquote, `<blockquote>`
* Line break, `<br>`
* Thematic break, `<hr>`
* Both inline and block code
* Generic directives (as `directive` nodes; parsing is a plugin's job)

## How to use the JSON renderer

### Installation

The package is published in PyPI, so it can be installed through `pip` (as any other package):

```shell
pip install mistune-json
```

### Usage

```python
import mistune
from mistune_json import JsonRenderer

# Create a renderer instance
renderer = JsonRenderer()

# Create a Markdown parser with the JSON renderer
markdown = mistune.create_markdown(renderer=renderer)

# Parse Markdown text
result = markdown("# Hello, world!")

print(result)
# {'content': [{'type': 'h', 'content': [{'type': 'text', 'content': 'Hello, world!'}], 'level': 1}]}
```

## Output Schema

The JSON output is a dictionary with a `content` key containing a list of nodes. Each node has a `type` field identifying its kind.

### Node Types

| Type | Description | Fields |
|------|-------------|--------|
| `text` | Plain text | `content` (str) |
| `p` | Paragraph | `content` (Node[]) |
| `h` | Heading (h1-h6) | `content` (Node[]), `level` (int 1-6) |
| `code` | Code block (fenced) | `content` (str), `lang` (str, optional) |
| `codespan` | Inline code | `content` (str) |
| `blockquote` | Block quote | `content` (Node[]) |
| `ol` | Ordered list | `content` (Node[], of `item`), `start` (int, optional) |
| `ul` | Unordered list | `content` (Node[], of `item`) |
| `item` | List item | `content` (Node[]) |
| `a` | Link | `content` (Node[]), `href` (str), `title` (str, optional) |
| `img` | Image | `src` (str), `alt` (Node[]), `title` (str, optional) |
| `em` | Emphasis (italic) | `content` (Node[]) |
| `strong` | Strong (bold) | `content` (Node[]) |
| `directive` | Generic directive | `name` (str), `attrs` (object), `content` (Node[]) |
| `hr` | Thematic break (horizontal rule) | - |
| `br` | Line break | - |

`content` is a string only for text-bearing nodes (`text`, `code`, `codespan`); everywhere else it is
a list of child nodes. Two rules hold at every depth:

- **Blank lines produce no node.** Consecutive blank lines collapse.
- **A renderer method that returns a list is spliced into its parent.** This is what makes
  `block_text` (the paragraph Mistune uses inside a tight list) transparent, so list items get a flat
  `content` array rather than `[[...]]`.

A few field rules follow from the renderer itself:

- `code.content` is stripped of leading and trailing whitespace.
- `ol.start` is present only when the list does not start at 1.
- `a.title` and `img.title` are omitted when the Markdown has no title.
- A soft line break becomes a `text` node containing `"\n"`; it never surfaces as a bare string.

Key order is not part of the contract; compare parsed JSON, not bytes. The
[golden fixtures](tests/fixtures/markdown) are the executable version of this table.

### Example

Input:

```markdown
# Title

This is a paragraph with **bold** and *italic* text.

![alt text](image.png)

- Item 1
- Item 2
```

Output:

```json
{
  "content": [
    {"type": "h", "content": [{"type": "text", "content": "Title"}], "level": 1},
    {"type": "p", "content": [
      {"type": "text", "content": "This is a paragraph with "},
      {"type": "strong", "content": [{"type": "text", "content": "bold"}]},
      {"type": "text", "content": " and "},
      {"type": "em", "content": [{"type": "text", "content": "italic"}]},
      {"type": "text", "content": " text."}
    ]},
    {"type": "p", "content": [
      {"type": "img", "src": "image.png", "alt": [
        {"type": "text", "content": "alt text"}
      ]}
    ]},
    {"type": "ul", "content": [
      {"type": "item", "content": [{"type": "text", "content": "Item 1"}]},
      {"type": "item", "content": [{"type": "text", "content": "Item 2"}]}
    ]}
  ]
}
```

### Directives

A `directive` node is produced by a **parser plugin**, not by this package. The renderer only renames
the token's `children` to `content` and copies `options` into `attrs`:

```python
{"type": "directive", "name": "callout", "attrs": {"tone": "warm"}, "content": [...]}
```

A plugin must emit a token of this shape. `children` is always present, even when empty, and `name`
and the options ride inside `attrs` because Mistune's `render_token` forwards nothing else:

```python
{
    "type": "directive",
    "attrs": {"name": "callout", "options": {"tone": "warm"}},
    "children": [],
}
```

`JsonRenderer.NAME` is `"json"`, so Mistune's HTML-only directive plugins (admonition, figure,
include, toc) decline to register themselves against it.

## Limitations

The following elements are not yet supported:

* Tables (headers and rows)
* Definition lists
* Task lists
* Raw HTML (block or inline). Mistune still tokenizes it, so inline HTML can appear as a plain
  string inside a node array. That is outside the `content` invariant described above; validate
  documents before persisting them if your input may contain raw HTML.

## Extensibility

You can subclass `JsonRenderer` to customize the JSON output by overriding two hooks:

### `create_node(node_type, data)`

Called for every node before it's returned. Override to add custom fields to nodes.

```python
from mistune_json import JsonRenderer


class CustomRenderer(JsonRenderer):
    def create_node(self, node_type, data):
        node = super().create_node(node_type, data)
        node["source"] = "mistune-json"  # Add source to all nodes
        return node
```

### `finalize_output(output)`

Called after all content is rendered. Override to transform the final output.

```python
from mistune_json import JsonRenderer


class CustomRenderer(JsonRenderer):
    def finalize_output(self, output):
        output["meta"] = {"generated_by": "my-app"}
        return output
```

### Full Example

```python
import mistune
from mistune_json import JsonRenderer
from datetime import datetime


class CustomRenderer(JsonRenderer):
    def create_node(self, node_type, data):
        node = super().create_node(node_type, data)
        node["rendered_at"] = datetime.now().isoformat()
        return node

    def finalize_output(self, output):
        output["meta"] = {"version": "1.0"}
        return output


renderer = CustomRenderer()
markdown = mistune.create_markdown(renderer=renderer)
result = markdown("# Hello")

# Each node now has 'rendered_at', and output has 'meta'
print(result)
```

## Golden fixtures

`tests/fixtures/markdown` holds one `.md`/`.json` pair per behavior, and
`tests/fixtures/directive-token.json` covers the renderer's half of the directive shape. Regenerate
the expected files after a deliberate output change:

```shell
uv run python tests/update_fixtures.py
```

Review the diff. An unintended node shape change shows up there, which is the point: the fixtures
are the compatibility fence for everyone consuming the package.

## Contributing and Feedback

Contributions are welcome! Feel free to open issues for:

* **Enhancements** - Request new features or supported elements
* **Bugs** - Report problems with the JSON output structure

Repository: [https://github.com/fernandonino/mistune-json](https://github.com/fernandonino/mistune-json)
