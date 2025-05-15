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

## Known bugs and improvements

### An array as the return type
The JSON render will actually return an array. Needless to say, an array is not valid JSON. There are a a few ways to solve this issue.

#### Returning a `dict`
The renderer can return a dictionary with the array in a `content` attribute. Example:
```json
{
  "content": [...]
}
```

#### Provinding an object to the renderer
TODO


#### The worst fix: no fix
The user of the renderer uses the array in a dictionary of their own to assign the array to an element of that dictionary. For example:
```python
html_page = new HtmlPage()
html_page.title = "This is the title to be shown in the browser's bar."
html_page.content = json_render("... some markdown here...")
```

### Blank lines
Blank lines are rendered as an empty dictionary, i.e. `{}`. This forces the user of the renderer to iterate over the result array to get rid of these empty elements.
