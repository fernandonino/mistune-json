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
* Line breake, `<br>`
* Thematic breake, `<hr>`
* Both inline and block code

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
| `text` | Plain text content | `content` (str) |
| `p` | Paragraph | `content` (list of inline nodes) |
| `h` | Heading (h1-h6) | `content` (list), `level` (int 1-6) |
| `code` | Code block (fenced) | `content` (str), `lang` (str, optional) |
| `codespan` | Inline code | `content` (str) |
| `blockquote` | Block quote | `content` (list of inline nodes) |
| `ol` | Ordered list | `content` (str), `start` (int, optional) |
| `ul` | Unordered list | `content` (str) |
| `a` | Link | `content` (str), `href` (str), `title` (str, optional) |
| `img` | Image | `src` (str), `alt` (str), `title` (str, optional) |
| `em` | Emphasis (italic) | `content` (str) |
| `strong` | Strong (bold) | `content` (str) |
| `hr` | Thematic break (horizontal rule) | - |
| `br` | Line break | - |

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
      {"type": "strong", "content": "bold"},
      {"type": "text", "content": " and "},
      {"type": "em", "content": "italic"},
      {"type": "text", "content": " text."}
    ]},
    {"type": "img", "src": "image.png", "alt": "alt text"},
    {"type": "ul", "content": "..."}
  ]
}
```

## Limitations

The following elements are not yet supported:

* Tables (headers and rows)
* Definition lists
* Task lists

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

## Contributing and Feedback

Contributions are welcome! Feel free to open issues for:

* **Enhancements** - Request new features or supported elements
* **Bugs** - Report problems with the JSON output structure

Repository: [https://github.com/fernandonino/mistune-json](https://github.com/fernandonino/mistune-json)
