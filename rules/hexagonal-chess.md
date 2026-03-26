---
title: "Hexagonal Chess"
bgg_id: 19432
player_count: "2"
play_time: "30-60 min"
designer: "Wladyslaw Glinski"
source_pdf: "hexagonal-chess-rules.pdf"
extracted_date: "2026-03-20"
summarized_date: "2026-03-20"
---

## Overview

Hexagonal Chess (Glinski's variant) is a chess variant invented in 1936 by Wladyslaw Glinski, played on a hexagonal board of 91 hexagonal cells in three colors. Each player commands a King, Queen, 3 Bishops, 2 Knights, 2 Rooks, and 9 Pawns. The game adapts standard chess principles to hexagonal geometry, creating new movement patterns and tactical possibilities. It is the most widely played hexagonal chess variant, popular particularly in Eastern Europe.

## Components

- 1 hexagonal board with 91 hexagonal cells in 3 colors (31 of one color, 30 each of the other two)
- 18 White pieces: 1 King, 1 Queen, 3 Bishops, 2 Knights, 2 Rooks, 9 Pawns
- 18 Black pieces: 1 King, 1 Queen, 3 Bishops, 2 Knights, 2 Rooks, 9 Pawns

## Setup

The board is oriented so that one vertex points toward each player. The board has 11 files (columns) running from one player to the other, with file lengths varying from 6 to 11 hexagons.

**White starting position (bottom vertex side):**
- King on f1, Queen on e1
- Bishops on f2, e2, d2 (one on each color)
- Knights on d1 and g1
- Rooks on c1 and h1
- Pawns on b1, c2, d3, e3, f3, g3, h2, i1, and one additional pawn forming a row

**Black starting position (top vertex side):** Mirror of White's setup on the opposite side of the board.

Each bishop starts on a different colored hexagon, ensuring all three board colors are covered.

## Turn Structure

Players alternate turns, starting with White. On each turn, a player must move one of their pieces. Standard chess conventions apply: you must move (no passing), and the game continues until checkmate, stalemate, or an agreed draw.

## Actions

### Piece Movement

On a hexagonal board, each cell has 6 adjacent cells (orthogonal directions) and 6 diagonal directions (lines connecting cells of the same color). Pieces move as follows:

**King:** Moves one space in any direction — the 6 orthogonal directions and the 6 diagonal directions (12 possible moves from the center). The King may not move into check.

**Queen:** Moves any number of unoccupied spaces in any orthogonal or diagonal direction (combines Rook and Bishop movement). From the center of the board, the Queen can reach up to 42 hexagons.

**Rook:** Moves any number of unoccupied spaces along the 6 orthogonal directions (straight lines crossing cell edges). Rooks move along lines where the cells alternate between all three colors.

**Bishop:** Moves any number of unoccupied spaces along the 6 diagonal directions (lines connecting cells of the same color). Each Bishop stays on its starting color for the entire game. This is why each player has 3 Bishops — one for each color.

**Knight:** Moves in an "L-shape" adapted to the hex grid: two steps in one orthogonal direction, then one step in an adjacent orthogonal direction (turning 60 degrees). The Knight jumps over intervening pieces. From most positions, a Knight has up to 12 possible destination cells (compared to 8 in standard chess).

**Pawn:** Moves forward toward the opponent's side of the board (along the file). A Pawn moves one space straight forward (orthogonally toward the opponent). From its starting position, a Pawn may advance two spaces forward. Pawns capture one space diagonally forward (to an adjacent cell in one of the two forward-diagonal directions, which in hexagonal terms are the forward rook-directions on either side).

### Capturing
A piece captures by moving to a space occupied by an opponent's piece, removing it from the board. All pieces capture the same way they move, except Pawns (which capture diagonally forward, not straight forward).

### Pawn Promotion
A Pawn that reaches any cell on the far two edges of the board (the hexagons at the opponent's end with no further forward movement possible) is promoted. The player replaces the Pawn with a Queen, Rook, Bishop, or Knight of the same color.

### En Passant
When a Pawn advances two spaces from its starting position and lands beside an opponent's Pawn that could have captured it had it moved only one space, the opponent may capture it en passant on the immediately following turn, moving their Pawn to the space the captured Pawn passed through.

### Check and Checkmate
**Check:** When a King is threatened by an opponent's piece, it is in check. The player must escape check on their next move by moving the King, blocking the attack, or capturing the attacking piece.

**Checkmate:** If a player's King is in check and there is no legal move to escape, the game is over. The player delivering checkmate wins.

## Scoring / Victory Conditions

- **Checkmate:** The player who checkmates the opponent's King wins.
- **Resignation:** A player may resign at any time, conceding the game.
- **Stalemate:** If a player has no legal moves and is NOT in check, the game is a stalemate. Under Glinski's original rules, the player who delivers stalemate receives 3/4 of a point and the stalemated player receives 1/4. Under modern convention, stalemate is typically scored as a draw (1/2 point each).
- **Draw:** By mutual agreement, threefold repetition, or 50-move rule (adapted from standard chess).

## Special Rules & Edge Cases

- **No castling.** Unlike standard chess, there is no castling move in hexagonal chess.
- **Three Bishops:** Each player has 3 Bishops (one per cell color) instead of the standard 2. This ensures all cells on the board can be reached by a Bishop.
- **Pawn initial double-move:** Each Pawn may move two spaces forward only from its initial starting position, never after it has moved.
- **Board geometry:** The hexagonal board creates different tactical properties than a square board. Pieces generally have greater mobility (e.g., Queen reaches 42 cells from center vs. 27 on a standard board). Knights have up to 12 possible moves instead of 8.
- **Color binding:** Bishops are strictly color-bound, just as in standard chess. With 3 colors on the hex board, 3 Bishops are needed for full coverage.
- **Stalemate scoring:** Glinski's original scoring for stalemate (3/4 vs 1/4) differs from standard chess draws. Check which convention is being used before play.

## Player Reference

| Piece | Quantity | Movement |
|-------|----------|----------|
| King | 1 | 1 space in any of 12 directions |
| Queen | 1 | Any distance, any direction (orthogonal + diagonal) |
| Rook | 2 | Any distance, orthogonal (6 directions) |
| Bishop | 3 | Any distance, diagonal (6 directions, color-bound) |
| Knight | 2 | L-shape hop (up to 12 destinations) |
| Pawn | 9 | 1 forward (2 from start), captures diagonally forward |

**No castling. Three Bishops per side. 91-cell hexagonal board.**

**Win:** Checkmate the opponent's King
