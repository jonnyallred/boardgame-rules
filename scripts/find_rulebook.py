#!/usr/bin/env python3
"""Find and download boardgame rulebook PDFs from BoardGameGeek.

Usage:
    python -m scripts.find_rulebook "Catan"
    python -m scripts.find_rulebook "Catan" --select 4
    python -m scripts.find_rulebook "Catan" --bgg-id 13
"""

import argparse
import os
import re
import sys

import requests
from dotenv import load_dotenv

from scripts.bgg import search_game, get_game_details
from scripts.bgg_files import files_page_url, fetch_files_page, parse_files_page, find_rulebook_files
from scripts.registry import add_game, update_status, find_game

load_dotenv()

PDF_DIR = "source_pdfs"


def slugify(name: str) -> str:
    """Convert game name to filesystem-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def download_pdf(url: str, dest: str) -> bool:
    """Download a file to dest path. Returns True on success."""
    try:
        resp = requests.get(url, stream=True, allow_redirects=True)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"  Download failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Find and download boardgame rulebook PDFs from BGG")
    parser.add_argument("game_name", help="Name of the boardgame to search for")
    parser.add_argument("--select", type=int, default=None, help="Auto-select search result by index")
    parser.add_argument("--bgg-id", type=int, default=None, help="Skip search, use this BGG ID directly")
    parser.add_argument("--registry", default="games.yaml", help="Path to games.yaml registry")
    parser.add_argument("--pdf-dir", default=PDF_DIR, help="Directory to save PDFs")
    args = parser.parse_args()

    token = os.environ.get("BGG_API_TOKEN")
    if not token:
        print("Error: BGG_API_TOKEN not set. Add it to .env or set as environment variable.")
        print("Register at https://boardgamegeek.com/applications")
        sys.exit(1)

    # Check if already in registry
    existing = find_game(args.registry, args.game_name)
    if existing and existing.get("status") != "pending":
        print(f"'{args.game_name}' already in registry with status: {existing['status']}")
        return

    # Get BGG ID — either directly, from search, or interactively
    if args.bgg_id:
        bgg_id = args.bgg_id
        print(f"Using BGG ID {bgg_id} directly...")
    else:
        print(f"Searching BGG for '{args.game_name}'...")
        results = search_game(args.game_name, token=token)

        if not results:
            print("No results found.")
            sys.exit(1)

        print(f"\nFound {len(results)} results:")
        for i, r in enumerate(results[:10]):
            year = f" ({r['year']})" if r.get("year") else ""
            print(f"  [{i}] {r['name']}{year} (BGG ID: {r['id']})")

        if args.select is not None:
            choice = args.select
        elif len(results) == 1:
            choice = 0
        else:
            try:
                choice = int(input("\nSelect game number [0]: ") or "0")
            except (ValueError, EOFError):
                choice = 0

        bgg_id = results[choice]["id"]
        print(f"\nSelected: {results[choice]['name']} (BGG ID: {bgg_id})")

    print(f"Fetching details...")
    details = get_game_details(bgg_id, token=token)

    # Add to registry
    add_game(
        args.registry,
        name=details["name"],
        bgg_id=details["bgg_id"],
        player_count=details.get("player_count"),
        play_time=details.get("play_time"),
        designer=details.get("designer"),
    )
    print(f"Added to registry: {details['name']}")

    # Find rulebook files
    print(f"\nChecking files page...")
    files_url = files_page_url(details["bgg_id"])
    print(f"  Files page: {files_url}")

    try:
        html = fetch_files_page(details["bgg_id"])
        files = parse_files_page(html)
        rulebooks = find_rulebook_files(files)
    except Exception as e:
        print(f"  Could not scrape files page: {e}")
        print(f"  Open manually: {files_url}")
        rulebooks = []

    if rulebooks:
        print(f"\nFound {len(rulebooks)} rulebook file(s):")
        for i, rb in enumerate(rulebooks):
            print(f"  [{i}] {rb['title']} ({rb['category']})")

        try:
            rb_choice = int(input("\nSelect rulebook to download [0]: ") or "0")
        except (ValueError, EOFError):
            rb_choice = 0

        selected_rb = rulebooks[rb_choice]
        if selected_rb.get("download_url"):
            slug = slugify(details["name"])
            dest = os.path.join(args.pdf_dir, f"{slug}-rules.pdf")
            os.makedirs(args.pdf_dir, exist_ok=True)
            print(f"\nDownloading to {dest}...")
            if download_pdf(selected_rb["download_url"], dest):
                update_status(args.registry, details["name"], "downloaded")
                print(f"Success! PDF saved to {dest}")
            else:
                print("Download failed. Try manually from the files page.")
        else:
            print(f"  No direct download link. Visit: {selected_rb.get('filepage_url', files_url)}")
    else:
        print(f"\nNo rulebook files found automatically.")
        print(f"Visit the files page to find and download manually: {files_url}")
        print(f"Then place the PDF in {args.pdf_dir}/")


if __name__ == "__main__":
    main()
