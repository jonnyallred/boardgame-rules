import pytest
import yaml
from datetime import datetime, timedelta, timezone
from scripts.registry import load_registry, save_registry, find_game, add_game, update_status, update_game, get_games_by_status, claim_games_by_status, find_expansions, find_base_game

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


def test_claim_games_by_status_updates_registry(registry_path):
    for i in range(3):
        add_game(registry_path, name=f"Game{i}", bgg_id=i)
        update_status(registry_path, f"Game{i}", "queued")
    claimed = claim_games_by_status(registry_path, "queued", "searching", limit=2)
    assert len(claimed) == 2
    registry = load_registry(registry_path)
    statuses = [g["status"] for g in registry]
    assert statuses.count("searching") == 2
    assert statuses.count("queued") == 1


def test_claim_games_by_status_reclaims_stale_claims(registry_path):
    add_game(registry_path, name="Fresh", bgg_id=1)
    add_game(registry_path, name="Stale", bgg_id=2)
    update_status(registry_path, "Fresh", "searching")
    update_status(registry_path, "Stale", "searching")
    update_game(
        registry_path,
        "Fresh",
        claimed_at=(datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
    )
    update_game(
        registry_path,
        "Stale",
        claimed_at=(datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
    )

    claimed = claim_games_by_status(
        registry_path,
        "queued",
        "searching",
        reclaim_statuses=["searching"],
        reclaim_timeout_seconds=3600,
    )

    assert len(claimed) == 1
    assert claimed[0]["name"] == "Stale"


@pytest.fixture
def expansion_registry(tmp_path):
    path = tmp_path / "games.yaml"
    data = {
        "games": [
            {"name": "Catan", "bgg_id": 13, "status": "validated"},
            {"name": "Catan: Seafarers", "bgg_id": 325, "status": "pending", "base_game_bgg_id": 13},
            {"name": "Catan: Cities & Knights", "bgg_id": 926, "status": "pending", "base_game_bgg_id": 13},
            {"name": "Wingspan", "bgg_id": 266192, "status": "validated"},
        ]
    }
    path.write_text(yaml.dump(data))
    return str(path)


def test_find_expansions(expansion_registry):
    expansions = find_expansions(expansion_registry, 13)
    assert len(expansions) == 2
    assert {e["name"] for e in expansions} == {"Catan: Seafarers", "Catan: Cities & Knights"}


def test_find_expansions_none(expansion_registry):
    expansions = find_expansions(expansion_registry, 266192)
    assert expansions == []


def test_find_base_game(expansion_registry):
    base = find_base_game(expansion_registry, 325)
    assert base is not None
    assert base["name"] == "Catan"
    assert base["bgg_id"] == 13


def test_find_base_game_not_expansion(expansion_registry):
    base = find_base_game(expansion_registry, 13)
    assert base is None
