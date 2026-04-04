#!/usr/bin/env python3
"""Summarize extracted rulebook text into structured markdown using Claude API.

Usage:
    python -m scripts.summarize extracted/qe-rules.txt --game "QE" --bgg-id 266830
    python -m scripts.summarize --batch --limit 5
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

import yaml
from dotenv import load_dotenv

from scripts.registry import (
    load_registry,
    update_status,
    get_games_by_status,
)

load_dotenv()

SYSTEM_PROMPT = (
    "You are an expert board game rules writer. Your task is to produce a structured, "
    "precise, and accurate summary of a board game's rules from extracted rulebook text. "
    "Precision is paramount: include all exact numbers, thresholds, costs, and edge cases "
    "from the original rules. Do not omit special cases or exceptions. Do not invent rules "
    "that are not in the source material. When in doubt, quote the original text. "
    "Output well-structured Markdown with YAML frontmatter exactly as specified in the prompt."
)

REQUIRED_SECTIONS = [
    "Overview",
    "Components",
    "Setup",
    "Turn Structure",
    "Actions",
    "Scoring / Victory Conditions",
    "Special Rules & Edge Cases",
    "Player Reference",
]


def slugify(name: str) -> str:
    """Convert a game name to a URL-friendly slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_prompt(
    extracted_text: str,
    game_name: str,
    bgg_id: int | None = None,
    player_count: str | None = None,
    play_time: str | None = None,
    designer: str | None = None,
) -> str:
    """Construct the user prompt for Claude to summarize a rulebook.

    Includes the extracted text in <rulebook> tags, a YAML frontmatter template,
    and the list of required section headings.
    """
    today = date.today().isoformat()

    frontmatter_lines = [
        f'title: "{game_name}"',
        f"bgg_id: {bgg_id}" if bgg_id else 'bgg_id: ""',
        f'player_count: "{player_count}"' if player_count else 'player_count: ""',
        f'play_time: "{play_time}"' if play_time else 'play_time: ""',
        f'designer: "{designer}"' if designer else 'designer: ""',
        f'source_pdf: "{slugify(game_name)}-rules.pdf"',
        f'extracted_date: "{today}"',
        f'summarized_date: "{today}"',
        'rulebook_version: ""',
    ]
    frontmatter_block = "\n".join(frontmatter_lines)

    sections_list = "\n".join(f"- {s}" for s in REQUIRED_SECTIONS)

    prompt = f"""Summarize the following board game rulebook into a structured Markdown document.

The output MUST begin with this YAML frontmatter block (fill in rulebook_version if you can determine it from the text):

---
{frontmatter_block}
---

Then write a heading `# {game_name}` followed by these required sections (each as ## headings):

{sections_list}

Precision over brevity -- keep all edge cases, exact numbers, thresholds, and scoring tables.
Include a Player Reference section with a quick-reference summary of key rules and numbers.

Here is the extracted rulebook text:

<rulebook>
{extracted_text}
</rulebook>"""

    return prompt


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from a Markdown document.

    Looks for content between --- delimiters at the start of the document.
    Returns parsed dict, or empty dict if no frontmatter found.
    """
    match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def summarize_text(
    extracted_text: str,
    game_name: str,
    **kwargs,
) -> str:
    """Call Claude API to summarize extracted rulebook text.

    Requires ANTHROPIC_API_KEY environment variable to be set.
    Returns the generated Markdown content.
    """
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Add it to your .env file or export it."
        )

    client = anthropic.Anthropic()
    user_prompt = build_prompt(extracted_text, game_name, **kwargs)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return message.content[0].text


def _find_extracted_file(slug: str, extracted_dir: str) -> str | None:
    """Find the extracted text file for a game, trying common name patterns."""
    patterns = [
        f"{slug}-rules.txt",
        f"{slug}_rules.txt",
        f"{slug}.txt",
    ]
    for pattern in patterns:
        path = os.path.join(extracted_dir, pattern)
        if os.path.exists(path):
            return path
    return None


def summarize_game(
    game: dict,
    registry_path: str,
    extracted_dir: str = "extracted",
    rules_dir: str = "rules",
    restore_status: str | None = None,
) -> bool:
    """Summarize a single game from its registry entry.

    Finds the extracted text file, calls summarize_text, saves the result
    to rules/<slug>.md, and updates the game's status to 'summarized'.

    Returns True on success, False on failure.
    """
    name = game["name"]
    slug = slugify(name)

    extracted_path = _find_extracted_file(slug, extracted_dir)
    if not extracted_path:
        print(f"  Skipping {name}: no extracted text file found in {extracted_dir}/")
        if restore_status:
            update_status(registry_path, name, restore_status)
        return False

    with open(extracted_path) as f:
        extracted_text = f.read()

    if len(extracted_text) < 500:
        print(f"  Skipping {name}: extracted text too short ({len(extracted_text)} chars)")
        if restore_status:
            update_status(registry_path, name, restore_status)
        return False

    print(f"  Summarizing {name}...")
    try:
        result = summarize_text(
            extracted_text,
            name,
            bgg_id=game.get("bgg_id"),
            player_count=game.get("player_count"),
            play_time=game.get("play_time"),
            designer=game.get("designer"),
        )
    except Exception as e:
        print(f"  Error summarizing {name}: {e}")
        if restore_status:
            update_status(registry_path, name, restore_status)
        return False

    os.makedirs(rules_dir, exist_ok=True)
    rules_path = os.path.join(rules_dir, f"{slug}.md")
    with open(rules_path, "w") as f:
        f.write(result)
    print(f"  Saved to {rules_path}")

    update_status(registry_path, name, "summarized")
    print(f"  Updated registry: {name} -> summarized")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Summarize extracted rulebook text into structured markdown using Claude API"
    )
    parser.add_argument(
        "extracted_file",
        nargs="?",
        help="Path to extracted text file",
    )
    parser.add_argument("--game", help="Game name (required for single-file mode)")
    parser.add_argument("--bgg-id", type=int, help="BoardGameGeek ID")
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all games with status 'extracted'",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max number of games to process in batch mode (0 = no limit)",
    )
    parser.add_argument(
        "--registry",
        default="games.yaml",
        help="Path to games.yaml (default: games.yaml)",
    )
    parser.add_argument(
        "--rules-dir",
        default="rules",
        help="Directory for output rules files (default: rules)",
    )
    args = parser.parse_args()

    if args.batch:
        games = get_games_by_status(args.registry, "extracted", limit=args.limit)
        if not games:
            print("No games with status 'extracted' found.")
            sys.exit(0)

        print(f"Processing {len(games)} game(s)...")
        success = 0
        for game in games:
            if summarize_game(game, args.registry, rules_dir=args.rules_dir):
                success += 1
        print(f"\nDone: {success}/{len(games)} games summarized.")
    else:
        if not args.extracted_file:
            parser.error("extracted_file is required unless --batch is used")
        if not args.game:
            parser.error("--game is required for single-file mode")

        if not os.path.exists(args.extracted_file):
            print(f"Error: file not found: {args.extracted_file}")
            sys.exit(1)

        with open(args.extracted_file) as f:
            extracted_text = f.read()

        if len(extracted_text) < 500:
            print(f"Error: extracted text too short ({len(extracted_text)} chars)")
            sys.exit(1)

        print(f"Summarizing {args.game}...")
        result = summarize_text(
            extracted_text,
            args.game,
            bgg_id=args.bgg_id,
        )

        os.makedirs(args.rules_dir, exist_ok=True)
        slug = slugify(args.game)
        rules_path = os.path.join(args.rules_dir, f"{slug}.md")
        with open(rules_path, "w") as f:
            f.write(result)
        print(f"Saved to {rules_path}")

        # Update registry if game exists
        from scripts.registry import find_game

        if find_game(args.registry, args.game):
            update_status(args.registry, args.game, "summarized")
            print(f"Updated registry: {args.game} -> summarized")


if __name__ == "__main__":
    main()
