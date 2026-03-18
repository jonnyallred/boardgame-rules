"""Game registry management -- reads/writes games.yaml."""

from __future__ import annotations

import yaml

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


def update_game(path: str, name: str, **fields) -> None:
    """Update arbitrary fields on a game entry (case-insensitive name match)."""
    games = load_registry(path)
    for game in games:
        if game["name"].lower() == name.lower():
            game.update(fields)
            break
    save_registry(path, games)


def get_games_by_status(path: str, status: str, limit: int = 0) -> list[dict]:
    """Return all games with a given status. Optional limit (0 = no limit)."""
    games = load_registry(path)
    matched = [g for g in games if g.get("status") == status]
    if limit > 0:
        return matched[:limit]
    return matched


def find_expansions(path: str, base_bgg_id: int) -> list[dict]:
    """Return all expansions for a given base game BGG ID."""
    games = load_registry(path)
    return [g for g in games if g.get("base_game_bgg_id") == base_bgg_id]


def find_base_game(path: str, bgg_id: int) -> dict | None:
    """Given an expansion's bgg_id, find its base game entry."""
    games = load_registry(path)
    # First find the expansion to get its base_game_bgg_id
    expansion = next((g for g in games if g["bgg_id"] == bgg_id), None)
    if not expansion or "base_game_bgg_id" not in expansion:
        return None
    base_bgg_id = expansion["base_game_bgg_id"]
    return next((g for g in games if g["bgg_id"] == base_bgg_id), None)
