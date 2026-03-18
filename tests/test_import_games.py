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


def test_build_bgg_lookup_uses_yaml_id(tmp_path):
    """When yaml_id is present in a CSV row, it should be used as the lookup key
    instead of the slugified name."""
    csv_path = tmp_path / "master_list.csv"
    csv_path.write_text(
        "bgg_id,name,year,type,status,notes,yaml_id\n"
        "174430,Gloomhaven,2017,boardgame,,,gloomhaven-2nd-ed\n"
    )
    lookup = build_bgg_lookup(str(csv_path))
    # The yaml_id key should be used, not the slugified name
    assert "gloomhaven-2nd-ed" in lookup
    assert lookup["gloomhaven-2nd-ed"] == 174430
    # The slugified name should NOT be present as a key
    assert "gloomhaven" not in lookup


def test_import_formats_designer(registry_path, mock_db, mock_master_csv):
    import_from_database(mock_db, registry_path, mock_master_csv)
    reg = load_registry(registry_path)
    agricola = next(g for g in reg if g["name"] == "Agricola")
    assert agricola["designer"] == "Uwe Rosenberg"


@pytest.fixture
def typed_mock_db(tmp_path):
    """Mock DB with a base game and an expansion."""
    games_dir = tmp_path / "typed_games"
    games_dir.mkdir()
    for game in [
        {"id": "agricola", "name": "Agricola", "year": 2007, "designer": ["Uwe Rosenberg"]},
        {"id": "catan", "name": "Catan", "year": 1995, "designer": ["Klaus Teuber"]},
        {"id": "catan-seafarers", "name": "Catan: Seafarers", "year": 1997, "designer": ["Klaus Teuber"]},
    ]:
        (games_dir / f"{game['id']}.yaml").write_text(yaml.dump(game))
    return str(games_dir)


@pytest.fixture
def typed_master_csv(tmp_path):
    """CSV with type column including boardgame and expansion."""
    csv_path = tmp_path / "master_list.csv"
    csv_path.write_text(
        "bgg_id,name,year,type,status,notes,yaml_id\n"
        "31260,Agricola,2007,boardgame,,,\n"
        "13,Catan,1995,boardgame,,,\n"
        "325,Catan: Seafarers,1997,boardgameexpansion,,,catan-seafarers\n"
    )
    return str(csv_path)


def test_import_type_filter(registry_path, typed_mock_db, typed_master_csv):
    """--type boardgame should exclude expansions."""
    # Without filter: all 3 imported
    stats_all = import_from_database(
        typed_mock_db, registry_path, typed_master_csv
    )
    assert stats_all["imported"] == 3

    # Reset registry
    Path(registry_path).write_text("games: []\n")

    # With filter: only boardgames
    stats_filtered = import_from_database(
        typed_mock_db, registry_path, typed_master_csv, game_type="boardgame"
    )
    reg = load_registry(registry_path)
    names = [g["name"] for g in reg]
    assert "Catan: Seafarers" not in names
    assert stats_filtered["imported"] == 2


def test_import_formats_designer_multiple(tmp_path, registry_path, mock_master_csv):
    """Designer list with multiple entries should be comma-joined."""
    games_dir = tmp_path / "games"
    games_dir.mkdir()
    game = {
        "id": "agricola",
        "name": "Agricola",
        "year": 2007,
        "designer": ["Uwe Rosenberg", "Someone Else"],
        "publisher": ["Lookout Games"],
        "possible_counts": [1, 2, 3, 4, 5],
        "playtime_minutes": 120,
        "min_playtime": 30,
        "max_playtime": 150,
    }
    (games_dir / "agricola.yaml").write_text(yaml.dump(game))
    import_from_database(str(games_dir), registry_path, mock_master_csv)
    reg = load_registry(registry_path)
    agricola = next(g for g in reg if g["name"] == "Agricola")
    assert agricola["designer"] == "Uwe Rosenberg, Someone Else"
