---
title: "Renju"
bgg_id: 11930
player_count: "2"
play_time: "15-45 min"
designer: "Traditional"
source_pdf: "renju-rules.pdf"
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

# Renju

## Overview

Renju is a professional variant of the abstract strategy game Gomoku, played on a 15x15 gridded board (same as a Go board). Two players take turns placing black and white stones on the intersections of the grid lines. The objective is to get exactly 5 of your stones in an unbroken row (horizontally, vertically, or diagonally). Renju differs from Gomoku by imposing restrictions on Black (the first player) to compensate for Black's inherent first-move advantage. These restrictions create a strategically deep and balanced competitive game.

## Components

- 1 Board with 15x15 grid lines (225 intersections)
- Black stones (sufficient supply)
- White stones (sufficient supply)

## Setup

1. Place the empty board between the two players.
2. One player takes Black, the other takes White.
3. Black always moves first.
4. **Black's first stone must be placed on the center intersection of the board.**

## Turn Structure

Players alternate turns:

1. **Black's Turn:** Place one black stone on any empty intersection, subject to Black's forbidden move restrictions.
2. **White's Turn:** Place one white stone on any empty intersection (no restrictions).

Stones once placed are never moved or removed.

## Actions

- **Place a Stone:** On your turn, place one stone of your color on any empty intersection (subject to restrictions for Black).
- **Pass (optional):** A player may choose to pass their turn. If both players pass consecutively, the game is a draw.

## Scoring / Victory Conditions

- **Win:** A player wins by placing exactly 5 of their stones in an unbroken row (horizontal, vertical, or diagonal).
- **Black's Overline Rule:** If Black creates a row of 6 or more stones, this does NOT count as a win for Black. Overlines are forbidden moves for Black.
- **White's Overline:** White CAN win with 6 or more stones in a row.
- **Draw:** If the board is completely filled with no winner, or if both players pass consecutively, the game is a draw.

## Special Rules & Edge Cases

### Forbidden Moves (Black Only)

Black cannot play a stone that creates any of the following:

| Forbidden Pattern | Description |
|---|---|
| **3x3 Fork** | Creating two simultaneous open threes (threes with both ends unblocked) |
| **4x4 Fork** | Creating two simultaneous fours (rows of 4 threatening to complete 5) |
| **Overline** | Creating 6 or more stones in a row |

- **4x3 Fork (Legal):** Black CAN create a fork with one four and one open three simultaneously. This is Black's primary winning tactic.
- **White has NO forbidden moves.** White can freely create any pattern, including overlines.
- **Forbidden Move = Loss:** If Black plays a stone that creates a forbidden pattern, Black loses the game immediately.

### Key Tactical Concepts

- **Open Three:** Three stones in a row with both ends unblocked, threatening to become an open four.
- **Four:** Four stones in a row with at least one end open, threatening to complete five on the next move.
- **Open Four:** Four stones in a row with both ends open; this is unstoppable (opponent can only block one end).
- **VCF (Victory by Continuous Fours):** A sequence of forcing moves using consecutive fours to create an unstoppable winning line.

### Opening Rules (Tournament Play)

Tournament Renju uses specific opening rules to further balance the game:
- The first three moves may follow prescribed patterns.
- After the opening, the players may swap colors.
- Various opening protocols exist (Soosyrv, Taraguchi, etc.) to ensure fairness.

## Player Reference

| Concept | Black | White |
|---|---|---|
| First Move | Center of board (mandatory) | N/A |
| Win Condition | Exactly 5 in a row | 5 or more in a row |
| 3x3 Fork | FORBIDDEN | Allowed |
| 4x4 Fork | FORBIDDEN | Allowed |
| Overline (6+) | FORBIDDEN | Allowed (can win) |
| 4x3 Fork | ALLOWED (key tactic) | Allowed |
