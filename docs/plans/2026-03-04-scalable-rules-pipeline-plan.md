# Scalable Rules Pipeline — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a 4-stage automated pipeline (import → find → download → extract → summarize) that processes 1000s of boardgames from the sibling boardgame-database project into structured rules summaries.

**Architecture:** Extends the existing boardgame-rules pipeline with new scripts for each stage. `games.yaml` is the central queue with expanded status tracking. PDF finding uses Claude Code + Playwright MCP tools interactively. Summarization calls the Claude API directly from Python. Quality checks auto-flag low-confidence results.

**Tech Stack:** Python 3.10+, PyYAML, requests, anthropic SDK, existing PyMuPDF/pdfplumber. Playwright via Claude Code MCP (not Python library).

---

## Task 1: Extend Registry with New Statuses and Fields

The existing `registry.py` supports 4 statuses (`pending → downloaded → extracted → summarized`). The pipeline needs more granular tracking plus new fields (`pdf_url`, `notes`, `review_notes`).

**Files:**
- Modify: `scripts/registry.py`
- Modify: `tests/test_registry.py`

**Step 1: Write failing tests for new registry capabilities**

Add to `tests/test_registry.py`:

```python
def test_add_game_with_extra_fields(registry_path):
    add_game(registry_path, name="Agricola", bgg_id=31260,
             player_count="1-5", play_time="30-150 min", designer="Uwe Rosenberg")
    reg = load_registry(registry_path)
    assert reg[0]["player_count"] == "1-5"
    assert reg[0]["designer"] == "Uwe Rosenberg"


def test_update_game_field(registry_path):
    add_game(registry_path, name="Catan", bgg_id=13)
    update_game(registry_path, "Catan", pdf_url="https://example.com/catan.pdf")
    game = find_game(registry_path, "Catan")
    assert game["pdf_url"] == "https://example.com/catan.pdf"


def test_update_game_field_preserves_existing(registry_path):
    add_game(registry_path, name="Catan", bgg_id=13, player_count="3-4")
    update_game(registry_path, "Catan", notes="Found on 1j1ju")
    game = find_game(registry_path, "Catan")
    assert game["player_count"] == "3-4"
    assert game["notes"] == "Found on 1j1ju"


def test_get_games_by_status(registry_path):
    add_game(registry_path, name="Catan", bgg_id=13)
    add_game(registry_path, name="Agricola", bgg_id=31260)
    update_status(registry_path, "Catan", "queued")
    update_status(registry_path, "Agricola", "queued")
    add_game(registry_path, name="Wingspan", bgg_id=266192)
    update_status(registry_path, "Wingspan", "found")
    result = get_games_by_status(registry_path, "queued")
    assert len(result) == 2
    assert all(g["status"] == "queued" for g in result)


def test_get_games_by_status_with_limit(registry_path):
    for i in range(10):
        add_game(registry_path, name=f"Game{i}", bgg_id=i)
        update_status(registry_path, f"Game{i}", "queued")
    result = get_games_by_status(registry_path, "queued", limit=5)
    assert len(result) == 5
```

**Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && python -m pytest tests/test_registry.py -v -k "test_update_game_field or test_get_games_by_status" 2>&1 | tail -20`

Expected: FAIL — `update_game` and `get_games_by_status` not defined.

**Step 3: Implement new registry functions**

Add to `scripts/registry.py`:

```python
def update_game(path: str, name: str, **fields) -> None:
    """Update arbitrary fields on a game entry."""
    games = load_registry(path)
    for game in games:
        if game["name"].lower() == name.lower():
            game.update(fields)
            break
    save_registry(path, games)


def get_games_by_status(path: str, status: str, limit: int = 0) -> list[dict]:
    """Get all games with a given status. Optional limit."""
    games = load_registry(path)
    matches = [g for g in games if g.get("status") == status]
    if limit > 0:
        return matches[:limit]
    return matches
```

**Step 4: Run tests to verify they pass**

Run: `source .venv/bin/activate && python -m pytest tests/test_registry.py -v`

Expected: All tests PASS.

**Step 5: Commit**

```bash
git add scripts/registry.py tests/test_registry.py
git commit -m "feat: add update_game and get_games_by_status to registry"
```

---

## Task 2: Import Games from Boardgame Database

One-time script that reads game YAML files from the sibling `boardgame-database` project and adds them to `games.yaml` with status `queued`. Each boardgame-database YAML file has fields: `id`, `name`, `year`, `designer` (list), `publisher` (list), `possible_counts` (list of ints), `playtime_minutes`, `min_playtime`, `max_playtime`.

The boardgame-database YAML files do NOT have `bgg_id` as a field — those are only in `master_list.csv`. The import script needs to cross-reference `master_list.csv` to get `bgg_id` for each game.

**Files:**
- Create: `scripts/import_games.py`
- Create: `tests/test_import_games.py`

**Step 1: Write failing tests**

Create `tests/test_import_games.py`:

```python
import pytest
import yaml
from pathlib import Path
from scripts.import_games import import_from_database, build_bgg_lookup
from scripts.registry import load_registry


@pytest.fixture
def registry_path(tmp_path):
    path = tmp_path / "games.yaml"
    path.write_text("games: []\n")
    return str(path)


@pytest.fixture
def mock_db(tmp_path):
    """Create a mock boardgame-database games/ directory."""
    games_dir = tmp_path / "games"
    games_dir.mkdir()

    game1 = {
        "id": "agricola",
        "name": "Agricola",
        "year": 2007,
        "designer": ["Uwe Rosenberg"],
        "publisher": ["Lookout Games"],
        "possible_counts": [1, 2, 3, 4, 5],
        "playtime_minutes": 120,
        "min_playtime": 30,
        "max_playtime": 150,
    }
    (games_dir / "agricola.yaml").write_text(yaml.dump(game1))

    game2 = {
        "id": "catan",
        "name": "Catan",
        "year": 1995,
        "designer": ["Klaus Teuber"],
        "publisher": ["KOSMOS"],
        "possible_counts": [3, 4],
        "playtime_minutes": 90,
        "min_playtime": 60,
        "max_playtime": 120,
    }
    (games_dir / "catan.yaml").write_text(yaml.dump(game2))

    return str(games_dir)


@pytest.fixture
def mock_master_csv(tmp_path):
    """Create a mock master_list.csv with bgg_ids."""
    csv_path = tmp_path / "master_list.csv"
    csv_path.write_text(
        "bgg_id,name,year,type,status,notes,yaml_id\n"
        "31260,Agricola,2007,boardgame,,,\n"
        "13,Catan,1995,boardgame,,,\n"
        ",Unknown Game,,boardgame,,,\n"
    )
    return str(csv_path)


def test_build_bgg_lookup(mock_master_csv):
    lookup = build_bgg_lookup(mock_master_csv)
    assert lookup["agricola"] == 31260
    assert lookup["catan"] == 13
    assert "unknown-game" not in lookup or lookup["unknown-game"] is None


def test_import_from_database(registry_path, mock_db, mock_master_csv):
    stats = import_from_database(mock_db, registry_path, mock_master_csv)
    reg = load_registry(registry_path)
    assert len(reg) == 2
    assert stats["imported"] == 2


def test_import_sets_queued_status(registry_path, mock_db, mock_master_csv):
    import_from_database(mock_db, registry_path, mock_master_csv)
    reg = load_registry(registry_path)
    assert all(g["status"] == "queued" for g in reg)


def test_import_includes_bgg_id(registry_path, mock_db, mock_master_csv):
    import_from_database(mock_db, registry_path, mock_master_csv)
    reg = load_registry(registry_path)
    agricola = next(g for g in reg if g["name"] == "Agricola")
    assert agricola["bgg_id"] == 31260


def test_import_formats_player_count(registry_path, mock_db, mock_master_csv):
    import_from_database(mock_db, registry_path, mock_master_csv)
    reg = load_registry(registry_path)
    agricola = next(g for g in reg if g["name"] == "Agricola")
    assert agricola["player_count"] == "1-5"


def test_import_formats_play_time(registry_path, mock_db, mock_master_csv):
    import_from_database(mock_db, registry_path, mock_master_csv)
    reg = load_registry(registry_path)
    agricola = next(g for g in reg if g["name"] == "Agricola")
    assert agricola["play_time"] == "30-150 min"


def test_import_skips_existing(registry_path, mock_db, mock_master_csv):
    import_from_database(mock_db, registry_path, mock_master_csv)
    stats = import_from_database(mock_db, registry_path, mock_master_csv)
    reg = load_registry(registry_path)
    assert len(reg) == 2
    assert stats["skipped"] >= 2


def test_import_with_limit(registry_path, mock_db, mock_master_csv):
    stats = import_from_database(mock_db, registry_path, mock_master_csv, limit=1)
    reg = load_registry(registry_path)
    assert len(reg) == 1
    assert stats["imported"] == 1
```

**Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && python -m pytest tests/test_import_games.py -v 2>&1 | tail -10`

Expected: FAIL — `scripts.import_games` module not found.

**Step 3: Implement import_games.py**

Create `scripts/import_games.py`:

```python
#!/usr/bin/env python3
"""Import games from boardgame-database into the rules pipeline queue.

Usage:
    python -m scripts.import_games /path/to/boardgame-database/games/
    python -m scripts.import_games /path/to/boardgame-database/games/ --limit 100
    python -m scripts.import_games /path/to/boardgame-database/games/ --master-csv /path/to/master_list.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

import yaml

from scripts.registry import load_registry, save_registry

DEFAULT_REGISTRY = "games.yaml"


def slugify(name: str) -> str:
    """Convert game name to filesystem-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_bgg_lookup(master_csv_path: str) -> dict[str, int | None]:
    """Build a slug → bgg_id lookup from master_list.csv."""
    lookup = {}
    with open(master_csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            bgg_id_str = row.get("bgg_id", "").strip()
            yaml_id = row.get("yaml_id", "").strip()
            if not name:
                continue
            slug = yaml_id if yaml_id else slugify(name)
            bgg_id = int(bgg_id_str) if bgg_id_str else None
            if bgg_id is not None:
                lookup[slug] = bgg_id
    return lookup


def import_from_database(
    games_dir: str,
    registry_path: str = DEFAULT_REGISTRY,
    master_csv_path: str | None = None,
    limit: int = 0,
) -> dict[str, int]:
    """Import games from boardgame-database YAML files into registry.

    Returns dict with counts: imported, skipped, no_bgg_id.
    """
    games_path = Path(games_dir)
    existing = load_registry(registry_path)
    existing_bgg_ids = {g["bgg_id"] for g in existing if g.get("bgg_id")}
    existing_names = {g["name"].lower() for g in existing}

    bgg_lookup = {}
    if master_csv_path:
        bgg_lookup = build_bgg_lookup(master_csv_path)

    stats = {"imported": 0, "skipped": 0, "no_bgg_id": 0}

    yaml_files = sorted(games_path.glob("*.yaml"))
    for yaml_file in yaml_files:
        if limit > 0 and stats["imported"] >= limit:
            break

        with open(yaml_file) as f:
            game_data = yaml.safe_load(f)

        if not game_data or not game_data.get("name"):
            continue

        name = game_data["name"]
        game_id = game_data.get("id", "")

        # Skip if already in registry
        if name.lower() in existing_names:
            stats["skipped"] += 1
            continue

        # Get bgg_id from lookup
        bgg_id = bgg_lookup.get(game_id)
        if bgg_id is None:
            bgg_id = bgg_lookup.get(slugify(name))

        if bgg_id is not None and bgg_id in existing_bgg_ids:
            stats["skipped"] += 1
            continue

        if bgg_id is None:
            stats["no_bgg_id"] += 1
            continue

        # Format fields
        counts = game_data.get("possible_counts", [])
        if counts:
            player_count = f"{min(counts)}-{max(counts)}" if len(counts) > 1 else str(counts[0])
        else:
            player_count = None

        min_time = game_data.get("min_playtime")
        max_time = game_data.get("max_playtime")
        if min_time and max_time and min_time != max_time:
            play_time = f"{min_time}-{max_time} min"
        elif min_time or max_time:
            play_time = f"{min_time or max_time} min"
        else:
            play_time = None

        designers = game_data.get("designer", [])
        designer_str = ", ".join(designers) if designers else None

        entry = {
            "name": name,
            "bgg_id": bgg_id,
            "status": "queued",
        }
        if player_count:
            entry["player_count"] = player_count
        if play_time:
            entry["play_time"] = play_time
        if designer_str:
            entry["designer"] = designer_str

        existing.append(entry)
        existing_bgg_ids.add(bgg_id)
        existing_names.add(name.lower())
        stats["imported"] += 1

    save_registry(registry_path, existing)
    return stats


def main():
    parser = argparse.ArgumentParser(description="Import games from boardgame-database")
    parser.add_argument("games_dir", help="Path to boardgame-database/games/ directory")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY, help="Path to games.yaml")
    parser.add_argument("--master-csv", default=None,
                        help="Path to boardgame-database/master_list.csv (for bgg_id lookup)")
    parser.add_argument("--limit", type=int, default=0, help="Max games to import (0=all)")
    args = parser.parse_args()

    if not Path(args.games_dir).is_dir():
        print(f"Error: {args.games_dir} is not a directory")
        sys.exit(1)

    print(f"Importing from {args.games_dir}...")
    stats = import_from_database(args.games_dir, args.registry, args.master_csv, args.limit)
    print(f"Done: {stats['imported']} imported, {stats['skipped']} skipped, {stats['no_bgg_id']} missing bgg_id")


if __name__ == "__main__":
    main()
```

**Step 4: Run tests to verify they pass**

Run: `source .venv/bin/activate && python -m pytest tests/test_import_games.py -v`

Expected: All tests PASS.

**Step 5: Commit**

```bash
git add scripts/import_games.py tests/test_import_games.py
git commit -m "feat: add import_games script to populate queue from boardgame-database"
```

---

## Task 3: Download PDF Script

Downloads PDFs from URLs stored in `games.yaml` (set during the Find stage). Verifies the downloaded file is actually a PDF.

**Files:**
- Create: `scripts/download_pdf.py`
- Create: `tests/test_download_pdf.py`

**Step 1: Write failing tests**

Create `tests/test_download_pdf.py`:

```python
import pytest
from unittest.mock import patch, MagicMock
from scripts.download_pdf import download_pdf, verify_pdf, download_batch
from scripts.registry import load_registry


@pytest.fixture
def registry_path(tmp_path):
    import yaml
    path = tmp_path / "games.yaml"
    data = {"games": [
        {"name": "Agricola", "bgg_id": 31260, "status": "found",
         "pdf_url": "https://example.com/agricola.pdf"},
        {"name": "Catan", "bgg_id": 13, "status": "found",
         "pdf_url": "https://example.com/catan.pdf"},
        {"name": "Wingspan", "bgg_id": 266192, "status": "queued"},
    ]}
    path.write_text(yaml.dump(data))
    return str(path)


def test_verify_pdf_valid(tmp_path):
    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"%PDF-1.4 some content here padding to make it big enough" + b"\0" * 10000)
    assert verify_pdf(str(pdf)) is True


def test_verify_pdf_too_small(tmp_path):
    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"%PDF-1.4 tiny")
    assert verify_pdf(str(pdf)) is False


def test_verify_pdf_wrong_magic(tmp_path):
    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"<html>not a pdf</html>" + b"\0" * 10000)
    assert verify_pdf(str(pdf)) is False


@patch("scripts.download_pdf.requests.get")
def test_download_pdf_success(mock_get, tmp_path):
    pdf_content = b"%PDF-1.4 " + b"\0" * 20000
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.iter_content = MagicMock(return_value=[pdf_content])
    mock_resp.raise_for_status = MagicMock()
    mock_resp.__enter__ = MagicMock(return_value=mock_resp)
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_get.return_value = mock_resp

    dest = str(tmp_path / "test.pdf")
    result = download_pdf("https://example.com/test.pdf", dest)
    assert result is True


@patch("scripts.download_pdf.requests.get")
def test_download_pdf_failure(mock_get, tmp_path):
    import requests
    mock_get.side_effect = requests.RequestException("Connection failed")
    dest = str(tmp_path / "test.pdf")
    result = download_pdf("https://example.com/test.pdf", dest)
    assert result is False
```

**Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && python -m pytest tests/test_download_pdf.py -v 2>&1 | tail -10`

Expected: FAIL — module not found.

**Step 3: Implement download_pdf.py**

Create `scripts/download_pdf.py`:

```python
#!/usr/bin/env python3
"""Download rulebook PDFs from found URLs.

Usage:
    python -m scripts.download_pdf                    # Download all with status=found
    python -m scripts.download_pdf --limit 10         # Download up to 10
    python -m scripts.download_pdf --game "Agricola"  # Download one specific game
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import requests

from scripts.registry import load_registry, get_games_by_status, update_status, update_game

PDF_DIR = "source_pdfs"
MIN_PDF_SIZE = 10_000  # 10KB minimum for a real PDF


def slugify(name: str) -> str:
    """Convert game name to filesystem-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def verify_pdf(path: str) -> bool:
    """Check that a file is a valid PDF (magic bytes + minimum size)."""
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
    """Download a file from URL to dest. Returns True on success."""
    try:
        resp = requests.get(url, stream=True, allow_redirects=True, timeout=60)
        resp.raise_for_status()
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"  Download failed: {e}")
        return False


def download_batch(registry_path: str, pdf_dir: str = PDF_DIR, limit: int = 0) -> dict[str, int]:
    """Download all games with status=found. Returns stats dict."""
    games = get_games_by_status(registry_path, "found", limit=limit)
    stats = {"downloaded": 0, "failed": 0, "invalid": 0}

    for game in games:
        url = game.get("pdf_url")
        if not url:
            print(f"  {game['name']}: No pdf_url, skipping")
            stats["failed"] += 1
            continue

        slug = slugify(game["name"])
        dest = os.path.join(pdf_dir, f"{slug}-rules.pdf")

        print(f"  Downloading {game['name']}...")
        if not download_pdf(url, dest):
            stats["failed"] += 1
            update_game(registry_path, game["name"], notes="Download failed")
            continue

        if not verify_pdf(dest):
            print(f"  {game['name']}: Downloaded file is not a valid PDF")
            os.remove(dest)
            stats["invalid"] += 1
            update_game(registry_path, game["name"], notes="Invalid PDF (wrong format or too small)")
            continue

        update_status(registry_path, game["name"], "downloaded")
        stats["downloaded"] += 1
        print(f"  {game['name']}: OK ({os.path.getsize(dest) // 1024}KB)")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Download rulebook PDFs from found URLs")
    parser.add_argument("--registry", default="games.yaml", help="Path to games.yaml")
    parser.add_argument("--pdf-dir", default=PDF_DIR, help="Directory to save PDFs")
    parser.add_argument("--limit", type=int, default=0, help="Max downloads (0=all)")
    parser.add_argument("--game", default=None, help="Download a specific game by name")
    args = parser.parse_args()

    if args.game:
        from scripts.registry import find_game
        game = find_game(args.registry, args.game)
        if not game:
            print(f"Game not found: {args.game}")
            sys.exit(1)
        if not game.get("pdf_url"):
            print(f"No pdf_url for {args.game}")
            sys.exit(1)
        slug = slugify(game["name"])
        dest = os.path.join(args.pdf_dir, f"{slug}-rules.pdf")
        if download_pdf(game["pdf_url"], dest) and verify_pdf(dest):
            update_status(args.registry, game["name"], "downloaded")
            print(f"Downloaded: {dest}")
        else:
            print("Download failed or invalid PDF")
            sys.exit(1)
    else:
        print(f"Downloading PDFs (limit={args.limit or 'all'})...")
        stats = download_batch(args.registry, args.pdf_dir, args.limit)
        print(f"Done: {stats['downloaded']} downloaded, {stats['failed']} failed, {stats['invalid']} invalid")


if __name__ == "__main__":
    main()
```

**Step 4: Run tests to verify they pass**

Run: `source .venv/bin/activate && python -m pytest tests/test_download_pdf.py -v`

Expected: All tests PASS.

**Step 5: Commit**

```bash
git add scripts/download_pdf.py tests/test_download_pdf.py
git commit -m "feat: add download_pdf script for batch PDF downloads"
```

---

## Task 4: Summarize Script (Claude API)

Calls the Anthropic API to generate structured rules markdown from extracted text. Uses the same template/format as existing rules files. Requires `ANTHROPIC_API_KEY` in `.env`.

**Files:**
- Create: `scripts/summarize.py`
- Create: `tests/test_summarize.py`
- Modify: `requirements.txt` (add `anthropic>=0.40.0`)
- Modify: `.env.example` (add `ANTHROPIC_API_KEY`)

**Step 1: Add anthropic dependency**

Add `anthropic>=0.40.0` to `requirements.txt` and run:

```bash
source .venv/bin/activate && pip install anthropic>=0.40.0
```

Add `ANTHROPIC_API_KEY=your_key_here` to `.env.example`.

**Step 2: Write failing tests**

Create `tests/test_summarize.py`:

```python
import pytest
from scripts.summarize import build_prompt, parse_frontmatter, SYSTEM_PROMPT


SAMPLE_EXTRACTED = """GAME RULES - QE
Players bid on company tiles using dry erase markers.
The highest bidder wins the company.
At the end, the player who spent the most is eliminated.
The remaining player with the most VP wins.
Setup: Deal one nation per player.
Turn: Auctioneer reveals tile, bids publicly, others bid secretly.
Scoring: Companies, nationalization, monopolization, diversification."""


def test_build_prompt_includes_extracted_text():
    prompt = build_prompt(
        extracted_text=SAMPLE_EXTRACTED,
        game_name="QE",
        bgg_id=266830,
        player_count="3-5",
        play_time="45 min",
        designer="Gavin Birnbaum",
    )
    assert "QE" in prompt
    assert "GAME RULES" in prompt
    assert "266830" in prompt


def test_build_prompt_includes_all_sections():
    prompt = build_prompt(
        extracted_text=SAMPLE_EXTRACTED,
        game_name="QE",
        bgg_id=266830,
    )
    for section in ["Overview", "Components", "Setup", "Turn Structure",
                    "Actions", "Scoring / Victory Conditions",
                    "Special Rules & Edge Cases", "Player Reference"]:
        assert section in prompt


def test_system_prompt_exists():
    assert len(SYSTEM_PROMPT) > 100
    assert "precision" in SYSTEM_PROMPT.lower() or "accurate" in SYSTEM_PROMPT.lower()


def test_parse_frontmatter():
    content = """---
title: "QE"
bgg_id: 266830
player_count: "3-5"
---

# QE

## Overview
A bidding game."""
    fm = parse_frontmatter(content)
    assert fm["title"] == "QE"
    assert fm["bgg_id"] == 266830
```

**Step 3: Run tests to verify they fail**

Run: `source .venv/bin/activate && python -m pytest tests/test_summarize.py -v 2>&1 | tail -10`

Expected: FAIL — module not found.

**Step 4: Implement summarize.py**

Create `scripts/summarize.py`:

```python
#!/usr/bin/env python3
"""Summarize extracted rulebook text into structured rules markdown using Claude API.

Usage:
    python -m scripts.summarize extracted/catan-rules.txt --game "Catan" --bgg-id 13
    python -m scripts.summarize --batch              # Summarize all extracted games
    python -m scripts.summarize --batch --limit 10   # Summarize up to 10
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
    load_registry, update_status, update_game,
    get_games_by_status, find_game,
)

load_dotenv()

RULES_DIR = "rules"
EXTRACTED_DIR = "extracted"

SYSTEM_PROMPT = """You are a board game rules expert. Your task is to produce a precise, \
comprehensive rules summary from extracted rulebook text.

Guidelines:
- Precision over brevity — keep ALL edge cases, exact numbers, thresholds, and exceptions.
- Use the exact section structure provided. Every section must have substantive content.
- Use markdown tables for structured data (costs, scoring, reference charts).
- Bold key terms on first mention.
- Number sequential steps, bullet-list options and components.
- Include parenthetical clarifications and examples where helpful.
- Do NOT invent rules not present in the source text. If something is unclear, note it.
- Write for someone learning the game — clear enough to play from this summary alone."""

EXPECTED_SECTIONS = [
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
    """Convert game name to filesystem-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_prompt(
    extracted_text: str,
    game_name: str,
    bgg_id: int | None = None,
    player_count: str | None = None,
    play_time: str | None = None,
    designer: str | None = None,
) -> str:
    """Build the user prompt for Claude API."""
    today = date.today().isoformat()

    frontmatter_lines = [
        f'title: "{game_name}"',
    ]
    if bgg_id:
        frontmatter_lines.append(f"bgg_id: {bgg_id}")
    if player_count:
        frontmatter_lines.append(f'player_count: "{player_count}"')
    if play_time:
        frontmatter_lines.append(f'play_time: "{play_time}"')
    if designer:
        frontmatter_lines.append(f'designer: "{designer}"')
    frontmatter_lines.append(f'extracted_date: "{today}"')
    frontmatter_lines.append(f'summarized_date: "{today}"')

    frontmatter = "\n".join(frontmatter_lines)

    sections = "\n".join(f"## {s}" for s in EXPECTED_SECTIONS)

    return f"""Produce a complete rules summary for the board game "{game_name}".

Use this YAML frontmatter (add source_pdf and rulebook_version if identifiable from the text):

---
{frontmatter}
---

Required sections (use these exact headings):

{sections}

Here is the extracted rulebook text:

<rulebook>
{extracted_text}
</rulebook>

Output ONLY the complete markdown file (frontmatter + all sections). No commentary."""


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def summarize_text(extracted_text: str, game_name: str, **kwargs) -> str:
    """Call Claude API to generate rules summary. Returns markdown string."""
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set in environment or .env")

    client = anthropic.Anthropic(api_key=api_key)
    prompt = build_prompt(extracted_text, game_name, **kwargs)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def summarize_game(
    game: dict,
    registry_path: str,
    extracted_dir: str = EXTRACTED_DIR,
    rules_dir: str = RULES_DIR,
) -> bool:
    """Summarize a single game. Returns True on success."""
    slug = slugify(game["name"])

    # Find extracted text file
    extracted_path = None
    for pattern in [f"{slug}-rules.txt", f"{slug}_rules.txt", f"{slug}.txt"]:
        candidate = os.path.join(extracted_dir, pattern)
        if os.path.exists(candidate):
            extracted_path = candidate
            break

    if not extracted_path:
        print(f"  {game['name']}: No extracted text found")
        update_game(registry_path, game["name"], notes="No extracted text file found")
        return False

    extracted_text = Path(extracted_path).read_text()
    if len(extracted_text) < 500:
        print(f"  {game['name']}: Extracted text too short ({len(extracted_text)} chars)")
        update_game(registry_path, game["name"], notes="Extracted text too short")
        return False

    print(f"  {game['name']}: Summarizing ({len(extracted_text)} chars)...")
    try:
        result = summarize_text(
            extracted_text,
            game_name=game["name"],
            bgg_id=game.get("bgg_id"),
            player_count=game.get("player_count"),
            play_time=game.get("play_time"),
            designer=game.get("designer"),
        )
    except Exception as e:
        print(f"  {game['name']}: API error: {e}")
        update_game(registry_path, game["name"], notes=f"Summarization failed: {e}")
        return False

    # Save rules file
    os.makedirs(rules_dir, exist_ok=True)
    output_path = os.path.join(rules_dir, f"{slug}.md")
    Path(output_path).write_text(result)
    update_status(registry_path, game["name"], "summarized")
    print(f"  {game['name']}: Saved to {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Summarize extracted rulebook text using Claude API")
    parser.add_argument("extracted_file", nargs="?", help="Path to extracted text file")
    parser.add_argument("--game", help="Game name (required with extracted_file)")
    parser.add_argument("--bgg-id", type=int, help="BGG ID")
    parser.add_argument("--batch", action="store_true", help="Summarize all extracted games")
    parser.add_argument("--limit", type=int, default=0, help="Max games to summarize (0=all)")
    parser.add_argument("--registry", default="games.yaml")
    parser.add_argument("--rules-dir", default=RULES_DIR)
    args = parser.parse_args()

    if args.batch:
        games = get_games_by_status(args.registry, "extracted", limit=args.limit)
        if not games:
            print("No games with status=extracted found.")
            return
        print(f"Summarizing {len(games)} game(s)...")
        success = sum(1 for g in games if summarize_game(g, args.registry, rules_dir=args.rules_dir))
        print(f"Done: {success}/{len(games)} summarized successfully")
    elif args.extracted_file:
        if not args.game:
            print("Error: --game is required when specifying an extracted file")
            sys.exit(1)
        text = Path(args.extracted_file).read_text()
        result = summarize_text(text, args.game, bgg_id=args.bgg_id)
        slug = slugify(args.game)
        output = os.path.join(args.rules_dir, f"{slug}.md")
        os.makedirs(args.rules_dir, exist_ok=True)
        Path(output).write_text(result)
        print(f"Saved to {output}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 5: Run tests to verify they pass**

Run: `source .venv/bin/activate && python -m pytest tests/test_summarize.py -v`

Expected: All tests PASS (tests only cover `build_prompt` and `parse_frontmatter`, not API calls).

**Step 6: Commit**

```bash
git add scripts/summarize.py tests/test_summarize.py requirements.txt .env.example
git commit -m "feat: add summarize script for Claude API rules generation"
```

---

## Task 5: Quality Check Script

Scores generated summaries and categorizes as auto-accept or flagged. Extends the existing `validate.py` checks with content-quality heuristics.

**Files:**
- Create: `scripts/quality_check.py`
- Create: `tests/test_quality_check.py`

**Step 1: Write failing tests**

Create `tests/test_quality_check.py`:

```python
import pytest
from pathlib import Path
from scripts.quality_check import check_quality, QualityResult

GOOD_RULES = """---
title: "QE"
bgg_id: 266830
player_count: "3-5"
play_time: "45 min"
designer: "Gavin Birnbaum"
extracted_date: "2026-03-04"
summarized_date: "2026-03-04"
---

# QE

## Overview
QE is a sealed-bid auction game where players represent central banks bidding
to bail out companies. The highest spender is eliminated. Among surviving
players, the one with the most victory points wins. Players can bid any amount.

## Components
- 21 Company Tiles with nation, industry, and VP value
- 5 Bid Tiles (dry erase)
- 5 Player Score Boards
- 5 Dry Erase Markers
- 1 First Auctioneer Token

## Setup
Assign nations to each player. Deal hidden industry tokens. Remove company
tiles based on player count. Shuffle remaining tiles face down.

## Turn Structure
Each turn has 5 phases: Opening Bid, Secret Bids, Award Company, Zero Bid VP,
End of Sale. The auctioneer rotates left after each turn.

## Actions
The core action is bidding. Bids must be positive whole numbers. The auctioneer
bids publicly. Other players bid secretly. No upper limit on bids.

## Scoring / Victory Conditions
Players add up spending. Highest spender eliminated. Score VP from companies,
zero bids, nationalization, monopolization, and diversification. Most VP wins.

## Special Rules & Edge Cases
Tied auctions trigger rebids up to 3 times. In 3-player games, the last tile
has no auctioneer. 5-player games allow one peek at a winning bid per game.

## Player Reference
| Category | Scoring |
|---|---|
| Elimination | Highest spender eliminated |
| Least Spent | 7 VP (3-4p) / 6 VP (5p) |
"""

SHORT_SECTION_RULES = """---
title: "QE"
bgg_id: 266830
---

# QE

## Overview
A game.

## Components
Tiles.

## Setup
Set up.

## Turn Structure
Take turns.

## Actions
Bid.

## Scoring / Victory Conditions
Score points.

## Special Rules & Edge Cases
None.

## Player Reference
See rules.
"""


def test_good_rules_pass(tmp_path):
    path = tmp_path / "qe.md"
    path.write_text(GOOD_RULES)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("QE rules text about bidding and companies and auctions " * 100)
    result = check_quality(str(path), str(extracted))
    assert result.passed is True
    assert len(result.issues) == 0


def test_short_sections_flagged(tmp_path):
    path = tmp_path / "qe.md"
    path.write_text(SHORT_SECTION_RULES)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("Some rules text " * 100)
    result = check_quality(str(path), str(extracted))
    assert result.passed is False
    assert any("thin" in issue.lower() or "short" in issue.lower() for issue in result.issues)


def test_short_extracted_text_flagged(tmp_path):
    path = tmp_path / "qe.md"
    path.write_text(GOOD_RULES)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("Very short text")
    result = check_quality(str(path), str(extracted))
    assert result.passed is False
    assert any("extracted" in issue.lower() for issue in result.issues)


def test_missing_sections_flagged(tmp_path):
    path = tmp_path / "qe.md"
    content = GOOD_RULES.replace("## Player Reference", "")
    path.write_text(content)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("Rules text " * 200)
    result = check_quality(str(path), str(extracted))
    assert result.passed is False
    assert any("Player Reference" in issue for issue in result.issues)
```

**Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && python -m pytest tests/test_quality_check.py -v 2>&1 | tail -10`

Expected: FAIL — module not found.

**Step 3: Implement quality_check.py**

Create `scripts/quality_check.py`:

```python
#!/usr/bin/env python3
"""Quality check for generated rules summaries.

Usage:
    python -m scripts.quality_check rules/qe.md extracted/qe-rules.txt
    python -m scripts.quality_check --batch          # Check all summarized games
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from scripts.validate import validate_rules_file, EXPECTED_SECTIONS
from scripts.registry import (
    load_registry, update_status, update_game,
    get_games_by_status,
)

MIN_EXTRACTED_SIZE = 2000  # 2KB minimum for source text
MIN_SECTION_WORDS = 20    # Minimum words per section
UNCERTAINTY_PHRASES = [
    "unclear from the text",
    "not specified in the rules",
    "the rulebook does not mention",
    "unable to determine",
    "not enough information",
]


@dataclass
class QualityResult:
    passed: bool = True
    issues: list[str] = field(default_factory=list)

    def flag(self, issue: str):
        self.passed = False
        self.issues.append(issue)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def check_quality(rules_path: str, extracted_path: str) -> QualityResult:
    """Run quality checks on a rules file. Returns QualityResult."""
    result = QualityResult()
    rules_text = Path(rules_path).read_text()

    # Check 1: Validation (structure + frontmatter)
    validation_errors = validate_rules_file(rules_path)
    for err in validation_errors:
        result.flag(err)

    # Check 2: Extracted text size
    if os.path.exists(extracted_path):
        extracted_size = os.path.getsize(extracted_path)
        if extracted_size < MIN_EXTRACTED_SIZE:
            result.flag(f"Extracted text too small ({extracted_size} bytes) — may be incomplete")
    else:
        result.flag(f"Extracted text file not found: {extracted_path}")

    # Check 3: Section content depth
    sections = re.split(r"^## ", rules_text, flags=re.MULTILINE)
    for section in sections[1:]:  # Skip content before first ##
        lines = section.strip().split("\n")
        section_name = lines[0].strip()
        section_body = " ".join(lines[1:]).strip()
        word_count = len(section_body.split())
        if word_count < MIN_SECTION_WORDS:
            result.flag(f"Section '{section_name}' is too short/thin ({word_count} words)")

    # Check 4: Uncertainty markers
    for phrase in UNCERTAINTY_PHRASES:
        if phrase.lower() in rules_text.lower():
            result.flag(f"Contains uncertainty: '{phrase}'")

    return result


def check_batch(
    registry_path: str,
    rules_dir: str = "rules",
    extracted_dir: str = "extracted",
) -> dict[str, int]:
    """Check all summarized games. Returns stats dict."""
    games = get_games_by_status(registry_path, "summarized")
    stats = {"validated": 0, "flagged": 0}

    for game in games:
        slug = slugify(game["name"])
        rules_path = os.path.join(rules_dir, f"{slug}.md")
        if not os.path.exists(rules_path):
            print(f"  {game['name']}: Rules file not found, skipping")
            continue

        # Find extracted text
        extracted_path = None
        for pattern in [f"{slug}-rules.txt", f"{slug}_rules.txt", f"{slug}.txt"]:
            candidate = os.path.join(extracted_dir, pattern)
            if os.path.exists(candidate):
                extracted_path = candidate
                break
        if not extracted_path:
            extracted_path = os.path.join(extracted_dir, f"{slug}-rules.txt")

        result = check_quality(rules_path, extracted_path)

        if result.passed:
            update_status(registry_path, game["name"], "validated")
            stats["validated"] += 1
            print(f"  {game['name']}: PASS")
        else:
            update_status(registry_path, game["name"], "flagged")
            update_game(registry_path, game["name"],
                        review_notes="; ".join(result.issues))
            stats["flagged"] += 1
            print(f"  {game['name']}: FLAGGED")
            for issue in result.issues:
                print(f"    - {issue}")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Quality check rules summaries")
    parser.add_argument("rules_file", nargs="?", help="Rules markdown file to check")
    parser.add_argument("extracted_file", nargs="?", help="Corresponding extracted text file")
    parser.add_argument("--batch", action="store_true", help="Check all summarized games")
    parser.add_argument("--registry", default="games.yaml")
    parser.add_argument("--rules-dir", default="rules")
    parser.add_argument("--extracted-dir", default="extracted")
    args = parser.parse_args()

    if args.batch:
        print("Running quality checks on all summarized games...")
        stats = check_batch(args.registry, args.rules_dir, args.extracted_dir)
        print(f"Done: {stats['validated']} validated, {stats['flagged']} flagged")
    elif args.rules_file and args.extracted_file:
        result = check_quality(args.rules_file, args.extracted_file)
        if result.passed:
            print("PASS — all quality checks passed")
        else:
            print("FLAGGED — issues found:")
            for issue in result.issues:
                print(f"  - {issue}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 4: Run tests to verify they pass**

Run: `source .venv/bin/activate && python -m pytest tests/test_quality_check.py -v`

Expected: All tests PASS.

**Step 5: Commit**

```bash
git add scripts/quality_check.py tests/test_quality_check.py
git commit -m "feat: add quality_check script with content scoring and flagging"
```

---

## Task 6: Batch Pipeline Orchestrator

A top-level script that runs pipeline stages for a batch of games. Each stage is independent — you can run just one stage or the full pipeline.

**Files:**
- Create: `scripts/process_batch.py`
- Create: `tests/test_process_batch.py`

**Step 1: Write failing tests**

Create `tests/test_process_batch.py`:

```python
import pytest
import yaml
from pathlib import Path
from scripts.process_batch import get_stage_games, STAGE_ORDER


@pytest.fixture
def registry_path(tmp_path):
    path = tmp_path / "games.yaml"
    data = {"games": [
        {"name": "Game1", "bgg_id": 1, "status": "found"},
        {"name": "Game2", "bgg_id": 2, "status": "downloaded"},
        {"name": "Game3", "bgg_id": 3, "status": "extracted"},
        {"name": "Game4", "bgg_id": 4, "status": "queued"},
        {"name": "Game5", "bgg_id": 5, "status": "summarized"},
    ]}
    path.write_text(yaml.dump(data))
    return str(path)


def test_stage_order():
    assert "download" in STAGE_ORDER
    assert "extract" in STAGE_ORDER
    assert "summarize" in STAGE_ORDER
    assert "quality_check" in STAGE_ORDER


def test_get_stage_games_download(registry_path):
    games = get_stage_games(registry_path, "download")
    assert len(games) == 1
    assert games[0]["name"] == "Game1"


def test_get_stage_games_extract(registry_path):
    games = get_stage_games(registry_path, "extract")
    assert len(games) == 1
    assert games[0]["name"] == "Game2"


def test_get_stage_games_summarize(registry_path):
    games = get_stage_games(registry_path, "summarize")
    assert len(games) == 1
    assert games[0]["name"] == "Game3"


def test_get_stage_games_quality_check(registry_path):
    games = get_stage_games(registry_path, "quality_check")
    assert len(games) == 1
    assert games[0]["name"] == "Game5"
```

**Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && python -m pytest tests/test_process_batch.py -v 2>&1 | tail -10`

Expected: FAIL — module not found.

**Step 3: Implement process_batch.py**

Create `scripts/process_batch.py`:

```python
#!/usr/bin/env python3
"""Batch pipeline orchestrator — run stages for N games.

Usage:
    python -m scripts.process_batch --stage download --limit 20
    python -m scripts.process_batch --stage extract --limit 20
    python -m scripts.process_batch --stage summarize --limit 10
    python -m scripts.process_batch --stage quality_check
    python -m scripts.process_batch --stage all --limit 10
    python -m scripts.process_batch --status           # Show pipeline status
"""

from __future__ import annotations

import argparse
import os
import sys

from scripts.registry import load_registry, get_games_by_status

# Maps stage name → required input status
STAGE_ORDER = {
    "download": "found",
    "extract": "downloaded",
    "summarize": "extracted",
    "quality_check": "summarized",
}


def get_stage_games(registry_path: str, stage: str, limit: int = 0) -> list[dict]:
    """Get games ready for a given stage."""
    input_status = STAGE_ORDER[stage]
    return get_games_by_status(registry_path, input_status, limit=limit)


def run_download(registry_path: str, limit: int = 0) -> dict:
    from scripts.download_pdf import download_batch
    return download_batch(registry_path, limit=limit)


def run_extract(registry_path: str, limit: int = 0) -> dict:
    """Run extraction on all downloaded games."""
    import re
    from scripts.extract_pdf import extract_text, clean_text, EXTRACTED_DIR
    from scripts.registry import update_status

    games = get_stage_games(registry_path, "extract", limit=limit)
    stats = {"extracted": 0, "failed": 0}

    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    for game in games:
        slug = re.sub(r"[^a-z0-9]+", "-", game["name"].lower()).strip("-")
        pdf_path = os.path.join("source_pdfs", f"{slug}-rules.pdf")
        if not os.path.exists(pdf_path):
            print(f"  {game['name']}: PDF not found at {pdf_path}")
            stats["failed"] += 1
            continue

        try:
            raw = extract_text(pdf_path)
            cleaned = clean_text(raw)
            output = os.path.join(EXTRACTED_DIR, f"{slug}-rules.txt")
            with open(output, "w") as f:
                f.write(cleaned)
            update_status(registry_path, game["name"], "extracted")
            stats["extracted"] += 1
            print(f"  {game['name']}: {len(cleaned)} chars")
        except Exception as e:
            print(f"  {game['name']}: Extraction failed: {e}")
            stats["failed"] += 1

    return stats


def run_summarize(registry_path: str, limit: int = 0) -> dict:
    from scripts.summarize import summarize_game
    games = get_stage_games(registry_path, "summarize", limit=limit)
    success = sum(1 for g in games if summarize_game(g, registry_path))
    return {"summarized": success, "failed": len(games) - success}


def run_quality_check(registry_path: str, limit: int = 0) -> dict:
    from scripts.quality_check import check_batch
    return check_batch(registry_path)


def show_status(registry_path: str):
    """Print pipeline status summary."""
    games = load_registry(registry_path)
    from collections import Counter
    counts = Counter(g.get("status", "unknown") for g in games)
    print(f"\nPipeline status ({len(games)} total games):")
    for status in ["queued", "searching", "found", "not_found", "downloaded",
                    "extracted", "summarized", "validated", "flagged", "pending"]:
        if counts.get(status, 0) > 0:
            print(f"  {status:15s} {counts[status]:5d}")


def main():
    parser = argparse.ArgumentParser(description="Batch pipeline orchestrator")
    parser.add_argument("--stage", choices=list(STAGE_ORDER.keys()) + ["all"],
                        help="Pipeline stage to run")
    parser.add_argument("--limit", type=int, default=0, help="Max games to process (0=all)")
    parser.add_argument("--registry", default="games.yaml")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    args = parser.parse_args()

    if args.status:
        show_status(args.registry)
        return

    if not args.stage:
        parser.print_help()
        sys.exit(1)

    stages = list(STAGE_ORDER.keys()) if args.stage == "all" else [args.stage]
    runners = {
        "download": run_download,
        "extract": run_extract,
        "summarize": run_summarize,
        "quality_check": run_quality_check,
    }

    for stage in stages:
        games = get_stage_games(args.registry, stage, limit=args.limit)
        if not games:
            print(f"\n[{stage}] No games ready for this stage.")
            continue
        print(f"\n[{stage}] Processing {len(games)} game(s)...")
        result = runners[stage](args.registry, args.limit)
        print(f"[{stage}] Result: {result}")


if __name__ == "__main__":
    main()
```

**Step 4: Run tests to verify they pass**

Run: `source .venv/bin/activate && python -m pytest tests/test_process_batch.py -v`

Expected: All tests PASS.

**Step 5: Commit**

```bash
git add scripts/process_batch.py tests/test_process_batch.py
git commit -m "feat: add process_batch orchestrator for pipeline stages"
```

---

## Task 7: PDF Finding Workflow (Claude Code Interactive)

This task is NOT a Python script — it's a documented workflow for using Claude Code with Playwright MCP tools to find rulebook PDFs. The registry helpers from Task 1 (`get_games_by_status`, `update_game`) provide the queue management.

**Files:**
- Modify: `CLAUDE.md` (add batch PDF finding workflow)

**Step 1: Add the workflow documentation to CLAUDE.md**

Add a new section to `CLAUDE.md` after the existing "Adding a New Game" section:

```markdown
## Batch PDF Finding (Interactive)

To find rulebook PDFs for queued games using Playwright browser tools:

1. Load the queue: `python -m scripts.process_batch --status` to see how many games need PDFs
2. Ask Claude Code: "Find rulebook PDFs for the next 20 queued games"
3. Claude will use Playwright to search these sites (in priority order):
   - **1j1ju.com** — search for game name, find English rulebook PDF link
   - **Google** — search `"{game name}" rulebook pdf`
   - **BGG files page** — `boardgamegeek.com/boardgame/{bgg_id}/files`
4. For each game found, Claude updates games.yaml: `status: found`, `pdf_url: "..."`
5. For games not found: `status: not_found`, `notes: "reason"`
6. After finding, run: `python -m scripts.process_batch --stage download --limit 20`

### Queue management helpers

```python
# In Python or Claude Code:
from scripts.registry import get_games_by_status, update_game

# Get next batch
games = get_games_by_status("games.yaml", "queued", limit=20)

# Record a found PDF
update_game("games.yaml", "Agricola", status="found",
            pdf_url="https://1j1ju.com/rules/agricola-en.pdf")

# Record not found
update_game("games.yaml", "Obscure Game", status="not_found",
            notes="No English rulebook found on 1j1ju, Google, or BGG")
```
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add batch PDF finding workflow to CLAUDE.md"
```

---

## Task 8: Update Documentation and Configuration

Final cleanup — update requirements, .env.example, and CLAUDE.md pipeline section.

**Files:**
- Modify: `requirements.txt`
- Modify: `.env.example`
- Modify: `CLAUDE.md` (update pipeline section with new stages)

**Step 1: Update requirements.txt**

Add `anthropic>=0.40.0` to `requirements.txt` (if not already done in Task 4).

**Step 2: Update .env.example**

Add `ANTHROPIC_API_KEY=your_key_here` line.

**Step 3: Update CLAUDE.md pipeline section**

Replace the "Adding a New Game" checklist with the updated pipeline that references the new scripts:

```markdown
## Pipeline (Batch Processing)

### Import games from boardgame-database
```bash
python -m scripts.import_games /path/to/boardgame-database/games/ \
  --master-csv /path/to/boardgame-database/master_list.csv \
  --limit 100
```

### Find PDFs (interactive with Claude Code + Playwright)
See "Batch PDF Finding" section below.

### Process pipeline stages
```bash
# Download all found PDFs
python -m scripts.process_batch --stage download --limit 50

# Extract text from downloaded PDFs
python -m scripts.process_batch --stage extract --limit 50

# Summarize extracted text via Claude API
python -m scripts.process_batch --stage summarize --limit 20

# Quality check summarized rules
python -m scripts.process_batch --stage quality_check

# Check overall pipeline status
python -m scripts.process_batch --status
```
```

**Step 4: Install new dependency**

```bash
source .venv/bin/activate && pip install anthropic>=0.40.0
```

**Step 5: Run all tests to verify nothing is broken**

```bash
source .venv/bin/activate && python -m pytest tests/ -v
```

Expected: All tests PASS.

**Step 6: Commit**

```bash
git add requirements.txt .env.example CLAUDE.md
git commit -m "docs: update pipeline docs, requirements, and config for batch processing"
```

---

## Summary

| Task | Script | Tests | Description |
|------|--------|-------|-------------|
| 1 | `registry.py` (modify) | `test_registry.py` (modify) | Add `update_game()` and `get_games_by_status()` |
| 2 | `import_games.py` (new) | `test_import_games.py` (new) | Import games from boardgame-database |
| 3 | `download_pdf.py` (new) | `test_download_pdf.py` (new) | Download PDFs with verification |
| 4 | `summarize.py` (new) | `test_summarize.py` (new) | Claude API summarization |
| 5 | `quality_check.py` (new) | `test_quality_check.py` (new) | Content scoring + flagging |
| 6 | `process_batch.py` (new) | `test_process_batch.py` (new) | Pipeline orchestrator |
| 7 | `CLAUDE.md` (modify) | — | PDF finding workflow docs |
| 8 | Config files (modify) | — | Requirements, .env, docs |
