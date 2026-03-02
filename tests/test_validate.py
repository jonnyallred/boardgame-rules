import pytest
from scripts.validate import validate_rules_file

VALID_RULES = """---
title: "Catan"
bgg_id: 13
player_count: "3-4"
play_time: "60-120 min"
designer: "Klaus Teuber"
source_pdf: "catan-rules.pdf"
extracted_date: "2026-03-02"
summarized_date: "2026-03-02"
rulebook_version: "5th Edition"
---

# Catan

## Overview
Build settlements on the island of Catan.

## Components
- 19 terrain hexes
- 6 sea frame pieces

## Setup
Place the board in the center of the table.

## Turn Structure
Roll dice, collect resources, trade, build.

## Actions
Build roads, settlements, cities. Buy development cards.

## Scoring / Victory Conditions
First player to 10 victory points wins.

## Special Rules & Edge Cases
Robber activates on a 7.

## Player Reference
Road: 1 brick + 1 lumber
"""

MISSING_SECTIONS = """---
title: "Catan"
bgg_id: 13
---

# Catan

## Overview
A game.

## Setup
Set it up.
"""

NO_FRONTMATTER = """# Catan

## Overview
A game about trading.
"""


def test_validate_valid_file(tmp_path):
    path = tmp_path / "catan.md"
    path.write_text(VALID_RULES)
    errors = validate_rules_file(str(path))
    assert errors == []


def test_validate_missing_sections(tmp_path):
    path = tmp_path / "catan.md"
    path.write_text(MISSING_SECTIONS)
    errors = validate_rules_file(str(path))
    assert any("Components" in e for e in errors)
    assert any("Turn Structure" in e for e in errors)


def test_validate_no_frontmatter(tmp_path):
    path = tmp_path / "catan.md"
    path.write_text(NO_FRONTMATTER)
    errors = validate_rules_file(str(path))
    assert any("frontmatter" in e.lower() for e in errors)


def test_validate_missing_required_fields(tmp_path):
    incomplete = """---
title: "Catan"
---

# Catan

## Overview
## Components
## Setup
## Turn Structure
## Actions
## Scoring / Victory Conditions
## Special Rules & Edge Cases
## Player Reference
"""
    path = tmp_path / "catan.md"
    path.write_text(incomplete)
    errors = validate_rules_file(str(path))
    assert any("bgg_id" in e for e in errors)
