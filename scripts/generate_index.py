"""Regenerate index.md with alphabetical sections and a jump bar.

Reads all rules/*.md frontmatter, groups games by first letter,
nests expansions under their base game, and writes a navigable index.

Usage:
    python -m scripts.generate_index              # Regenerate in place
    python -m scripts.generate_index --dry-run    # Print to stdout
"""

import argparse
import sys
from collections import OrderedDict
from pathlib import Path

import yaml


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[4:end]) or {}
    except yaml.YAMLError:
        return {}


def load_games(rules_dir: Path) -> list[dict]:
    """Load game metadata from all rules/*.md files."""
    games = []
    for path in sorted(rules_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if not fm.get("title"):
            continue
        fm["slug"] = path.stem
        games.append(fm)
    return games


def letter_key(title: str) -> str:
    """Return the grouping key for a game title."""
    first = title[0]
    if first.isdigit():
        return "#"
    return first.upper()


def group_games(games: list[dict]) -> OrderedDict:
    """Group games by letter, nesting expansions under base games."""
    # Separate base games and expansions
    base_games = []
    expansions_by_base = {}  # bgg_id -> [expansion, ...]

    for g in games:
        base_id = g.get("base_game_bgg_id")
        if base_id:
            expansions_by_base.setdefault(base_id, []).append(g)
        else:
            base_games.append(g)

    # Sort base games case-insensitively
    base_games.sort(key=lambda g: g["title"].lower())

    # Sort each expansion list
    for exps in expansions_by_base.values():
        exps.sort(key=lambda g: g["title"].lower())

    # Build bgg_id lookup for base games
    base_by_bgg_id = {g["bgg_id"]: g for g in base_games if g.get("bgg_id")}

    # Handle orphaned expansions (base game has no rules file)
    orphaned = []
    matched_base_ids = set()
    for base_id, exps in expansions_by_base.items():
        if base_id in base_by_bgg_id:
            matched_base_ids.add(base_id)
        else:
            for exp in exps:
                print(
                    f"Warning: orphaned expansion '{exp['title']}' "
                    f"(base_game_bgg_id={base_id} has no rules file)",
                    file=sys.stderr,
                )
                orphaned.append(exp)

    # Add orphans as standalone entries
    all_base = base_games + orphaned
    all_base.sort(key=lambda g: g["title"].lower())

    # Group by letter
    groups = OrderedDict()
    for g in all_base:
        key = letter_key(g["title"])
        if key not in groups:
            groups[key] = []
        groups[key].append(("base", g))
        # Add matched expansions
        bgg_id = g.get("bgg_id")
        if bgg_id and bgg_id in matched_base_ids:
            for exp in expansions_by_base.get(bgg_id, []):
                groups[key].append(("expansion", exp))

    # Sort keys: # first, then A-Z
    sorted_keys = sorted(groups.keys(), key=lambda k: ("0" if k == "#" else k))
    return OrderedDict((k, groups[k]) for k in sorted_keys)


def format_row(game: dict, is_expansion: bool = False) -> str:
    """Format a single table row."""
    title = game["title"]
    slug = game["slug"]
    prefix = "↳ " if is_expansion else ""
    player_count = game.get("player_count", "")
    play_time = game.get("play_time", "")
    designer = game.get("designer", "")
    return f"| {prefix}[{title}](rules/{slug}/) | {player_count} | {play_time} | {designer} |"


def read_preamble(index_path: Path) -> str:
    """Read everything up to and including '## Available Games' from existing index.md."""
    if not index_path.exists():
        return ""
    content = index_path.read_text(encoding="utf-8")
    marker = "## Available Games"
    idx = content.find(marker)
    if idx == -1:
        return ""
    return content[: idx + len(marker)] + "\n"


FOOTER = "\n*{{ site.time | date: \"%B %Y\" }} · {{ site.pages | where_exp: \"p\", \"p.path contains 'rules/'\" | size }} games available*\n"


def generate(rules_dir: Path, index_path: Path) -> str:
    """Generate the full index.md content."""
    preamble = read_preamble(index_path)
    if not preamble:
        raise RuntimeError(
            f"Could not find '## Available Games' marker in {index_path}"
        )

    games = load_games(rules_dir)
    groups = group_games(games)

    lines = [preamble, ""]

    # Jump bar
    bar_parts = []
    for key in groups:
        if key == "#":
            bar_parts.append("[#](#0-9)")
        else:
            bar_parts.append(f"[{key}](#{key.lower()})")
    lines.append(" | ".join(bar_parts))
    lines.append("")

    # Sections
    table_header = "| Game | Players | Time | Designer |"
    table_sep = "|------|---------|------|----------|"

    for key, entries in groups.items():
        if key == "#":
            lines.append("### 0-9 {#0-9}")
        else:
            lines.append(f"### {key}")
        lines.append("")
        lines.append(table_header)
        lines.append(table_sep)
        for kind, game in entries:
            lines.append(format_row(game, is_expansion=(kind == "expansion")))
        lines.append("")

    lines.append(FOOTER.strip())
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Regenerate index.md with alphabetical navigation")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing")
    parser.add_argument("--rules-dir", default="rules", help="Path to rules directory")
    parser.add_argument("--index", default="index.md", help="Path to index.md")
    args = parser.parse_args()

    rules_dir = Path(args.rules_dir)
    index_path = Path(args.index)

    content = generate(rules_dir, index_path)

    if args.dry_run:
        print(content)
    else:
        index_path.write_text(content, encoding="utf-8")
        # Count games for summary (both base games and expansions)
        game_count = sum(1 for line in content.splitlines() if line.startswith("| ") and "[" in line and "Game |" not in line)
        print(f"Wrote {index_path} with {game_count} game entries")


if __name__ == "__main__":
    main()
