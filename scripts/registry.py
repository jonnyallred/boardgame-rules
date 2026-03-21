"""Game registry management -- reads/writes games.yaml.

All writes go through save_registry(), which uses fcntl.flock() to prevent
concurrent processes from corrupting the file. The lock is held for the
entire read-modify-write cycle via the locked_registry() context manager.
"""

from __future__ import annotations

import contextlib
import fcntl
import os
import tempfile
import yaml

DEFAULT_REGISTRY = "games.yaml"

LOCK_SUFFIX = ".lock"


@contextlib.contextmanager
def locked_registry(path: str):
    """Context manager that yields (games_list, save_fn) under an exclusive file lock.

    Usage:
        with locked_registry("games.yaml") as (games, save):
            for g in games:
                if g["name"] == target:
                    g["status"] = "summarized"
            save(games)

    The lock is held from entry until exit, ensuring the full read-modify-write
    is atomic with respect to other processes using the same lock file.
    """
    lock_path = path + LOCK_SUFFIX
    lock_fd = open(lock_path, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        # Read inside the lock
        games = _load_unlocked(path)

        def save(updated_games: list[dict]) -> None:
            _save_unlocked(path, updated_games)

        yield games, save
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()


def _load_unlocked(path: str) -> list[dict]:
    """Load games list (no locking -- caller must hold the lock)."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("games", []) or []


def _save_unlocked(path: str, games: list[dict]) -> None:
    """Atomic write via temp file + rename (no locking -- caller must hold the lock)."""
    dir_name = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            yaml.dump({"games": games}, f, default_flow_style=False, sort_keys=False)
        os.replace(tmp_path, path)
    except BaseException:
        os.unlink(tmp_path)
        raise


def load_registry(path: str = DEFAULT_REGISTRY) -> list[dict]:
    """Load games list from registry YAML file (read-only, no lock)."""
    return _load_unlocked(path)


def save_registry(path: str, games: list[dict]) -> None:
    """Write games list back to registry YAML file (locked, atomic)."""
    lock_path = path + LOCK_SUFFIX
    lock_fd = open(lock_path, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        _save_unlocked(path, games)
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()


def find_game(path: str, name: str) -> dict | None:
    """Find a game by name (case-insensitive)."""
    games = load_registry(path)
    for game in games:
        if game["name"].lower() == name.lower():
            return game
    return None


def add_game(path: str, *, name: str, bgg_id: int, **extra) -> dict:
    """Add a game to the registry. Skips if already exists (by bgg_id)."""
    with locked_registry(path) as (games, save):
        for game in games:
            if game["bgg_id"] == bgg_id:
                return game
        entry = {"name": name, "bgg_id": bgg_id, "status": "pending", **extra}
        games.append(entry)
        save(games)
        return entry


def update_status(path: str, name: str, status: str) -> None:
    """Update a game's pipeline status."""
    with locked_registry(path) as (games, save):
        for game in games:
            if game["name"].lower() == name.lower():
                game["status"] = status
                break
        save(games)


def update_game(path: str, name: str, **fields) -> None:
    """Update arbitrary fields on a game entry (case-insensitive name match)."""
    with locked_registry(path) as (games, save):
        for game in games:
            if game["name"].lower() == name.lower():
                game.update(fields)
                break
        save(games)


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
