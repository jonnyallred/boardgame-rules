"""BoardGameGeek XML API2 client for searching games and fetching metadata."""

from __future__ import annotations

import xml.etree.ElementTree as ET
import requests

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
