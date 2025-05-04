# Mistune JSON
The goal of this project is to provide a very simple JSON render plug-in for the [Mistune](https://mistune.lepture.com/en/latest) library.

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
* Inline code, `<code>`
* Blockquote, `<blockquote>`

More elements are to come, especially code blocks (with `<pre><code></code></pre>`).

## How to use the JSON renderer
### Installation
This project is a work in progress. The package is not yet published in PyPI, but once it is, it will be installed with:
```shell
pip install mistune-json
```

### Usage
```python
import json
import mistune
from mistune_json import JsonRenderer
json_renderer = mistune.create_markdown(renderer=JsonRenderer())

print(json.dumps(json_render(
"""# h1 Heading
## h2 Heading
### h3 Heading
This is an unordered list:
* Item 1
* Item 2
* Item 3
This text has *strong* words. And some _emphasis as well_.
""")))
```