import pytest
from scripts.summarize import build_prompt, parse_frontmatter, SYSTEM_PROMPT


SAMPLE_EXTRACTED = """GAME RULES - QE
Players bid on company tiles using dry erase markers.
The highest bidder wins the company.
At the end, the player who spent the most is eliminated.
The remaining player with the most VP wins.
Setup: Deal one nation per player.
Turn: Auctioneer reveals tile, bids publicly, others bid secretly.
Scoring: Companies, nationalization, monopolization, diversification."""


def test_build_prompt_includes_extracted_text():
    prompt = build_prompt(
        extracted_text=SAMPLE_EXTRACTED,
        game_name="QE",
        bgg_id=266830,
        player_count="3-5",
        play_time="45 min",
        designer="Gavin Birnbaum",
    )
    assert "QE" in prompt
    assert "GAME RULES" in prompt
    assert "266830" in prompt


def test_build_prompt_includes_all_sections():
    prompt = build_prompt(
        extracted_text=SAMPLE_EXTRACTED,
        game_name="QE",
        bgg_id=266830,
    )
    for section in ["Overview", "Components", "Setup", "Turn Structure",
                    "Actions", "Scoring / Victory Conditions",
                    "Special Rules & Edge Cases", "Player Reference"]:
        assert section in prompt


def test_build_prompt_includes_rulebook_tags():
    prompt = build_prompt(extracted_text=SAMPLE_EXTRACTED, game_name="QE")
    assert "<rulebook>" in prompt
    assert "</rulebook>" in prompt


def test_system_prompt_exists():
    assert len(SYSTEM_PROMPT) > 100
    assert "precision" in SYSTEM_PROMPT.lower() or "accurate" in SYSTEM_PROMPT.lower()


def test_parse_frontmatter():
    content = """---
title: "QE"
bgg_id: 266830
player_count: "3-5"
---

# QE

## Overview
A bidding game."""
    fm = parse_frontmatter(content)
    assert fm["title"] == "QE"
    assert fm["bgg_id"] == 266830


def test_parse_frontmatter_missing():
    content = "# No frontmatter here"
    fm = parse_frontmatter(content)
    assert fm == {}
