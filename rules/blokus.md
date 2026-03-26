---
title: "Blokus"
bgg_id: 2453
player_count: "2-4"
play_time: "20-30 min"
designer: "Bernard Tavitian"
source_pdf: "blokus-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
---

## Overview

Blokus is an abstract territory strategy game where players take turns placing polyomino pieces (shapes made of squares) onto a shared 20x20 grid board. Each player has 21 pieces in their color and tries to place as many of them as possible. The player who places the most squares (or has the fewest remaining) wins.

## Components

- 1 game board (20x20 grid)
- 84 pieces in four colors (red, blue, yellow, green), 21 pieces per color:
  - 1 one-square piece (monomino)
  - 1 two-square piece (domino)
  - 2 three-square pieces (trominoes)
  - 5 four-square pieces (tetrominoes)
  - 12 five-square pieces (pentominoes)

## Setup

1. Each player chooses a color and takes that set of 21 pieces.
2. Choose a player to go first; play proceeds clockwise around the board.

## Turn Structure

On each turn, a player places exactly one piece on the board following the placement rules. If a player cannot legally place any piece, they must pass their turn. Play continues clockwise until no player can place any more pieces.

## Actions

**Place a Piece:**

- Place one of your 21 pieces onto the board.
- **First piece:** The first piece played by each player must cover one of the four corner squares of the board.
- **Subsequent pieces:** Each new piece must touch at least one other piece of the same color, but **only at the corners** (diagonal contact).
- **Same-color restriction:** Pieces of the same color can **never** touch along a side (edge-to-edge).
- **Different-color contact:** There are no restrictions on how pieces of different colors may contact each other.
- Once a piece has been placed on the board, it cannot be moved.

**Pass:**

- If you cannot legally place any of your remaining pieces, you must pass your turn.

## Scoring / Victory Conditions

**Game End:** The game ends when no player can place any more pieces.

### Basic Scoring

Each player counts the number of unit squares in their remaining (unplaced) pieces. The player with the **lowest** number of remaining squares wins.

### Advanced Scoring

Players compete for the **highest** score:

- Each remaining square = **-1 point**
- If a player places **all 21 pieces**: **+15 points**
- If the **last piece placed** was the 1-square piece: **+5 additional bonus points** (total +20 if all placed and monomino was last)

| Scenario | Score |
|---|---|
| All pieces placed, monomino last | +20 points |
| All pieces placed, monomino not last | +15 points |
| 8 squares remaining | -8 points |
| 24 squares remaining | -24 points |

## Special Rules & Edge Cases

### Two-Player Variant
- One player controls blue and red; the other controls yellow and green.
- Playing order: blue, yellow, red, green (alternating between the two players).
- At game end, each player calculates their score by combining both of their colors.

### Three-Player Variant
- Each player chooses one color.
- The fourth (remaining) color is shared and played alternately by each player in turn.
- Playing order: blue, yellow, red, green.
- Final scores are calculated the same way as the standard 4-player game; the shared color's score is ignored.

### Key Clarifications
- Corner contact is required between same-color pieces — you cannot place a piece of your color that has no diagonal connection to one of your existing pieces (except your first piece).
- Pieces of different colors may freely touch along sides or corners.
- A player who passes may resume playing on a later turn if a legal placement becomes available (though this is rare).

## Player Reference

| Piece Type | Count per Player | Squares per Piece | Total Squares |
|---|---|---|---|
| Monomino (1-square) | 1 | 1 | 1 |
| Domino (2-square) | 1 | 2 | 2 |
| Trominoes (3-square) | 2 | 3 | 6 |
| Tetrominoes (4-square) | 5 | 4 | 20 |
| Pentominoes (5-square) | 12 | 5 | 60 |
| **Total** | **21** | — | **89** |

**Quick Rules Reminder:**
1. First piece covers a board corner
2. Each new piece must touch your own color diagonally (corner-to-corner)
3. Same color pieces never touch edge-to-edge
4. Pass if you cannot place; game ends when nobody can place
5. Fewest remaining squares wins (basic) or highest score wins (advanced)
