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
The package is not yet published in PyPI, but once it is, it will be installed with:
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
# {'content': [{'type': 'h', 'content': ['type': 'text', 'content': 'Hello, world!'], 'level': 1}]}
```

## Improvements and bugs

### Tables
There is currently no support for rendering tables (headers and rows). It might be added in the future, if there is enough need for it. You can rise an issue [here](https://github.com/fernandonino/mistune-json/issues) and label it as _enhancement_.

### Integration testing
Tests for a full Markdown document will be added to assure that the JSON render works as expected.

### Bugs
If you find a problem with the JSON output structure, feel free to [report a bug](https://github.com/fernandonino/mistune-json/issues).