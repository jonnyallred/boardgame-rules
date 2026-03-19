---
title: "Chess"
bgg_id: 171
player_count: "2"
play_time: "30-120 min"
source_pdf: "chess-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
---

## Overview

Chess is a two-player abstract strategy game played on an 8x8 board. Each player commands 16 pieces of different types with unique movement abilities. The objective is to checkmate the opponent's king -- placing it under attack with no legal escape. Chess is one of the oldest and most widely played strategy games in the world, governed by FIDE (World Chess Federation) rules.

## Components

- 1 chessboard: 8x8 grid of 64 alternately light ("white") and dark ("black") squares
- 16 white pieces: 1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, 8 Pawns
- 16 black pieces: 1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, 8 Pawns

## Setup

1. Orient the board so each player has a white square in the near-right corner.
2. Place pieces on the two rows closest to each player:
   - **Back row (from left to right):** Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
   - **Front row:** 8 Pawns
   - The Queen goes on the square matching her color (white queen on white square, black queen on black square).
3. White moves first.

## Turn Structure

Players alternate turns. On each turn, a player must make exactly one legal move. A move consists of moving one piece to a different square according to its movement rules, optionally capturing an opponent's piece by moving to its square.

## Actions

### Piece Movement

| Piece | Movement |
|-------|----------|
| **King** | 1 square in any direction (horizontal, vertical, diagonal) |
| **Queen** | Any number of squares along a rank, file, or diagonal (cannot jump) |
| **Rook** | Any number of squares along a rank or file (cannot jump) |
| **Bishop** | Any number of squares along a diagonal (cannot jump) |
| **Knight** | "L-shape": 2 squares in one direction + 1 square perpendicular (CAN jump over pieces) |
| **Pawn** | Forward 1 square (or 2 from starting position); captures diagonally forward 1 square |

### Special Moves

**Castling:** The King moves 2 squares toward a Rook, and the Rook moves to the square the King crossed. Requirements:
- Neither the King nor the chosen Rook has previously moved
- No pieces between the King and the Rook
- The King is not in check, does not pass through check, and does not land in check

**En Passant:** When a pawn advances 2 squares from its starting position and lands beside an opponent's pawn, the opponent may capture it as if it had advanced only 1 square. This capture must be made on the immediately following turn or the right is lost.

**Pawn Promotion:** When a pawn reaches the opposite end of the board (8th rank), it must be immediately replaced by a Queen, Rook, Bishop, or Knight of the same color (player's choice). Promotion to a Queen is most common. The promoted piece takes effect immediately.

### Check and Checkmate

**Check:** The King is under direct attack by an opponent's piece. The player in check MUST resolve the check on their turn by:
- Moving the King to a safe square
- Blocking the attack with another piece
- Capturing the attacking piece

**Checkmate:** The King is in check and no legal move can resolve it. The game is over; the checkmating player wins.

## Scoring / Victory Conditions

**Win:** Checkmate the opponent's King, or the opponent resigns.

**Draw:** The game is drawn if:
- **Stalemate:** The player to move has no legal moves and is NOT in check.
- **Insufficient material:** Neither player has enough pieces to checkmate (e.g., King vs. King, King+Bishop vs. King).
- **Threefold repetition:** The same position occurs 3 times with the same player to move.
- **50-move rule:** 50 consecutive moves by each player without a pawn move or capture.
- **Agreement:** Both players agree to a draw.

In tournament play: Win = 1 point, Draw = 0.5 points, Loss = 0 points.

## Special Rules & Edge Cases

- You may never make a move that leaves your own King in check.
- A piece is considered to attack a square even if moving there would expose its own King.
- A pawn promoting to a second Queen (or other piece) is legal even if that piece was not previously captured.
- Castling is a single King move, not a Rook move. You must move the King first.
- You cannot castle out of check, through check, or into check.
- En passant capture is only available on the turn immediately after the opponent's two-square pawn advance.
- Touch-move rule (tournament play): If you touch a piece, you must move it if legal.
- If no legal move is available and the King is not in check, it is stalemate (draw), not a loss.

## Player Reference

**Piece values (approximate):**

| Piece | Value |
|-------|-------|
| Pawn | 1 |
| Knight | 3 |
| Bishop | 3 |
| Rook | 5 |
| Queen | 9 |
| King | N/A (invaluable) |

**Setup reminder:** White square in near-right corner. Queen on her own color.

**Checkmate = Win. Stalemate = Draw.**

**Special moves:** Castling (King+Rook), En Passant (Pawn), Promotion (Pawn reaches 8th rank).
