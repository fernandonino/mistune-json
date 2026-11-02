"""Golden fixtures for the public JSON node vocabulary.

Each Markdown source in ``fixtures/markdown`` has an expected ``.json`` file
beside it. The fixtures compare parsed structure, not bytes, so key order is
irrelevant and node/array order is part of the contract.
"""

import json
from pathlib import Path
from typing import Any

import mistune
import pytest

from mistune_json import JsonRenderer

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "markdown"
DIRECTIVE_FIXTURE = Path(__file__).parent / "fixtures" / "directive-token.json"

FIXTURES = sorted(FIXTURE_DIR.glob("*.md"))

NODE_TYPES = {
    "a",
    "blockquote",
    "br",
    "code",
    "codespan",
    "directive",
    "em",
    "h",
    "hr",
    "img",
    "item",
    "ol",
    "p",
    "strong",
    "text",
    "ul",
}

STRING_CONTENT = {"code", "codespan", "text"}
LIST_CONTENT = {"a", "blockquote", "directive", "em", "h", "item", "ol", "p", "strong", "ul"}
NO_CONTENT = {"br", "hr", "img"}


def read_fixture(source: Path) -> Any:
    """Load the expected JSON for a Markdown fixture."""
    return json.loads(source.with_suffix(".json").read_text(encoding="utf-8"))


def walk(node: Any, path: str) -> None:
    """Assert that one node and its descendants stay inside the vocabulary."""
    assert isinstance(node, dict), f"{path}: expected a node object, got {type(node).__name__}"

    node_type = node.get("type")
    assert node_type in NODE_TYPES, f"{path}: unknown node type {node_type!r}"

    if node_type in LIST_CONTENT:
        content = node.get("content")
        assert isinstance(content, list), f"{path}: content must be a list"
        for index, child in enumerate(content):
            walk(child, f"{path}.content[{index}]")
    elif node_type in STRING_CONTENT:
        assert isinstance(node.get("content"), str), f"{path}: content must be a string"
    else:
        assert node_type in NO_CONTENT
        assert "content" not in node, f"{path}: {node_type} must not have content"

    if node_type == "img":
        alt = node.get("alt")
        assert isinstance(alt, list), f"{path}: alt must be a list of nodes"
        for index, child in enumerate(alt):
            walk(child, f"{path}.alt[{index}]")

    if node_type == "h":
        assert isinstance(node.get("level"), int), f"{path}: level must be an integer"

    if node_type == "directive":
        assert isinstance(node.get("name"), str), f"{path}: name must be a string"
        assert isinstance(node.get("attrs"), dict), f"{path}: attrs must be an object"


@pytest.mark.parametrize("source", FIXTURES, ids=lambda path: path.stem)
def test_golden_fixture(source: Path) -> None:
    """The renderer output matches the fixture exactly."""
    markdown = mistune.create_markdown(renderer=JsonRenderer())
    actual = markdown(source.read_text(encoding="utf-8"))

    assert actual == read_fixture(source)


def test_fixture_pairs_are_complete() -> None:
    """Every Markdown source has an expected JSON file, with no orphans."""
    sources = {path.stem for path in FIXTURE_DIR.glob("*.md")}
    expected = {path.stem for path in FIXTURE_DIR.glob("*.json")}

    assert sources == expected


@pytest.mark.parametrize("source", FIXTURES, ids=lambda path: path.stem)
def test_fixture_matches_the_vocabulary(source: Path) -> None:
    """Every fixture stays inside the documented node vocabulary."""
    document = read_fixture(source)

    assert isinstance(document, dict), f"{source.stem}: document must be an object"
    content = document.get("content")
    assert isinstance(content, list), f"{source.stem}: content must be a list"

    for index, node in enumerate(content):
        walk(node, f"{source.stem}.content[{index}]")


def test_directive_token_fixture() -> None:
    """A directive token becomes a directive node; options become attrs."""
    fixture = json.loads(DIRECTIVE_FIXTURE.read_text(encoding="utf-8"))
    node = JsonRenderer().render_token(fixture["token"], None)

    assert node == fixture["expected"]
    walk(node, "directive")
