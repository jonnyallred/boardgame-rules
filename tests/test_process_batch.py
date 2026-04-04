import pytest
import yaml
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from scripts.process_batch import CLAIM_TIMEOUT_SECONDS, get_stage_games, run_extract, run_summarize, run_quality_check, STAGE_ORDER
from scripts.registry import load_registry, update_game


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


def test_run_extract_reverts_claimed_status_when_pdf_missing(registry_path, tmp_path):
    stats = run_extract(registry_path, limit=1)
    assert stats["skipped"] == 1
    games = load_registry(registry_path)
    assert next(g for g in games if g["name"] == "Game2")["status"] == "downloaded"


@patch("scripts.process_batch.summarize_game", return_value=False)
def test_run_summarize_reverts_claimed_status_on_failure(mock_summarize, registry_path):
    stats = run_summarize(registry_path, limit=1)
    assert stats["failed"] == 1
    games = load_registry(registry_path)
    assert next(g for g in games if g["name"] == "Game3")["status"] == "extracted"


@patch("scripts.process_batch.check_games", return_value={"validated": 0, "flagged": 0, "errors": 1})
def test_run_quality_check_claims_only_limited_games(mock_check_games, registry_path):
    extra = yaml.safe_load(open(registry_path))
    extra["games"].append({"name": "Game6", "bgg_id": 6, "status": "summarized"})
    with open(registry_path, "w") as f:
        yaml.dump(extra, f)
    run_quality_check(registry_path, limit=1)
    claimed_games = mock_check_games.call_args[0][0]
    assert len(claimed_games) == 1


@patch("scripts.process_batch.summarize_game", return_value=True)
def test_run_summarize_reclaims_stale_claim(mock_summarize, registry_path):
    update_game(
        registry_path,
        "Game3",
        status="summarizing",
        claimed_at=(datetime.now(timezone.utc) - timedelta(seconds=CLAIM_TIMEOUT_SECONDS + 5)).isoformat(),
    )
    stats = run_summarize(registry_path, limit=1)
    assert stats["processed"] == 1
    assert mock_summarize.call_args[0][0]["name"] == "Game3"
