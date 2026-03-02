"""Scrape BGG game files page to find rulebook PDFs.

BGG's files page is JS-rendered, so this module provides both:
1. An HTML scraper for cases where server-rendered HTML is available
2. A fallback that constructs the files page URL for manual browsing
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
