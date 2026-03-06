#!/usr/bin/env python3
"""Batch pipeline orchestrator for the boardgame rules pipeline.

Runs pipeline stages (download, extract, summarize, quality_check) on games
that are ready for each stage based on their current status.

Usage:
    python -m scripts.process_batch --stage extract --limit 5
    python -m scripts.process_batch --stage all
    python -m scripts.process_batch --status
"""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter

from scripts.registry import load_registry, get_games_by_status, update_status
from scripts.extract_pdf import extract_text, clean_text, EXTRACTED_DIR
from scripts.download_pdf import download_batch
from scripts.summarize import summarize_game
from scripts.quality_check import check_batch

STAGE_ORDER = {
    "download": "found",
    "extract": "downloaded",
    "summarize": "extracted",
    "quality_check": "summarized",
}

ALL_STATUSES = [
    "queued",
    "searching",
    "found",
    "not_found",
    "downloaded",
    "extracted",
    "summarized",
    "validated",
    "flagged",
    "pending",
]


def slugify(name: str) -> str:
    """Convert game name to filesystem-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def get_stage_games(registry_path: str, stage: str, limit: int = 0) -> list[dict]:
    """Return games ready for the given pipeline stage.

    Each stage requires a specific input status (defined in STAGE_ORDER).
    """
    required_status = STAGE_ORDER[stage]
    return get_games_by_status(registry_path, required_status, limit=limit)


def run_download(registry_path: str, limit: int = 0) -> dict:
    """Run the download stage: download PDFs for games with status 'found'."""
    print("=== Download stage ===")
    stats = download_batch(registry_path, limit=limit)
    print(f"Download done: {stats}")
    return stats


def run_extract(registry_path: str, limit: int = 0) -> dict:
    """Run the extract stage: extract text from PDFs for games with status 'downloaded'.

    Finds PDFs at source_pdfs/{slug}-rules.pdf, extracts and cleans text,
    saves to extracted/{slug}-rules.txt, and updates status to 'extracted'.
    """
    print("=== Extract stage ===")
    games = get_stage_games(registry_path, "extract", limit=limit)
    stats = {"processed": 0, "failed": 0, "skipped": 0}

    os.makedirs(EXTRACTED_DIR, exist_ok=True)

    for game in games:
        name = game["name"]
        slug = slugify(name)
        pdf_path = os.path.join("source_pdfs", f"{slug}-rules.pdf")
        output_path = os.path.join(EXTRACTED_DIR, f"{slug}-rules.txt")

        if not os.path.exists(pdf_path):
            print(f"  Skipping {name}: PDF not found at {pdf_path}")
            stats["skipped"] += 1
            continue

        try:
            print(f"  Extracting {name}...")
            raw_text = extract_text(pdf_path)
            cleaned = clean_text(raw_text)

            with open(output_path, "w") as f:
                f.write(cleaned)
            print(f"  Saved to {output_path} ({len(cleaned)} chars)")

            update_status(registry_path, name, "extracted")
            stats["processed"] += 1
        except Exception as e:
            print(f"  Error extracting {name}: {e}")
            stats["failed"] += 1

    print(f"Extract done: {stats}")
    return stats


def run_summarize(registry_path: str, limit: int = 0) -> dict:
    """Run the summarize stage: summarize extracted text for games with status 'extracted'."""
    print("=== Summarize stage ===")
    games = get_stage_games(registry_path, "summarize", limit=limit)
    stats = {"processed": 0, "failed": 0}

    for game in games:
        success = summarize_game(game, registry_path)
        if success:
            stats["processed"] += 1
        else:
            stats["failed"] += 1

    print(f"Summarize done: {stats}")
    return stats


def run_quality_check(registry_path: str, limit: int = 0) -> dict:
    """Run the quality check stage on games with status 'summarized'."""
    print("=== Quality check stage ===")
    stats = check_batch(registry_path)
    print(f"Quality check done: {stats}")
    return stats


def show_status(registry_path: str) -> None:
    """Print a summary of game counts by status."""
    games = load_registry(registry_path)
    counts = Counter(g.get("status", "unknown") for g in games)

    print(f"Registry: {len(games)} games total\n")
    for status in ALL_STATUSES:
        count = counts.get(status, 0)
        if count > 0:
            print(f"  {status:15s} {count}")

    # Print any statuses not in ALL_STATUSES
    for status, count in sorted(counts.items()):
        if status not in ALL_STATUSES:
            print(f"  {status:15s} {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch pipeline orchestrator for boardgame rules"
    )
    parser.add_argument(
        "--stage",
        choices=["download", "extract", "summarize", "quality_check", "all"],
        help="Pipeline stage to run",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max number of games to process (0 = all)",
    )
    parser.add_argument(
        "--registry",
        default="games.yaml",
        help="Path to games.yaml registry (default: games.yaml)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status summary and exit",
    )
    args = parser.parse_args()

    if args.status:
        show_status(args.registry)
        return

    if not args.stage:
        parser.error("--stage is required unless --status is used")

    if args.stage == "all":
        run_download(args.registry, limit=args.limit)
        run_extract(args.registry, limit=args.limit)
        run_summarize(args.registry, limit=args.limit)
        run_quality_check(args.registry, limit=args.limit)
    elif args.stage == "download":
        run_download(args.registry, limit=args.limit)
    elif args.stage == "extract":
        run_extract(args.registry, limit=args.limit)
    elif args.stage == "summarize":
        run_summarize(args.registry, limit=args.limit)
    elif args.stage == "quality_check":
        run_quality_check(args.registry, limit=args.limit)


if __name__ == "__main__":
    main()
