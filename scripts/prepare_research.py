#!/usr/bin/env python3
"""Prepare a candidates file for bulk research: check slugs, register games, output batch JSON.

Usage:
    python -m scripts.prepare_research candidates.txt --batch-size 50 --batches 4

Reads a candidates file (one game per line: "Name (bgg_id)"), checks for slug
collisions, registers all games in games.yaml, and prints JSON batches to stdout
for use by the research-games skill's subagent dispatching.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

from scripts.registry import add_game


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def parse_candidates(path: str) -> list[dict]:
    games = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"^(.+) \((\d+)\)$", line)
            if m:
                name = m.group(1)
                bgg_id = int(m.group(2))
                games.append({"name": name, "bgg_id": bgg_id, "slug": slugify(name)})
    return games


def check_collisions(games: list[dict]) -> list[dict]:
    """Return deduplicated list, printing warnings for collisions."""
    seen: dict[str, str] = {}
    clean = []
    for g in games:
        if g["slug"] in seen:
            print(f"  COLLISION: \"{g['name']}\" and \"{seen[g['slug']]}\" -> {g['slug']}, skipping", file=sys.stderr)
        else:
            seen[g["slug"]] = g["name"]
            clean.append(g)
    return clean


def register_games(games: list[dict], registry: str) -> tuple[int, int]:
    added = skipped = 0
    for g in games:
        try:
            existing = add_game(registry, name=g["name"], bgg_id=g["bgg_id"], status="queued")
            if existing.get("status") != "queued":
                skipped += 1
            else:
                added += 1
        except Exception:
            skipped += 1
    return added, skipped


def main():
    parser = argparse.ArgumentParser(description="Prepare candidates for bulk research")
    parser.add_argument("candidates", help="Path to candidates file")
    parser.add_argument("--batch-size", type=int, default=50, help="Games per batch (default: 50)")
    parser.add_argument("--batches", type=int, default=4, help="Number of batches (default: 4)")
    parser.add_argument("--registry", default="games.yaml", help="Path to games.yaml")
    args = parser.parse_args()

    # Parse
    games = parse_candidates(args.candidates)
    print(f"Parsed {len(games)} candidates", file=sys.stderr)

    # Check collisions
    games = check_collisions(games)

    # Register
    added, skipped = register_games(games, args.registry)
    print(f"Registered: {added}, Skipped: {skipped}", file=sys.stderr)

    # Split into batches and output JSON
    batch_size = args.batch_size
    num_batches = args.batches
    actual_batches = []
    for i in range(num_batches):
        batch = games[i * batch_size : (i + 1) * batch_size]
        if batch:
            actual_batches.append(batch)

    remainder = games[num_batches * batch_size :]
    if remainder:
        print(f"  Warning: {len(remainder)} games don't fit in {num_batches} batches of {batch_size}", file=sys.stderr)

    # Output JSON to stdout (one batch per line, prefixed)
    for i, batch in enumerate(actual_batches):
        print(f"BATCH {i + 1}/{len(actual_batches)} ({len(batch)} games):", file=sys.stderr)
        print(f"BATCH{i + 1}:{json.dumps(batch)}")

    print(f"\n{len(actual_batches)} batches ready for dispatch", file=sys.stderr)


if __name__ == "__main__":
    main()
