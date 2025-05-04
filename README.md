# Mistune JSON
The goal of this project is to provide a very simple JSON renderer plug-in for the [Mistune](https://mistune.lepture.com/en/latest) library.
The project is still a work in progress. Feel free to contribute with a PR including a new feature or bug fix.

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
The package is not yet published in PyPI, but once it is, it will be installed with:
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
"""
# h1 Heading
## h2 Heading
### h3 Heading
This is an unordered list:
* Item 1
* Item 2
* Item 3
This text has *strong* words. And some _emphasis as well_.
""")))
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
