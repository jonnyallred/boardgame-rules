---
title: "Proteus"
bgg_id: 2211
player_count: "2"
play_time: "20-40 minutes"
designer: "Francis Lalumiere"
source_pdf: "proteus-rules.pdf"
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

## Overview

Proteus is a two-player abstract strategy game played on a standard chessboard using six-sided dice as pieces. Each face of a die shows a different chess piece, and the piece shown on top determines how that die moves. After moving one die, a player must rotate a different die one step up or down, transforming it into a stronger or weaker piece. More powerful pieces are worth more points when captured.

## Components

- 16 Proteus dice (8 per player, white and black)
- 1 standard chessboard

## Setup

1. Decide who plays white and who plays black.
2. Each die starts as a pawn (pawn face up).
3. Each player places their 8 dice on the 8 black squares closest to them.

## Turn Structure

White moves first. Turns alternate. On each turn, a player must:
1. **Move** one die (according to the piece shown on its top face).
2. **Rotate** a different die one step up or down in the piece hierarchy.

A player who cannot move any of their dice loses the game, regardless of points.

## Actions

### Moving a Die
Each die moves according to its current identity (the face shown on top):

| Piece | Movement | Point Value |
|-------|----------|-------------|
| Pyramid | Cannot move or be captured | - |
| Pawn | 1 space forward; captures diagonally forward. Can move 2 spaces forward from starting squares | 2 |
| Bishop | Any distance diagonally | 3 |
| Knight | L-shape (2+1), jumps over pieces | 4 |
| Rook | Any distance horizontally or vertically | 5 |
| Queen | Any distance in any direction (horizontal, vertical, or diagonal) | 6 |

- There is no King piece. The game is won by points, not checkmate.
- Pawns do NOT capture en passant.
- Pawns reaching the opposite edge do NOT promote.
- Only Knights can jump over Pyramids.

### Rotating a Die
After moving, you must rotate a **different** die one step up or down:
- Pyramid <-> Pawn <-> Bishop <-> Knight <-> Rook <-> Queen
- A Pyramid cannot be rotated down; a Queen cannot be rotated up.

### Capturing
A piece is captured when an opposing piece moves to its square.

**Queen Backstabbing:** The Queen can also be captured by moving a piece to the square directly behind her (between the Queen and her own first rank). A Queen on her own first rank cannot be backstabbed. Backstabbing only occurs when an opposing piece actively moves to the back square, not when pieces happen to already occupy that position.

### Trade-Off
Instead of moving, a player may perform a **double rotation** -- rotate one piece two steps up or two steps down. The target piece must be able to complete the full 2-step rotation (e.g., a Rook cannot be double-rotated up because it is only one step from Queen).

## Scoring / Victory Conditions

The game ends when one player has only one die remaining. Both players sum the point values of captured pieces.

| Piece | Points |
|-------|--------|
| Pawn | 2 |
| Bishop | 3 |
| Knight | 4 |
| Rook | 5 |
| Queen | 6 |
| Pyramid | Cannot be captured |

The player with the most points wins. If a player cannot move any die, they lose immediately regardless of points.

## Special Rules & Edge Cases

- You must move one die and rotate a **different** die each turn (never the same die).
- Pyramids are purely defensive: they cannot move, cannot be captured, and cannot be rotated down.
- You can rotate a doomed piece down to give your opponent fewer points when they capture it.
- Rotating a Pawn down to Pyramid makes it uncapturable.
- Captured pieces are set aside. Do not accidentally rotate them.

### Variants
- **Russian Roulette:** After capturing, the capturing piece is rolled randomly to a new face.
- **Wall Street:** Players start with a 20-point budget to buy starting pieces instead of all pawns.
- **Polarity:** Odd pieces (Bishop, Rook) can only capture even pieces (Pawn, Knight, Queen) and vice versa.
- **Warhorses:** Knight and Bishop swap positions in the rotation sequence (Knight = 3 pts, Bishop = 4 pts).

## Player Reference

| Rotation Sequence (low to high) | Points |
|--------------------------------|--------|
| Pyramid | 0 (uncapturable) |
| Pawn | 2 |
| Bishop | 3 |
| Knight | 4 |
| Rook | 5 |
| Queen | 6 |

**Turn:** Move 1 die + Rotate 1 different die (or Trade-Off: double-rotate instead of moving).
