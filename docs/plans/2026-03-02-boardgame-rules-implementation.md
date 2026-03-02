# Boardgame Rules Database — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python pipeline that finds boardgame rulebook PDFs via BoardGameGeek, extracts text, and produces structured Markdown rule summaries.

**Architecture:** Flat file pipeline — three CLI scripts (`find_rulebook.py`, `extract_pdf.py`, `validate.py`) operate on a shared directory structure with `games.yaml` as the registry. No database or server.

**Tech Stack:** Python 3, PyMuPDF (fitz), pdfplumber, PyYAML, requests, beautifulsoup4

---

## Prerequisites

- Python 3.10+ available
- BGG API access token (register at https://boardgamegeek.com/applications, store in `.env` as `BGG_API_TOKEN`)

---

### Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `.env.example`
- Create: `games.yaml`
- Create: `source_pdfs/.gitkeep` (directory placeholder)
- Create: `extracted/.gitkeep`
- Create: `rules/.gitkeep`
- Create: `scripts/__init__.py` (empty)

**Step 1: Create requirements.txt**

```
PyMuPDF>=1.24.0
pdfplumber>=0.11.0
PyYAML>=6.0
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dotenv>=1.0.0
```

**Step 2: Create .gitignore**

```
source_pdfs/*.pdf
.env
__pycache__/
*.pyc
.venv/
```

**Step 3: Create .env.example**

```
BGG_API_TOKEN=your_token_here
```

**Step 4: Create games.yaml (empty registry)**

```yaml
# Boardgame Rules Registry
# Status: pending | downloaded | extracted | summarized
games: []
```

**Step 5: Create directory placeholders**

```bash
mkdir -p source_pdfs extracted rules scripts
touch source_pdfs/.gitkeep extracted/.gitkeep rules/.gitkeep scripts/__init__.py
```

**Step 6: Set up virtualenv and install dependencies**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Step 7: Commit**

```bash
git add requirements.txt .gitignore .env.example games.yaml source_pdfs/.gitkeep extracted/.gitkeep rules/.gitkeep scripts/__init__.py
git commit -m "feat: scaffold project structure and dependencies"
```

---

### Task 2: Game Registry Helper (scripts/registry.py)

Shared module for reading/writing `games.yaml`. All three scripts use this.

**Files:**
- Create: `scripts/registry.py`
- Create: `tests/test_registry.py`

**Step 1: Write the failing tests**

```python
# tests/test_registry.py
import os
import tempfile
import pytest
import yaml
from scripts.registry import load_registry, save_registry, find_game, add_game, update_status

@pytest.fixture
def registry_path(tmp_path):
    path = tmp_path / "games.yaml"
    path.write_text("games: []\n")
    return str(path)

@pytest.fixture
def populated_registry(tmp_path):
    path = tmp_path / "games.yaml"
    data = {
        "games": [
            {"name": "Catan", "bgg_id": 13, "status": "pending"},
            {"name": "Wingspan", "bgg_id": 266192, "status": "downloaded"},
        ]
    }
    path.write_text(yaml.dump(data))
    return str(path)

def test_load_empty_registry(registry_path):
    reg = load_registry(registry_path)
    assert reg == []

def test_load_populated_registry(populated_registry):
    reg = load_registry(populated_registry)
    assert len(reg) == 2
    assert reg[0]["name"] == "Catan"

def test_add_game(registry_path):
    add_game(registry_path, name="Catan", bgg_id=13)
    reg = load_registry(registry_path)
    assert len(reg) == 1
    assert reg[0]["name"] == "Catan"
    assert reg[0]["bgg_id"] == 13
    assert reg[0]["status"] == "pending"

def test_add_game_no_duplicates(registry_path):
    add_game(registry_path, name="Catan", bgg_id=13)
    add_game(registry_path, name="Catan", bgg_id=13)
    reg = load_registry(registry_path)
    assert len(reg) == 1

def test_find_game(populated_registry):
    game = find_game(populated_registry, "Catan")
    assert game is not None
    assert game["bgg_id"] == 13

def test_find_game_missing(populated_registry):
    game = find_game(populated_registry, "Nonexistent")
    assert game is None

def test_update_status(populated_registry):
    update_status(populated_registry, "Catan", "extracted")
    game = find_game(populated_registry, "Catan")
    assert game["status"] == "extracted"

def test_save_registry(registry_path):
    games = [{"name": "Catan", "bgg_id": 13, "status": "pending"}]
    save_registry(registry_path, games)
    loaded = load_registry(registry_path)
    assert loaded == games
```

**Step 2: Run tests to verify they fail**

```bash
source .venv/bin/activate
pip install pytest
python -m pytest tests/test_registry.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.registry'`

**Step 3: Implement scripts/registry.py**

```python
"""Game registry management — reads/writes games.yaml."""

import yaml
from pathlib import Path

DEFAULT_REGISTRY = "games.yaml"


def load_registry(path: str = DEFAULT_REGISTRY) -> list[dict]:
    """Load games list from registry YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("games", []) or []


def save_registry(path: str, games: list[dict]) -> None:
    """Write games list back to registry YAML file."""
    with open(path, "w") as f:
        yaml.dump({"games": games}, f, default_flow_style=False, sort_keys=False)


def find_game(path: str, name: str) -> dict | None:
    """Find a game by name (case-insensitive)."""
    games = load_registry(path)
    for game in games:
        if game["name"].lower() == name.lower():
            return game
    return None


def add_game(path: str, *, name: str, bgg_id: int, **extra) -> dict:
    """Add a game to the registry. Skips if already exists (by bgg_id)."""
    games = load_registry(path)
    for game in games:
        if game["bgg_id"] == bgg_id:
            return game
    entry = {"name": name, "bgg_id": bgg_id, "status": "pending", **extra}
    games.append(entry)
    save_registry(path, games)
    return entry


def update_status(path: str, name: str, status: str) -> None:
    """Update a game's pipeline status."""
    games = load_registry(path)
    for game in games:
        if game["name"].lower() == name.lower():
            game["status"] = status
            break
    save_registry(path, games)
```

**Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/test_registry.py -v
```

Expected: All 8 tests PASS

**Step 5: Commit**

```bash
git add scripts/registry.py tests/test_registry.py
git commit -m "feat: add game registry helper for games.yaml management"
```

---

### Task 3: BGG Search & Metadata (scripts/bgg.py)

Wraps BGG XML API2 for searching games and fetching metadata. Requires auth token.

**Files:**
- Create: `scripts/bgg.py`
- Create: `tests/test_bgg.py`

**Step 1: Write the failing tests**

```python
# tests/test_bgg.py
import pytest
from unittest.mock import patch, MagicMock
from scripts.bgg import search_game, get_game_details, parse_search_results, parse_game_details

SEARCH_XML = """<?xml version="1.0" encoding="utf-8"?>
<items total="2" termsofuse="https://boardgamegeek.com/xmlapi/termsofuse">
    <item type="boardgame" id="13">
        <name type="primary" value="Catan"/>
        <yearpublished value="1995"/>
    </item>
    <item type="boardgame" id="278">
        <name type="primary" value="Catan Card Game"/>
        <yearpublished value="1996"/>
    </item>
</items>"""

THING_XML = """<?xml version="1.0" encoding="utf-8"?>
<items termsofuse="https://boardgamegeek.com/xmlapi/termsofuse">
    <item type="boardgame" id="13">
        <name type="primary" sortindex="1" value="Catan"/>
        <description>In Catan, players try to be the dominant force on the island.</description>
        <yearpublished value="1995"/>
        <minplayers value="3"/>
        <maxplayers value="4"/>
        <minplaytime value="60"/>
        <maxplaytime value="120"/>
        <link type="boardgamedesigner" id="11" value="Klaus Teuber"/>
        <link type="boardgamepublisher" id="37" value="KOSMOS"/>
    </item>
</items>"""


def test_parse_search_results():
    results = parse_search_results(SEARCH_XML)
    assert len(results) == 2
    assert results[0]["id"] == 13
    assert results[0]["name"] == "Catan"
    assert results[0]["year"] == 1995


def test_parse_game_details():
    details = parse_game_details(THING_XML)
    assert details["name"] == "Catan"
    assert details["bgg_id"] == 13
    assert details["player_count"] == "3-4"
    assert details["play_time"] == "60-120 min"
    assert details["designer"] == "Klaus Teuber"
    assert details["year"] == 1995


@patch("scripts.bgg.requests.get")
def test_search_game(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = SEARCH_XML
    mock_get.return_value = mock_resp

    results = search_game("Catan", token="test-token")
    assert len(results) == 2
    mock_get.assert_called_once()
    # Verify auth header was sent
    call_kwargs = mock_get.call_args
    assert "Authorization" in call_kwargs[1]["headers"]


@patch("scripts.bgg.requests.get")
def test_get_game_details(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = THING_XML
    mock_get.return_value = mock_resp

    details = get_game_details(13, token="test-token")
    assert details["name"] == "Catan"
    assert details["bgg_id"] == 13
```

**Step 2: Run tests to verify they fail**

```bash
python -m pytest tests/test_bgg.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.bgg'`

**Step 3: Implement scripts/bgg.py**

```python
"""BoardGameGeek XML API2 client for searching games and fetching metadata."""

import xml.etree.ElementTree as ET
import requests
import time

BGG_API_BASE = "https://boardgamegeek.com/xmlapi2"


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def search_game(query: str, token: str) -> list[dict]:
    """Search BGG for a game by name. Returns list of {id, name, year}."""
    resp = requests.get(
        f"{BGG_API_BASE}/search",
        params={"query": query, "type": "boardgame"},
        headers=_headers(token),
    )
    resp.raise_for_status()
    return parse_search_results(resp.text)


def get_game_details(bgg_id: int, token: str) -> dict:
    """Fetch detailed metadata for a game by BGG ID."""
    resp = requests.get(
        f"{BGG_API_BASE}/thing",
        params={"id": bgg_id, "type": "boardgame"},
        headers=_headers(token),
    )
    resp.raise_for_status()
    return parse_game_details(resp.text)


def parse_search_results(xml_text: str) -> list[dict]:
    """Parse BGG search XML into a list of result dicts."""
    root = ET.fromstring(xml_text)
    results = []
    for item in root.findall("item"):
        name_el = item.find("name")
        year_el = item.find("yearpublished")
        results.append({
            "id": int(item.get("id")),
            "name": name_el.get("value") if name_el is not None else "",
            "year": int(year_el.get("value")) if year_el is not None else None,
        })
    return results


def parse_game_details(xml_text: str) -> dict:
    """Parse BGG thing XML into a game details dict."""
    root = ET.fromstring(xml_text)
    item = root.find("item")

    name = ""
    for name_el in item.findall("name"):
        if name_el.get("type") == "primary":
            name = name_el.get("value")
            break

    minp = item.find("minplayers")
    maxp = item.find("maxplayers")
    mint = item.find("minplaytime")
    maxt = item.find("maxplaytime")
    year_el = item.find("yearpublished")

    designers = [
        link.get("value")
        for link in item.findall("link")
        if link.get("type") == "boardgamedesigner"
    ]

    min_players = int(minp.get("value")) if minp is not None else None
    max_players = int(maxp.get("value")) if maxp is not None else None
    min_time = int(mint.get("value")) if mint is not None else None
    max_time = int(maxt.get("value")) if maxt is not None else None

    player_count = f"{min_players}-{max_players}" if min_players and max_players else None
    play_time = f"{min_time}-{max_time} min" if min_time and max_time else None

    return {
        "name": name,
        "bgg_id": int(item.get("id")),
        "player_count": player_count,
        "play_time": play_time,
        "designer": ", ".join(designers) if designers else None,
        "year": int(year_el.get("value")) if year_el is not None else None,
    }
```

**Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/test_bgg.py -v
```

Expected: All 4 tests PASS

**Step 5: Commit**

```bash
git add scripts/bgg.py tests/test_bgg.py
git commit -m "feat: add BGG XML API2 client for game search and metadata"
```

---

### Task 4: BGG Files Page Scraper (scripts/bgg_files.py)

Scrapes the BGG game files page to find rulebook PDF download links. The BGG API does not expose file listings, so we scrape the HTML.

**Files:**
- Create: `scripts/bgg_files.py`
- Create: `tests/test_bgg_files.py`

**Step 1: Write the failing tests**

Note: This scraper depends on BGG's HTML structure. Tests use fixture HTML. If BGG changes their layout, the scraper will need updating.

```python
# tests/test_bgg_files.py
import pytest
from unittest.mock import patch, MagicMock
from scripts.bgg_files import parse_files_page, find_rulebook_files

# Minimal fixture mimicking BGG files page structure.
# BGG uses a JS-rendered page, so we'll test with the pattern we expect
# from their server-rendered fallback / API response.
FILES_HTML = """
<html><body>
<div class="file-list">
  <div class="file-row">
    <a href="/filepage/12345/catan-rules-english" class="file-link">Catan Rules (English)</a>
    <span class="file-category">Rules</span>
    <a href="/file/download_redirect/abc123def/CatanRules.pdf" class="download-link">Download</a>
  </div>
  <div class="file-row">
    <a href="/filepage/12346/catan-faq" class="file-link">Catan FAQ</a>
    <span class="file-category">FAQ</span>
    <a href="/file/download_redirect/xyz789/CatanFAQ.pdf" class="download-link">Download</a>
  </div>
  <div class="file-row">
    <a href="/filepage/12347/catan-reference-card" class="file-link">Catan Player Reference</a>
    <span class="file-category">Player Aid</span>
    <a href="/file/download_redirect/ref456/CatanRef.pdf" class="download-link">Download</a>
  </div>
</div>
</body></html>
"""


def test_parse_files_page():
    files = parse_files_page(FILES_HTML)
    assert len(files) == 3
    assert files[0]["title"] == "Catan Rules (English)"
    assert files[0]["category"] == "Rules"
    assert "download_redirect" in files[0]["download_url"]


def test_find_rulebook_files():
    files = parse_files_page(FILES_HTML)
    rulebooks = find_rulebook_files(files)
    # Should prefer files with "Rules" category or "rule" in title
    assert len(rulebooks) >= 1
    assert rulebooks[0]["title"] == "Catan Rules (English)"
```

**Step 2: Run tests to verify they fail**

```bash
python -m pytest tests/test_bgg_files.py -v
```

Expected: FAIL — `ModuleNotFoundError`

**Step 3: Implement scripts/bgg_files.py**

```python
"""Scrape BGG game files page to find rulebook PDFs.

BGG's files page is JS-rendered, so this module provides both:
1. An HTML scraper for cases where server-rendered HTML is available
2. A fallback that constructs the files page URL for manual browsing

The HTML structure may change — update parse_files_page() if needed.
"""

import re
import requests
from bs4 import BeautifulSoup

BGG_BASE = "https://boardgamegeek.com"


def files_page_url(bgg_id: int) -> str:
    """Construct the URL for a game's files page on BGG."""
    return f"{BGG_BASE}/boardgame/{bgg_id}/files"


def fetch_files_page(bgg_id: int) -> str:
    """Fetch the HTML of a game's files page."""
    resp = requests.get(files_page_url(bgg_id))
    resp.raise_for_status()
    return resp.text


def parse_files_page(html: str) -> list[dict]:
    """Parse file entries from BGG files page HTML.

    Returns list of dicts with keys: title, category, download_url, filepage_url
    """
    soup = BeautifulSoup(html, "html.parser")
    files = []

    for row in soup.select(".file-row"):
        file_link = row.select_one(".file-link, a[href*='/filepage/']")
        category_el = row.select_one(".file-category")
        download_link = row.select_one(".download-link, a[href*='download_redirect']")

        if not file_link:
            continue

        entry = {
            "title": file_link.get_text(strip=True),
            "category": category_el.get_text(strip=True) if category_el else "",
            "filepage_url": BGG_BASE + file_link.get("href", ""),
            "download_url": (
                BGG_BASE + download_link.get("href", "")
                if download_link
                else None
            ),
        }
        files.append(entry)

    return files


def find_rulebook_files(files: list[dict]) -> list[dict]:
    """Filter and rank files to find likely rulebook PDFs.

    Prioritizes by: 'Rules' category > 'rule' in title > other files.
    """
    rule_pattern = re.compile(r"\brule", re.IGNORECASE)

    def score(f: dict) -> int:
        s = 0
        if f.get("category", "").lower() == "rules":
            s += 10
        if rule_pattern.search(f.get("title", "")):
            s += 5
        if "english" in f.get("title", "").lower():
            s += 3
        return s

    scored = [(score(f), f) for f in files]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [f for s, f in scored if s > 0]
```

**Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/test_bgg_files.py -v
```

Expected: All 2 tests PASS

**Step 5: Commit**

```bash
git add scripts/bgg_files.py tests/test_bgg_files.py
git commit -m "feat: add BGG files page scraper for finding rulebook PDFs"
```

---

### Task 5: find_rulebook.py CLI Script

Combines BGG search, metadata, files scraping, and PDF download into one CLI tool.

**Files:**
- Create: `scripts/find_rulebook.py`

**Step 1: Implement the CLI script**

```python
#!/usr/bin/env python3
"""Find and download boardgame rulebook PDFs from BoardGameGeek.

Usage:
    python -m scripts.find_rulebook "Catan"
    python -m scripts.find_rulebook "Catan" --registry games.yaml
"""

import argparse
import os
import sys
import re
import requests
from pathlib import Path
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
        print("Use --force to re-download (not yet implemented)")
        return

    # Search BGG
    print(f"Searching BGG for '{args.game_name}'...")
    results = search_game(args.game_name, token=token)

    if not results:
        print("No results found.")
        sys.exit(1)

    # Show results and let user pick
    print(f"\nFound {len(results)} results:")
    for i, r in enumerate(results[:10]):
        year = f" ({r['year']})" if r.get("year") else ""
        print(f"  [{i}] {r['name']}{year} (BGG ID: {r['id']})")

    if len(results) == 1:
        choice = 0
    else:
        try:
            choice = int(input("\nSelect game number [0]: ") or "0")
        except (ValueError, EOFError):
            choice = 0

    selected = results[choice]
    print(f"\nFetching details for '{selected['name']}'...")
    details = get_game_details(selected["id"], token=token)

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
```

**Step 2: Test manually**

```bash
# With a valid BGG_API_TOKEN in .env:
python -m scripts.find_rulebook "Catan"
```

Expected: Searches BGG, shows results, downloads PDF to source_pdfs/

**Step 3: Commit**

```bash
git add scripts/find_rulebook.py
git commit -m "feat: add find_rulebook CLI for searching and downloading from BGG"
```

---

### Task 6: PDF Text Extraction (scripts/extract_pdf.py)

**Files:**
- Create: `scripts/extract_pdf.py`
- Create: `tests/test_extract_pdf.py`

**Step 1: Write the failing tests**

```python
# tests/test_extract_pdf.py
import os
import tempfile
import pytest
from scripts.extract_pdf import extract_text, clean_text

# Note: We can't test PDF extraction without actual PDFs.
# These tests cover the text cleaning logic.

def test_clean_text_removes_page_numbers():
    text = "Some rules text\n\n42\n\nMore rules text"
    cleaned = clean_text(text)
    # Standalone page numbers (just a number on its own line) should be removed
    assert "\n42\n" not in cleaned
    assert "Some rules text" in cleaned
    assert "More rules text" in cleaned


def test_clean_text_removes_headers_footers():
    text = "© 2024 KOSMOS\nSome rules\n© 2024 KOSMOS\nMore rules\n© 2024 KOSMOS"
    cleaned = clean_text(text)
    # Repeated copyright lines (appearing 3+ times) treated as headers/footers
    assert cleaned.count("© 2024 KOSMOS") <= 1


def test_clean_text_normalizes_whitespace():
    text = "Rules   text   here\n\n\n\n\nMore text"
    cleaned = clean_text(text)
    assert "Rules text here" in cleaned  # collapsed spaces
    assert "\n\n\n" not in cleaned  # no triple+ newlines


def test_clean_text_preserves_content():
    text = "Players: 3-4\nTime: 60 minutes\n\nSetup: Place the board in the center."
    cleaned = clean_text(text)
    assert "Players: 3-4" in cleaned
    assert "Time: 60 minutes" in cleaned
    assert "Setup: Place the board in the center." in cleaned
```

**Step 2: Run tests to verify they fail**

```bash
python -m pytest tests/test_extract_pdf.py -v
```

Expected: FAIL — `ModuleNotFoundError`

**Step 3: Implement scripts/extract_pdf.py**

```python
#!/usr/bin/env python3
"""Extract text from boardgame rulebook PDFs.

Usage:
    python -m scripts.extract_pdf source_pdfs/catan-rules.pdf
    python -m scripts.extract_pdf source_pdfs/catan-rules.pdf --output extracted/catan.txt
"""

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

import fitz  # PyMuPDF

from scripts.registry import update_status, find_game, load_registry

EXTRACTED_DIR = "extracted"


def extract_text(pdf_path: str) -> str:
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            pages.append(text)
    doc.close()
    return "\n\n".join(pages)


def extract_text_pdfplumber(pdf_path: str) -> str:
    """Fallback extraction using pdfplumber (better for tables)."""
    import pdfplumber

    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text)

            # Also extract tables
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cells = [str(c) if c else "" for c in row]
                    pages.append(" | ".join(cells))

    return "\n\n".join(pages)


def clean_text(text: str) -> str:
    """Clean extracted PDF text: remove artifacts, normalize whitespace."""
    lines = text.split("\n")

    # Count line frequencies to detect repeated headers/footers
    line_counts = Counter(line.strip() for line in lines if line.strip())
    total_pages = text.count("\f") + 1  # rough page count
    threshold = max(3, total_pages // 2)

    cleaned_lines = []
    for line in lines:
        stripped = line.strip()

        # Remove standalone page numbers
        if re.match(r"^\d{1,3}$", stripped):
            continue

        # Remove repeated headers/footers (lines appearing on many pages)
        if stripped and line_counts[stripped] >= threshold:
            continue

        # Collapse multiple spaces within a line
        line = re.sub(r"  +", " ", line)

        cleaned_lines.append(line)

    result = "\n".join(cleaned_lines)

    # Collapse 3+ consecutive blank lines to 2
    result = re.sub(r"\n{3,}", "\n\n", result)

    return result.strip()


def main():
    parser = argparse.ArgumentParser(description="Extract text from boardgame rulebook PDFs")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output", help="Output text file path (default: extracted/<name>.txt)")
    parser.add_argument("--method", choices=["pymupdf", "pdfplumber"], default="pymupdf",
                        help="Extraction method (default: pymupdf)")
    parser.add_argument("--registry", default="games.yaml", help="Path to games.yaml")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF not found: {args.pdf_path}")
        sys.exit(1)

    # Determine output path
    pdf_stem = Path(args.pdf_path).stem
    if args.output:
        output_path = args.output
    else:
        os.makedirs(EXTRACTED_DIR, exist_ok=True)
        output_path = os.path.join(EXTRACTED_DIR, f"{pdf_stem}.txt")

    # Extract
    print(f"Extracting text from {args.pdf_path} (method: {args.method})...")
    if args.method == "pdfplumber":
        raw_text = extract_text_pdfplumber(args.pdf_path)
    else:
        raw_text = extract_text(args.pdf_path)

    print(f"  Raw text: {len(raw_text)} characters")

    # Clean
    cleaned = clean_text(raw_text)
    print(f"  Cleaned text: {len(cleaned)} characters")

    # Write
    with open(output_path, "w") as f:
        f.write(cleaned)
    print(f"  Saved to: {output_path}")

    # Update registry if we can match the game
    # Try to match PDF filename to a game in the registry
    games = load_registry(args.registry)
    for game in games:
        slug = re.sub(r"[^a-z0-9]+", "-", game["name"].lower()).strip("-")
        if slug in pdf_stem.lower():
            update_status(args.registry, game["name"], "extracted")
            print(f"  Updated registry: {game['name']} → extracted")
            break


if __name__ == "__main__":
    main()
```

**Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/test_extract_pdf.py -v
```

Expected: All 4 tests PASS

**Step 5: Commit**

```bash
git add scripts/extract_pdf.py tests/test_extract_pdf.py
git commit -m "feat: add PDF text extraction with PyMuPDF and text cleaning"
```

---

### Task 7: Validation Script (scripts/validate.py)

**Files:**
- Create: `scripts/validate.py`
- Create: `tests/test_validate.py`

**Step 1: Write the failing tests**

```python
# tests/test_validate.py
import os
import pytest
from scripts.validate import validate_rules_file, validate_all

VALID_RULES = """---
title: "Catan"
bgg_id: 13
player_count: "3-4"
play_time: "60-120 min"
designer: "Klaus Teuber"
source_pdf: "catan-rules.pdf"
extracted_date: "2026-03-02"
summarized_date: "2026-03-02"
rulebook_version: "5th Edition"
---

# Catan

## Overview
Build settlements on the island of Catan.

## Components
- 19 terrain hexes
- 6 sea frame pieces

## Setup
Place the board in the center of the table.

## Turn Structure
Roll dice, collect resources, trade, build.

## Actions
Build roads, settlements, cities. Buy development cards.

## Scoring / Victory Conditions
First player to 10 victory points wins.

## Special Rules & Edge Cases
Robber activates on a 7.

## Player Reference
Road: 1 brick + 1 lumber
"""

MISSING_SECTIONS = """---
title: "Catan"
bgg_id: 13
---

# Catan

## Overview
A game.

## Setup
Set it up.
"""

NO_FRONTMATTER = """# Catan

## Overview
A game about trading.
"""


def test_validate_valid_file(tmp_path):
    path = tmp_path / "catan.md"
    path.write_text(VALID_RULES)
    errors = validate_rules_file(str(path))
    assert errors == []


def test_validate_missing_sections(tmp_path):
    path = tmp_path / "catan.md"
    path.write_text(MISSING_SECTIONS)
    errors = validate_rules_file(str(path))
    assert any("Components" in e for e in errors)
    assert any("Turn Structure" in e for e in errors)


def test_validate_no_frontmatter(tmp_path):
    path = tmp_path / "catan.md"
    path.write_text(NO_FRONTMATTER)
    errors = validate_rules_file(str(path))
    assert any("frontmatter" in e.lower() for e in errors)


def test_validate_missing_required_fields(tmp_path):
    incomplete = """---
title: "Catan"
---

# Catan

## Overview
## Components
## Setup
## Turn Structure
## Actions
## Scoring / Victory Conditions
## Special Rules & Edge Cases
## Player Reference
"""
    path = tmp_path / "catan.md"
    path.write_text(incomplete)
    errors = validate_rules_file(str(path))
    assert any("bgg_id" in e for e in errors)
```

**Step 2: Run tests to verify they fail**

```bash
python -m pytest tests/test_validate.py -v
```

Expected: FAIL — `ModuleNotFoundError`

**Step 3: Implement scripts/validate.py**

```python
#!/usr/bin/env python3
"""Validate rules markdown files for completeness.

Usage:
    python -m scripts.validate
    python -m scripts.validate rules/catan.md
"""

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

RULES_DIR = "rules"

REQUIRED_FRONTMATTER = ["title", "bgg_id"]

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


def validate_rules_file(path: str) -> list[str]:
    """Validate a rules markdown file. Returns list of error messages."""
    errors = []
    content = Path(path).read_text()
    filename = os.path.basename(path)

    # Check frontmatter
    fm_match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not fm_match:
        errors.append(f"{filename}: No YAML frontmatter found")
        return errors

    try:
        frontmatter = yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{filename}: Invalid YAML frontmatter: {e}")
        return errors

    # Check required fields
    for field in REQUIRED_FRONTMATTER:
        if field not in frontmatter:
            errors.append(f"{filename}: Missing required frontmatter field: {field}")

    # Check sections
    body = content[fm_match.end():]
    for section in EXPECTED_SECTIONS:
        pattern = rf"^## {re.escape(section)}"
        if not re.search(pattern, body, re.MULTILINE):
            errors.append(f"{filename}: Missing section: {section}")

    return errors


def validate_all(rules_dir: str = RULES_DIR) -> dict[str, list[str]]:
    """Validate all .md files in the rules directory."""
    results = {}
    rules_path = Path(rules_dir)

    if not rules_path.exists():
        return {}

    for md_file in sorted(rules_path.glob("*.md")):
        errors = validate_rules_file(str(md_file))
        results[md_file.name] = errors

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate rules markdown files")
    parser.add_argument("files", nargs="*", help="Specific files to validate (default: all in rules/)")
    parser.add_argument("--rules-dir", default=RULES_DIR, help="Rules directory")
    args = parser.parse_args()

    if args.files:
        all_errors = {}
        for f in args.files:
            all_errors[f] = validate_rules_file(f)
    else:
        all_errors = validate_all(args.rules_dir)

    if not all_errors:
        print("No rules files found.")
        sys.exit(0)

    has_errors = False
    for filename, errors in all_errors.items():
        if errors:
            has_errors = True
            print(f"\n{filename}:")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"{filename}: OK")

    if has_errors:
        sys.exit(1)
    else:
        print(f"\nAll {len(all_errors)} file(s) valid.")


if __name__ == "__main__":
    main()
```

**Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/test_validate.py -v
```

Expected: All 4 tests PASS

**Step 5: Commit**

```bash
git add scripts/validate.py tests/test_validate.py
git commit -m "feat: add rules file validation for frontmatter and sections"
```

---

### Task 8: End-to-End Test with a Real Game

Manual integration test. Process one game through the full pipeline.

**Step 1: Set up BGG API token**

```bash
# Get your token from https://boardgamegeek.com/applications
echo "BGG_API_TOKEN=your_actual_token" > .env
```

**Step 2: Find and download a rulebook**

```bash
source .venv/bin/activate
python -m scripts.find_rulebook "Catan"
```

Verify: PDF appears in `source_pdfs/`, game added to `games.yaml` with status `downloaded`

**Step 3: Extract text**

```bash
python -m scripts.extract_pdf source_pdfs/catan-rules.pdf
```

Verify: Text file appears in `extracted/`, review it for quality. If tables are mangled, try:

```bash
python -m scripts.extract_pdf source_pdfs/catan-rules.pdf --method pdfplumber
```

**Step 4: Interactive summarization**

This is the Claude Code interactive step. Read the extracted text, then create the rules markdown using the template format.

**Step 5: Validate**

```bash
python -m scripts.validate
```

Expected: `catan.md: OK`

**Step 6: Commit the results**

```bash
git add extracted/ rules/ games.yaml
git commit -m "feat: add Catan rules (first game in database)"
```

---

### Task 9: Final Cleanup

**Step 1: Add a CLAUDE.md for this project**

Create `CLAUDE.md` with project conventions so Claude Code knows how to work with this repo in future sessions.

```markdown
# Boardgame Rules Database

## Project Structure
- `games.yaml` — master game registry (name, bgg_id, status)
- `source_pdfs/` — downloaded PDFs (gitignored)
- `extracted/` — raw extracted text from PDFs
- `rules/` — final structured markdown files with YAML frontmatter
- `scripts/` — Python pipeline tools

## Pipeline
1. `python -m scripts.find_rulebook "Game Name"` — search BGG, download PDF
2. `python -m scripts.extract_pdf source_pdfs/game.pdf` — extract text
3. Interactive summarization with Claude Code
4. `python -m scripts.validate` — check completeness

## Rules File Format
YAML frontmatter (title, bgg_id, player_count, play_time, designer, source_pdf, extracted_date, summarized_date, rulebook_version) + Markdown body with sections: Overview, Components, Setup, Turn Structure, Actions, Scoring / Victory Conditions, Special Rules & Edge Cases, Player Reference.

## Testing
```bash
python -m pytest tests/ -v
```

## Requirements
- Python 3.10+
- BGG API token in `.env` (register at https://boardgamegeek.com/applications)
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md with project conventions"
```
