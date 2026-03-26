---
title: "Coerceo"
bgg_id: 84783
player_count: "2"
play_time: "20-40 min"
designer: "Mark Steere"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
---

## Overview

Coerceo is an abstract strategy game for two players on a modular hexagonal board. Players move their pieces around the board trying to capture opponents' pieces by enclosure. As the game progresses, the board shrinks — any unoccupied hexagonal tile with three or more open edges is removed, constantly changing the topology of the playing field. The combination of capture by enclosure and a shrinking board creates a dynamic, tactical game.

## Components

- 19 hexagonal tiles (forming the modular board)
- 24 pieces per player (2 colors), tetrahedral shaped
- Each hexagonal tile has 6 triangular cells

## Setup

1. Arrange the 19 hexagonal tiles in the standard configuration to form the board.
2. Each player places their 24 pieces on alternating triangular cells in a checkerboard-like pattern. One player occupies one set of cells, the opponent the other set.
3. Choose who goes first (the first player plays with a slight disadvantage in tournament play, so the pie rule may be used).

## Turn Structure

On your turn, perform exactly one action: either move a piece or spend two captured tiles to remove an enemy piece.

## Actions

### Move
- Move one of your pieces to an adjacent empty triangular cell. Pieces move along edges of the triangular grid (each cell has up to 3 adjacent cells).
- After moving, check for captures and tile removal.

### Capture by Enclosure
- If, after your move, any group of your opponent's pieces is completely enclosed (surrounded with no empty adjacent cells and no path to open space), all pieces in that enclosed group are captured and removed from the board.
- Captured pieces are kept by the capturing player as "conquered tiles."

### Tile Removal (Board Shrinking)
- After each move (and any captures), check all hexagonal tiles. Any tile that has 3 or more open edges (edges not shared with another tile) **and** contains no pieces from either player is removed from the game.
- This causes the board to shrink over time, forcing pieces closer together.

### Spend Conquered Tiles
- Instead of making a normal move, you may spend 2 previously captured enemy pieces to remove any one enemy piece still on the board. This is an alternative action.

## Scoring / Victory Conditions

- The game ends when one player has lost all their pieces. That player loses.
- **Tournament rule:** The game can also end when a player captures their 6th enemy piece (short game) or 12th enemy piece (standard game). The player who reaches the capture threshold first wins.
- If neither player can make progress, a draw may be declared by mutual agreement.

## Special Rules & Edge Cases

- Board tiles are removed automatically when unoccupied and sufficiently exposed (3+ open edges). Players do not choose which tiles to remove.
- A single move can trigger a chain reaction of tile removals if removing one tile causes adjacent tiles to meet the removal criteria.
- The shrinking board prevents stalemates by constantly reducing available space.
- Pieces cannot jump or move through occupied cells.
- The game has no hidden information and no randomness — it is a pure abstract strategy game.
- Draws are rare due to the shrinking board mechanic but possible through repetition of positions.

## Player Reference

| Move | Move one piece to an adjacent empty cell |
|------|------------------------------------------|
| Capture | Enclose enemy group (no empty adjacent cells/paths) |
| Tile Removal | Unoccupied tiles with 3+ open edges are removed |
| Spend 2 Captures | Remove any 1 enemy piece from the board |
| Win Condition | Eliminate all enemy pieces or reach capture threshold |
