#!/usr/bin/env python3
"""Quality checks for rules markdown files.

Validates content depth, extracted text size, and flags uncertainty phrases.

Usage:
    python -m scripts.quality_check rules/qe.md extracted/qe-rules.txt
    python -m scripts.quality_check --batch --registry games.yaml
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from scripts.registry import get_games_by_status, update_game, update_status
from scripts.validate import validate_rules_file

MIN_EXTRACTED_SIZE = 2000
MIN_SECTION_WORDS = 20

UNCERTAINTY_PHRASES = [
    "unclear from the text",
    "not specified in the rules",
    "the rulebook does not mention",
    "unable to determine",
    "not enough information",
]


def slugify(name: str) -> str:
    """Convert a game name to a URL-friendly slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


@dataclass
class QualityResult:
    passed: bool = True
    issues: list[str] = field(default_factory=list)

    def flag(self, issue: str):
        self.passed = False
        self.issues.append(issue)


def check_quality(rules_path: str, extracted_path: str) -> QualityResult:
    """Run quality checks on a rules file and its extracted text source.

    Returns a QualityResult with pass/fail and any flagged issues.
    """
    result = QualityResult()

    # Check 1: Run validate_rules_file — each error becomes a flag
    errors = validate_rules_file(rules_path)
    for error in errors:
        result.flag(error)

    # Check 2: Extracted text file size < MIN_EXTRACTED_SIZE bytes
    extracted_size = os.path.getsize(extracted_path)
    if extracted_size < MIN_EXTRACTED_SIZE:
        result.flag("Extracted text too small")

    # Check 3: Section content depth — flag sections with < MIN_SECTION_WORDS words
    rules_text = Path(rules_path).read_text()
    sections = re.split(r"^## ", rules_text, flags=re.MULTILINE)
    for section in sections[1:]:  # skip preamble before first ##
        lines = section.split("\n")
        section_name = lines[0].strip()
        section_body = "\n".join(lines[1:])
        word_count = len(section_body.split())
        if word_count < MIN_SECTION_WORDS:
            result.flag(f"Section too short/thin: {section_name} ({word_count} words)")

    # Check 4: Uncertainty phrases in rules text
    rules_lower = rules_text.lower()
    for phrase in UNCERTAINTY_PHRASES:
        if phrase in rules_lower:
            result.flag(f"Uncertainty phrase found: \"{phrase}\"")

    return result


def check_games(
    games: list[dict],
    registry_path: str,
    rules_dir: str = "rules",
    extracted_dir: str = "extracted",
    restore_status: str | None = None,
) -> dict:
    """Check an explicit list of games and update registry statuses."""
    stats = {"validated": 0, "flagged": 0, "errors": 0}

    for game in games:
        name = game["name"]
        slug = slugify(name)
        rules_path = os.path.join(rules_dir, f"{slug}.md")
        extracted_path = os.path.join(extracted_dir, f"{slug}-rules.txt")

        if not os.path.exists(rules_path):
            print(f"  SKIP {name}: rules file not found ({rules_path})")
            if restore_status:
                update_status(registry_path, name, restore_status)
            stats["errors"] += 1
            continue

        if not os.path.exists(extracted_path):
            print(f"  SKIP {name}: extracted file not found ({extracted_path})")
            if restore_status:
                update_status(registry_path, name, restore_status)
            stats["errors"] += 1
            continue

        try:
            result = check_quality(rules_path, extracted_path)
        except Exception as e:
            print(f"  ERROR {name}: {e}")
            if restore_status:
                update_status(registry_path, name, restore_status)
            stats["errors"] += 1
            continue

        if result.passed:
            update_status(registry_path, name, "validated")
            stats["validated"] += 1
            print(f"  PASS {name}")
        else:
            notes = "; ".join(result.issues)
            update_game(registry_path, name, status="flagged", review_notes=notes)
            stats["flagged"] += 1
            print(f"  FLAG {name}: {notes}")

    return stats


def check_batch(
    registry_path: str,
    rules_dir: str = "rules",
    extracted_dir: str = "extracted",
    limit: int = 0,
) -> dict:
    """Check all games with status 'summarized', update to 'validated' or 'flagged'.

    Returns stats dict with counts of validated, flagged, and errors.
    """
    games = get_games_by_status(registry_path, "summarized", limit=limit)
    return check_games(games, registry_path, rules_dir=rules_dir, extracted_dir=extracted_dir)


def main():
    parser = argparse.ArgumentParser(description="Quality check rules files")
    parser.add_argument("rules_file", nargs="?", help="Path to rules markdown file")
    parser.add_argument("extracted_file", nargs="?", help="Path to extracted text file")
    parser.add_argument("--batch", action="store_true", help="Check all summarized games")
    parser.add_argument("--registry", default="games.yaml", help="Path to games registry")
    parser.add_argument("--rules-dir", default="rules", help="Rules directory")
    parser.add_argument("--extracted-dir", default="extracted", help="Extracted text directory")
    parser.add_argument("--limit", type=int, default=0, help="Max summarized games to check (0 = all)")
    args = parser.parse_args()

    if args.batch:
        print("Running batch quality check...")
        stats = check_batch(
            args.registry,
            rules_dir=args.rules_dir,
            extracted_dir=args.extracted_dir,
            limit=args.limit,
        )
        print(f"\nResults: {stats['validated']} validated, {stats['flagged']} flagged, {stats['errors']} errors")
        sys.exit(1 if stats["flagged"] or stats["errors"] else 0)
    elif args.rules_file and args.extracted_file:
        result = check_quality(args.rules_file, args.extracted_file)
        if result.passed:
            print("PASSED: No quality issues found.")
        else:
            print(f"FAILED: {len(result.issues)} issue(s) found:")
            for issue in result.issues:
                print(f"  - {issue}")
            sys.exit(1)
    else:
        parser.error("Provide rules_file and extracted_file, or use --batch")


if __name__ == "__main__":
    main()
