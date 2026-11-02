"""Regenerate the golden JSON fixtures from their Markdown sources."""

import json
from pathlib import Path

import mistune

from mistune_json import JsonRenderer

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "markdown"


def main() -> None:
    """Render every fixture source and rewrite its expected JSON."""
    markdown = mistune.create_markdown(renderer=JsonRenderer())

    for source in sorted(FIXTURE_DIR.glob("*.md")):
        output = markdown(source.read_text(encoding="utf-8"))
        target = source.with_suffix(".json")
        target.write_text(
            json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"updated {target.relative_to(FIXTURE_DIR.parent.parent)}")


if __name__ == "__main__":
    main()
