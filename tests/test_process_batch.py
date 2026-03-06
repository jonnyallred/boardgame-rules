import pytest
import yaml
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


def test_get_stage_games_with_limit(registry_path):
    # Add more "found" games
    import yaml as _yaml
    data = _yaml.safe_load(open(registry_path))
    for i in range(10, 20):
        data["games"].append({"name": f"Game{i}", "bgg_id": i, "status": "found"})
    with open(registry_path, "w") as f:
        _yaml.dump(data, f)
    games = get_stage_games(registry_path, "download", limit=5)
    assert len(games) == 5
