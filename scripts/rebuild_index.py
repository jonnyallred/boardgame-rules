#!/usr/bin/env python3
"""Rebuild index.md from all rules files.

Scans the rules/ directory, reads frontmatter from each .md file, and rebuilds
index.md with alphabetical letter sections and navigation.

Usage:
    python -m scripts.rebuild_index
    python -m scripts.rebuild_index --rules-dir rules --index index.md
"""

from __future__ import annotations

import argparse
import os
from collections import defaultdict

import yaml

HEADER_TEMPLATE = """\
---
title: Board Game Rules
layout: home
---

# Board Game Rules

AI-friendly rules summaries for board games. Use these with **Claude**, **ChatGPT**, or any AI assistant to get instant rules answers — including via voice.

## How to Use

### With Claude (voice or text)

Start a conversation with Claude and paste this prompt:

```
You are a board game rules expert. I'll ask you questions about board games.
When I mention a game, fetch its rules from:
https://jonnyallred.github.io/boardgame-rules/rules/{{slug}}/
where {{slug}} is the game name in lowercase with hyphens (e.g., "ark-nova", "blood-on-the-clocktower").

The full list of available games is at:
https://jonnyallred.github.io/boardgame-rules/

Answer conversationally. Cite specific rules when relevant.
If a game isn't available, say so and offer general advice.
```

Then just ask questions — "How does trading work in Catan?" or "What happens when you run out of cards in Arcs?"

**For voice:** Paste the prompt into a Claude conversation on the mobile app, then switch to voice mode. Claude will remember the instructions and you can ask rules questions hands-free at the table.

### With ChatGPT, Gemini, or other assistants

The same prompt works — any AI assistant that can fetch web pages will pull the rules on demand.

---

## Available Games

"""

TABLE_HEADER = """\
| Game | Players | Time | Designer |
|------|---------|------|----------|
"""


def read_rules_entries(rules_dir: str) -> list[tuple[str, str, str, str, str]]:
    """Read all rules files and return (title, slug, player_count, play_time, designer) tuples."""
    entries = []
    for fname in os.listdir(rules_dir):
        if not fname.endswith(".md"):
            continue
        slug = fname[:-3]
        path = os.path.join(rules_dir, fname)
        with open(path) as f:
            content = f.read()
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1])
        except yaml.YAMLError:
            continue
        if not fm:
            continue
        title = fm.get("title", slug)
        pc = fm.get("player_count", "")
        pt = fm.get("play_time", "")
        designer = fm.get("designer", "")
        entries.append((title, slug, str(pc), str(pt), str(designer)))
    entries.sort(key=lambda x: x[0].lower().lstrip("'\""))
    return entries


def group_by_letter(entries: list[tuple[str, str, str, str, str]]) -> dict[str, list]:
    """Group entries by first letter (digits go into '0-9')."""
    groups: dict[str, list] = defaultdict(list)
    for e in entries:
        first = e[0].lstrip("'\"")[0].upper()
        if first.isdigit():
            groups["0-9"].append(e)
        else:
            groups[first].append(e)
    return dict(groups)


def build_index(entries: list[tuple[str, str, str, str, str]]) -> str:
    """Build the complete index.md content."""
    groups = group_by_letter(entries)
    letters = sorted(groups.keys(), key=lambda x: ("0" if x == "0-9" else x))

    lines = [HEADER_TEMPLATE]

    # Letter navigation
    nav_parts = [f"[{letter}](#{letter.lower() if letter != '0-9' else '0-9'})" for letter in letters]
    lines.append(" | ".join(nav_parts) + "\n\n")

    # Each section
    for letter in letters:
        anchor = letter.lower() if letter != "0-9" else "0-9"
        lines.append(f"### {letter} {{{anchor}}}\n\n")
        lines.append(TABLE_HEADER)
        for title, slug, pc, pt, designer in groups[letter]:
            lines.append(f"| [{title}](rules/{slug}/) | {pc} | {pt} | {designer} |\n")
        lines.append("\n")

    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Rebuild index.md from rules files")
    parser.add_argument("--rules-dir", default="rules", help="Rules directory (default: rules)")
    parser.add_argument("--index", default="index.md", help="Output index file (default: index.md)")
    args = parser.parse_args()

    entries = read_rules_entries(args.rules_dir)
    content = build_index(entries)

    with open(args.index, "w") as f:
        f.write(content)

    print(f"Rebuilt {args.index}: {len(entries)} games")


if __name__ == "__main__":
    main()
