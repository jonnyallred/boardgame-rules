import pytest
from pathlib import Path
from scripts.quality_check import check_quality, check_batch, QualityResult

GOOD_RULES = """---
title: "QE"
bgg_id: 266830
player_count: "3-5"
play_time: "45 min"
designer: "Gavin Birnbaum"
extracted_date: "2026-03-04"
summarized_date: "2026-03-04"
---

# QE

## Overview
QE is a sealed-bid auction game where players represent central banks bidding
to bail out companies. The highest spender is eliminated. Among surviving
players, the one with the most victory points wins. Players can bid any amount
they want without limit.

## Components
- 21 Company Tiles with nation, industry, and VP value
- 5 Bid Tiles (dry erase) for writing bids secretly
- 5 Player Score Boards for tracking scoring categories
- 5 Dry Erase Markers for writing bids
- 1 First Auctioneer Token to track rounds

## Setup
Assign nations to each player and give them a bid tile. Deal hidden industry
tokens randomly. Remove company tiles based on player count as specified
in the rulebook. Shuffle remaining tiles face down.

## Turn Structure
Each turn has 5 phases: Opening Bid where auctioneer reveals and bids,
Secret Bids where others bid secretly, Award Company to highest bidder,
Zero Bid VP for players who bid zero, and End of Sale rotating auctioneer.

## Actions
The core action is bidding on company tiles. Bids must be positive whole
numbers except non-auctioneers may bid zero. The auctioneer bids publicly
while other players bid secretly. There is no upper limit on bids.

## Scoring / Victory Conditions
Players add up all spending on company tiles. The highest spender is
eliminated from the game. Remaining players score VP from companies owned,
zero bids earned, nationalization bonuses, monopolization, and diversification.

## Special Rules & Edge Cases
Tied auctions trigger rebids up to 3 times before highest non-tied bid wins.
In 3-player games the last tile has no auctioneer. In 5-player games each
player may peek at one winning bid per game. Zero bid VP is skipped in 3p.

## Player Reference
| Category | Scoring |
|---|---|
| Elimination | Highest spender eliminated |
| Least Spent | 7 VP (3-4p) / 6 VP (5p) |
| Companies | Face value on tiles |
| Nationalization | 1/3/6/10 VP |
"""

SHORT_SECTION_RULES = """---
title: "QE"
bgg_id: 266830
---

# QE

## Overview
A game.

## Components
Tiles.

## Setup
Set up.

## Turn Structure
Take turns.

## Actions
Bid.

## Scoring / Victory Conditions
Score points.

## Special Rules & Edge Cases
None.

## Player Reference
See rules.
"""


def test_good_rules_pass(tmp_path):
    path = tmp_path / "qe.md"
    path.write_text(GOOD_RULES)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("QE rules text about bidding and companies and auctions " * 100)
    result = check_quality(str(path), str(extracted))
    assert result.passed is True
    assert len(result.issues) == 0


def test_short_sections_flagged(tmp_path):
    path = tmp_path / "qe.md"
    path.write_text(SHORT_SECTION_RULES)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("Some rules text " * 200)
    result = check_quality(str(path), str(extracted))
    assert result.passed is False
    assert any("thin" in issue.lower() or "short" in issue.lower() for issue in result.issues)


def test_short_extracted_text_flagged(tmp_path):
    path = tmp_path / "qe.md"
    path.write_text(GOOD_RULES)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("Very short text")
    result = check_quality(str(path), str(extracted))
    assert result.passed is False
    assert any("extracted" in issue.lower() for issue in result.issues)


def test_missing_sections_flagged(tmp_path):
    path = tmp_path / "qe.md"
    content = GOOD_RULES.replace("## Player Reference", "").replace("| Category", "").replace("|---|---|", "").replace("| Elimination", "").replace("| Least Spent", "").replace("| Companies", "").replace("| Nationalization", "")
    path.write_text(content)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("Rules text " * 200)
    result = check_quality(str(path), str(extracted))
    assert result.passed is False
    assert any("Player Reference" in issue for issue in result.issues)


def test_uncertainty_phrases_flagged(tmp_path):
    path = tmp_path / "qe.md"
    uncertain = GOOD_RULES.replace("Players can bid any amount", "It is unclear from the text how much players can bid")
    path.write_text(uncertain)
    extracted = tmp_path / "qe-rules.txt"
    extracted.write_text("Rules text " * 200)
    result = check_quality(str(path), str(extracted))
    assert result.passed is False
    assert any("unclear" in issue.lower() for issue in result.issues)


def test_check_batch_honors_limit(tmp_path):
    registry_path = tmp_path / "games.yaml"
    registry_path.write_text(
        """games:
  - name: Game One
    bgg_id: 1
    status: summarized
  - name: Game Two
    bgg_id: 2
    status: summarized
"""
    )

    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    extracted_dir = tmp_path / "extracted"
    extracted_dir.mkdir()

    for slug in ("game-one", "game-two"):
        (rules_dir / f"{slug}.md").write_text(GOOD_RULES.replace("QE", slug))
        (extracted_dir / f"{slug}-rules.txt").write_text("Rules text " * 300)

    stats = check_batch(
        str(registry_path),
        rules_dir=str(rules_dir),
        extracted_dir=str(extracted_dir),
        limit=1,
    )

    assert stats["validated"] == 1
