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
