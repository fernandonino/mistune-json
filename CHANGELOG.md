# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.2] - 2026-11-04

### Fixed

- Soft line breaks render as `text` nodes instead of bare `"\n"` strings, which violated the
  documented node vocabulary. Covered by a new golden fixture.

## [0.3.1] - 2026-11-02

### Added

- Golden fixture suite in `tests/fixtures/` covering the public node vocabulary, plus a
  directive-token fixture. Regenerate with `uv run python tests/update_fixtures.py`.
- CI job that runs the suite against the minimum supported Mistune version.

### Changed

- README: `img.alt` is a `Node[]`, not a string, and the example shows standalone images wrapped in
  a paragraph. Documented code whitespace stripping, optional `ol.start`, omitted titles, and the
  raw-HTML limitation.

## [0.3.0] - 2026-10-20

### Changed (breaking)

- Blank lines are no longer emitted at any depth.
- List-item `content` is now a flat Node[] instead of a nested array.

### Added

- `JsonRenderer.directive()` renders generic `directive` tokens as
  `{type, name, attrs, content}`. Parsing a directive is a plugin's job; this package only defines
  the output shape.
- Project homepage to the `pyproject.toml` file.

### Changed

- `JsonRenderer.NAME` is now `"json"` instead of the inherited `"html"`, so Mistune's HTML-only
  plugins (directives, tables, footnotes, ...) decline to register against it.

## [0.2.0] - 2026-05-19

### Added

- Custom exceptions: `MistuneJSONError` and `MistuneJSONValidationError`
- Extensibility hooks: `create_node()` and `finalize_output()` for subclass customization
- Documentation noting that `render_tokens()` and `iter_tokens()` are used internally by Mistune

### Changed

- All render methods now use `create_node()` for building node dictionaries
- Optimized `__call__` to use `filter()` for removing empty items (more Pythonic)

## [0.1.0] - 2024-12-15

### Added

- Initial release of mistune-json
- JSON renderer for Mistune Markdown parser
- Support for the following HTML elements:
  - Paragraph (`<p>`)
  - Image (`<img>`)
  - Ordered lists (`<ol>`)
  - Unordered lists (`<ul>`)
  - Heading elements (`<h1>` through `<h6>`)
  - Links (`<a>`)
  - Emphasis (`<em>`)
  - Strong (`<strong>`)
  - Blockquote (`<blockquote>`)
  - Line break (`<br>`)
  - Thematic break (`<hr>`)
  - Inline and block code
- Optional `output` parameter for pre-populating output dictionary
- Unit tests for all rendered elements
