"""Validate skill markdown structure and required sections."""
from __future__ import annotations

from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
REQUIRED_SECTIONS = [
    "## Purpose",
    "## Procedure",
    "## Outputs",
    "## Quality Gate",
]


def _parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---")
    parts = text.split("---", 2)
    assert len(parts) >= 3
    lines = parts[1].strip().splitlines()
    metadata = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata, parts[2]


def test_all_skills_have_name_and_description():
    for path in SKILLS_DIR.glob("*.md"):
        metadata, body = _parse_frontmatter(path)
        assert "name" in metadata, path
        assert "description" in metadata, path
        if path.name == "main.md":
            for section in ["## Workflow", "## Output Format", "## Quality Gates", "## Rights Gate"]:
                assert section in body, f"{path} missing {section}"
        else:
            for section in REQUIRED_SECTIONS:
                assert section in body, f"{path} missing {section}"


def test_main_has_rights_gate():
    body = (SKILLS_DIR / "main.md").read_text(encoding="utf-8")
    assert "## Rights Gate" in body
    assert "Unclear" in body
