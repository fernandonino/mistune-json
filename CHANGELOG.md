# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-05-19

### Added

- Custom exceptions: `MistuneJSONError` and `MistuneJSONValidationError`
- Extensibility hooks: `create_node()` and `finalize_output()` for subclass customization
- Documentation noting that `render_tokens()` and `iter_tokens()` are used internally by Mistune

### Changed

- All render methods now use `create_node()` for building node dictionaries

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

