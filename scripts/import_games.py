#!/usr/bin/env python3
"""Import games from boardgame-database into the rules pipeline queue.

Reads game YAML files from a sibling boardgame-database project and creates
entries in this project's games.yaml with status "queued". Cross-references
master_list.csv to get BGG IDs.

Usage:
    python -m scripts.import_games /path/to/boardgame-database/games
    python -m scripts.import_games /path/to/boardgame-database/games --limit 100
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import yaml

from scripts.registry import load_registry, save_registry


def slugify(name: str) -> str:
    """Convert game name to filesystem-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_bgg_lookup(
    master_csv_path: str, game_type: str | None = None
) -> dict[str, int]:
    """Read master_list.csv and build a slug -> bgg_id lookup dict.

    Uses the yaml_id column if present; otherwise slugifies the name.
    Only includes rows where bgg_id is non-empty.

    Args:
        master_csv_path: Path to master_list.csv.
        game_type: If set, only include rows where the type column matches.
    """
    lookup: dict[str, int] = {}
    with open(master_csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bgg_id_str = row.get("bgg_id", "").strip()
            if not bgg_id_str:
                continue
            try:
                bgg_id = int(bgg_id_str)
            except ValueError:
                continue

            # Filter by type if requested
            if game_type is not None:
                if row.get("type", "").strip() != game_type:
                    continue

            # Use yaml_id if available, otherwise slugify the name
            yaml_id = row.get("yaml_id", "").strip()
            if yaml_id:
                slug = yaml_id
            else:
                name = row.get("name", "").strip()
                if not name:
                    continue
                slug = slugify(name)

            lookup[slug] = bgg_id
    return lookup


def _format_player_count(possible_counts: list[int] | None) -> str | None:
    """Format player count list into a range string like '1-5' or '3'."""
    if not possible_counts:
        return None
    counts = sorted(int(str(c).rstrip('+')) for c in possible_counts if str(c).rstrip('+').isdigit())
    if len(counts) == 1:
        return str(counts[0])
    return f"{counts[0]}-{counts[-1]}"


def _format_play_time(min_playtime: int | None, max_playtime: int | None) -> str | None:
    """Format play time range into a string like '30-150 min'."""
    if min_playtime is None and max_playtime is None:
        return None
    if min_playtime and max_playtime and min_playtime != max_playtime:
        return f"{min_playtime}-{max_playtime} min"
    value = max_playtime or min_playtime
    return f"{value} min"


def _format_designer(designers: list[str] | None) -> str | None:
    """Format designer list into a comma-separated string."""
    if not designers:
        return None
    return ", ".join(designers)


def import_from_database(
    games_dir: str,
    registry_path: str,
    master_csv_path: str,
    limit: int = 0,
    game_type: str | None = None,
    dry_run: bool = False,
    output_path: str = "candidates.txt",
) -> dict[str, int]:
    """Import games from boardgame-database YAML files into the registry.

    Args:
        games_dir: Path to boardgame-database/games/ directory.
        registry_path: Path to this project's games.yaml.
        master_csv_path: Path to boardgame-database/master_list.csv.
        limit: Maximum number of games to import (0 = no limit).
        game_type: If set, only import games matching this type (e.g. "boardgame").

    Returns:
        Stats dict with keys: imported, skipped, no_bgg_id, errors.
    """
    stats = {"imported": 0, "skipped": 0, "no_bgg_id": 0, "errors": 0}
    candidates: list[tuple[str, int]] = []

    # Build BGG ID lookup from CSV
    bgg_lookup = build_bgg_lookup(master_csv_path, game_type=game_type)

    # Load registry once
    games = load_registry(registry_path)
    existing_bgg_ids = {g["bgg_id"] for g in games if "bgg_id" in g}
    existing_names = {g["name"].lower() for g in games}

    # Read all game YAML files
    games_path = Path(games_dir)
    yaml_files = sorted(games_path.glob("*.yaml"))

    for yaml_file in yaml_files:
        if limit > 0 and stats["imported"] >= limit:
            break

        try:
            with open(yaml_file) as f:
                game_data = yaml.safe_load(f)
        except Exception:
            stats["errors"] += 1
            continue

        if not game_data or not game_data.get("name"):
            stats["errors"] += 1
            continue

        name = game_data["name"]
        game_id = game_data.get("id", "")

        # Look up BGG ID using the game's id (slug) first, then by slugified name
        bgg_id = bgg_lookup.get(game_id)
        if bgg_id is None:
            bgg_id = bgg_lookup.get(slugify(name))
        if bgg_id is None:
            stats["no_bgg_id"] += 1
            continue

        # Skip if already in registry
        if bgg_id in existing_bgg_ids or name.lower() in existing_names:
            stats["skipped"] += 1
            continue

        # Build registry entry
        entry: dict = {
            "name": name,
            "bgg_id": bgg_id,
            "status": "queued",
        }

        player_count = _format_player_count(game_data.get("possible_counts"))
        if player_count:
            entry["player_count"] = player_count

        play_time = _format_play_time(
            game_data.get("min_playtime"),
            game_data.get("max_playtime"),
        )
        if play_time:
            entry["play_time"] = play_time

        designer = _format_designer(game_data.get("designer"))
        if designer:
            entry["designer"] = designer

        if dry_run:
            candidates.append((name, bgg_id))
        else:
            games.append(entry)
        existing_bgg_ids.add(bgg_id)
        existing_names.add(name.lower())
        stats["imported"] += 1

    if dry_run:
        with open(output_path, "w") as f:
            for name, bgg_id in candidates:
                f.write(f"{name} ({bgg_id})\n")
    else:
        save_registry(registry_path, games)

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Import games from boardgame-database into the rules pipeline queue"
    )
    parser.add_argument(
        "games_dir",
        help="Path to boardgame-database/games/ directory",
    )
    parser.add_argument(
        "--master-csv",
        default=None,
        help="Path to master_list.csv (default: games_dir/../master_list.csv)",
    )
    parser.add_argument(
        "--registry",
        default="games.yaml",
        help="Path to games.yaml registry (default: games.yaml)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Maximum number of games to import (0 = no limit)",
    )
    parser.add_argument(
        "--type",
        default=None,
        dest="game_type",
        help="Filter by CSV type column (e.g., 'boardgame' to exclude expansions)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't register games, just output a candidates file",
    )
    parser.add_argument(
        "--output",
        default="candidates.txt",
        help="Output file for --dry-run mode (default: candidates.txt)",
    )
    args = parser.parse_args()

    # Default master CSV location: sibling to games/ dir
    master_csv = args.master_csv
    if master_csv is None:
        master_csv = str(Path(args.games_dir).parent / "master_list.csv")

    stats = import_from_database(
        args.games_dir,
        args.registry,
        master_csv,
        limit=args.limit,
        game_type=args.game_type,
        dry_run=args.dry_run,
        output_path=args.output,
    )

    if args.dry_run:
        print(f"Dry run complete:")
        print(f"  Candidates: {stats['imported']}")
        print(f"  Skipped (already in registry): {stats['skipped']}")
        print(f"  Skipped (no BGG ID): {stats['no_bgg_id']}")
        print(f"  Written to: {args.output}")
    else:
        print(f"Import complete:")
        print(f"  Imported: {stats['imported']}")
        print(f"  Skipped (already in registry): {stats['skipped']}")
        print(f"  Skipped (no BGG ID): {stats['no_bgg_id']}")
        if stats["errors"]:
            print(f"  Errors: {stats['errors']}")


if __name__ == "__main__":
    main()
