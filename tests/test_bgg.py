import pytest
from unittest.mock import patch, MagicMock
from scripts.bgg import search_game, get_game_details, parse_search_results, parse_game_details
from scripts.find_rulebook import should_skip_existing

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


def test_should_skip_existing_only_for_terminal_statuses():
    assert should_skip_existing(None) is False
    assert should_skip_existing({"status": "pending"}) is False
    assert should_skip_existing({"status": "queued"}) is False
    assert should_skip_existing({"status": "not_found"}) is False
    assert should_skip_existing({"status": "downloaded"}) is True
