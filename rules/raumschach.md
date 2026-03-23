---
title: "Raumschach"
bgg_id: 34848
player_count: "2"
play_time: "30-90 min"
designer: "Ferdinand Maack"
source_pdf: "raumschach-rules.pdf"
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

# Raumschach

## Overview

Raumschach (German for "Space Chess") is one of the first three-dimensional chess variants, invented by Dr. Ferdinand Maack in 1907. It is played on a 5x5x5 cubic board (125 cells), arranged as five stacked 5x5 levels. Each player commands a full army including standard chess pieces plus two Unicorns, a piece unique to 3D chess that moves along space diagonals. The game follows standard chess objectives: checkmate the opponent's King.

## Components

- 1 Raumschach board: five 5x5 levels stacked vertically (levels labeled A through E from bottom to top)
- White pieces (20): 1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, 2 Unicorns, 10 Pawns
- Black pieces (20): 1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, 2 Unicorns, 10 Pawns

## Setup

**White** starts on levels A and B (bottom two levels):
- Level A (rank 1): Rook, Knight, King, Knight, Rook; (rank 2): 5 Pawns
- Level B (rank 1): Bishop, Unicorn, Queen, Unicorn, Bishop; (rank 2): 5 Pawns

**Black** starts on levels D and E (top two levels), mirrored:
- Level E (rank 5): Rook, Knight, King, Knight, Rook; (rank 4): 5 Pawns
- Level D (rank 5): Bishop, Unicorn, Queen, Unicorn, Bishop; (rank 4): 5 Pawns

White moves first.

## Turn Structure

Players alternate turns. On each turn, a player moves one piece according to its movement rules. Capturing is performed by moving onto a cell occupied by an opponent's piece.

## Actions

### Piece Movement Rules

| Piece | Movement |
|---|---|
| **Rook** | Moves any number of cells along a file, rank, or column (orthogonal movement through any single axis) |
| **Bishop** | Moves any number of cells diagonally in any coordinate plane (2D diagonal movement) |
| **Unicorn** | Moves any number of cells along space diagonals (3D diagonal, through corners of cells) |
| **Queen** | Combines Rook + Bishop + Unicorn movement (all directions) |
| **King** | Moves one cell in any direction the Queen could move |
| **Knight** | Moves as in standard chess: one cell orthogonally then one cell diagonally outward, always in the same coordinate plane. Can jump over pieces. |
| **Pawn** | Moves one cell forward (toward opponent's side) along rank or vertically between levels. Captures one cell forward-diagonally. |

### Pawn Details
- **No initial two-step move.** Pawns always move exactly one cell.
- **No en passant** (since there is no two-step move).
- **Promotion:** White Pawns promote upon reaching rank 5 of level A or B. Black Pawns promote upon reaching rank 1 of level D or E.
- Pawns promote to any piece except King.

## Scoring / Victory Conditions

- **Checkmate:** The game is won by placing the opponent's King in checkmate (the King is in check and cannot escape).
- **Stalemate:** If a player has no legal moves and is not in check, the game is a draw.
- **Draw:** By agreement, threefold repetition, or 50-move rule (as in standard chess).

## Special Rules & Edge Cases

- **No Castling:** There is no castling move in Raumschach.
- **Unicorn Color Binding:** The Unicorn is bound to cells of one "color" in 3D space (analogous to the Bishop's binding in 2D chess). Each player starts with one Unicorn on each "color."
- **Increased King Mobility:** The King can potentially move to up to 26 adjacent cells (vs. 8 in standard chess), making checkmate more difficult to achieve.
- **Knight Power:** The 3D Knight is significantly more powerful than in standard chess due to additional move options across levels.
- **Notation:** Cells are denoted by level letter + file letter + rank number (e.g., Ac3 = level A, file c, rank 3).

## Player Reference

| Piece | Directions | Range |
|---|---|---|
| Rook | Orthogonal (3 axes) | Unlimited |
| Bishop | 2D Diagonal (3 planes) | Unlimited |
| Unicorn | 3D Diagonal (4 diagonals) | Unlimited |
| Queen | All of the above | Unlimited |
| King | All of the above | 1 cell |
| Knight | 1 orthogonal + 1 diagonal | Jump |
| Pawn | 1 forward (move), 1 forward-diagonal (capture) | 1 cell |
