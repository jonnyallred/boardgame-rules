#!/usr/bin/env python3
"""Download rulebook PDFs for games in the registry.

Usage:
    python -m scripts.download_pdf
    python -m scripts.download_pdf --game "Catan"
    python -m scripts.download_pdf --limit 5
"""

import argparse
import os
import re

import requests

from scripts.registry import get_games_by_status, update_status

MIN_PDF_SIZE = 10_000  # 10 KB minimum for a valid PDF


def slugify(name: str) -> str:
    """Convert game name to filesystem-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def verify_pdf(path: str) -> bool:
    """Check that a file exists, is at least MIN_PDF_SIZE bytes, and starts with PDF magic bytes."""
    try:
        size = os.path.getsize(path)
        if size < MIN_PDF_SIZE:
            return False
        with open(path, "rb") as f:
            magic = f.read(5)
        return magic == b"%PDF-"
    except OSError:
        return False


def download_pdf(url: str, dest: str) -> bool:
    """Download a file from url to dest path. Returns True on success, False on exception."""
    try:
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        resp = requests.get(url, stream=True, allow_redirects=True, timeout=60)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"  Download failed: {e}")
        return False


def download_batch(registry_path: str, pdf_dir: str = "source_pdfs", limit: int = 0) -> dict:
    """Download PDFs for all games with status 'found'.

    Returns a stats dict with keys: attempted, downloaded, failed, skipped.
    """
    games = get_games_by_status(registry_path, "found", limit=limit)
    stats = {"attempted": 0, "downloaded": 0, "failed": 0, "skipped": 0}

    for game in games:
        name = game["name"]
        pdf_url = game.get("pdf_url")

        if not pdf_url:
            print(f"  Skipping {name}: no pdf_url")
            stats["skipped"] += 1
            continue

        slug = slugify(name)
        dest = os.path.join(pdf_dir, f"{slug}-rules.pdf")
        stats["attempted"] += 1

        print(f"  Downloading {name} from {pdf_url}...")
        if download_pdf(pdf_url, dest):
            if verify_pdf(dest):
                update_status(registry_path, name, "downloaded")
                stats["downloaded"] += 1
                print(f"  OK: {dest}")
            else:
                print(f"  Invalid PDF (too small or wrong format), removing: {dest}")
                try:
                    os.remove(dest)
                except OSError:
                    pass
                stats["failed"] += 1
        else:
            stats["failed"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(description="Download rulebook PDFs for games in the registry")
    parser.add_argument("--registry", default="games.yaml", help="Path to games.yaml registry")
    parser.add_argument("--pdf-dir", default="source_pdfs", help="Directory to save PDFs")
    parser.add_argument("--limit", type=int, default=0, help="Max number of games to download (0 = all)")
    parser.add_argument("--game", type=str, default=None, help="Download a single game by name")
    args = parser.parse_args()

    if args.game:
        from scripts.registry import find_game
        game = find_game(args.registry, args.game)
        if not game:
            print(f"Game '{args.game}' not found in registry.")
            return
        pdf_url = game.get("pdf_url")
        if not pdf_url:
            print(f"Game '{args.game}' has no pdf_url.")
            return
        slug = slugify(game["name"])
        dest = os.path.join(args.pdf_dir, f"{slug}-rules.pdf")
        print(f"Downloading {game['name']} from {pdf_url}...")
        if download_pdf(pdf_url, dest) and verify_pdf(dest):
            update_status(args.registry, game["name"], "downloaded")
            print(f"OK: {dest}")
        else:
            print("Download failed or invalid PDF.")
            try:
                os.remove(dest)
            except OSError:
                pass
    else:
        print(f"Downloading PDFs for games with status 'found'...")
        stats = download_batch(args.registry, pdf_dir=args.pdf_dir, limit=args.limit)
        print(f"\nDone: {stats['downloaded']} downloaded, {stats['failed']} failed, {stats['skipped']} skipped")


if __name__ == "__main__":
    main()
