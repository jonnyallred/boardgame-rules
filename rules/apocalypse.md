---
title: "Apocalypse"
bgg_id: 2574
player_count: "2"
play_time: "15 min"
designer: "C.S. Elliott"
source_pdf: ""
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
---

## Overview

Apocalypse is a chess variant for 2 players invented by C.S. Elliott in 1976. It is played on a 5x5 board with simultaneous secret moves. Each player controls 2 Horsemen (knights) and 5 Footmen (pawns). The goal is to eliminate all of the opponent's Footmen. The simultaneous movement creates unique tactical and psychological tension not found in standard chess.

## Components

- 1 board (5x5 grid)
- 10 White pieces: 2 Horsemen, 5 Footmen
- 10 Black pieces: 2 Horsemen, 5 Footmen
- Paper and pen for writing secret moves

## Setup

Arrange pieces on the 5x5 board:

**White (rows 1-2):**
- Row 1: Horseman, Footman, Footman, Footman, Horseman
- Row 2: Footman, Footman, empty, empty, empty

Wait -- the standard layout is:
- Row 1 (White's back rank): Horseman on a1, Footman on b1, Footman on c1, Footman on d1, Horseman on e1
- Row 2 (White's front rank): Footman on a2, Footman on b2, Footman on c2, Footman on d2, Footman on e2

**Black (rows 4-5), mirrored:**
- Row 5 (Black's back rank): Horseman on a5, Footman on b5, Footman on c5, Footman on d5, Horseman on e5
- Row 4 (Black's front rank): Footman on a4, Footman on b4, Footman on c4, Footman on d4, Footman on e4

## Turn Structure

Both players act simultaneously each turn:

1. **Secret Move:** Both players secretly write down one move for one of their pieces.
2. **Reveal:** Both moves are revealed simultaneously.
3. **Resolve:** Execute both moves, resolving any conflicts according to the collision rules.

## Actions

**Horseman Movement:** Moves exactly like a knight in chess (L-shape: 2 squares in one direction, 1 square perpendicular). Can jump over other pieces.

**Footman Movement:** Moves like a pawn in chess with these modifications:
- Moves 1 square forward (toward opponent's side). No initial double-step.
- Captures diagonally forward 1 square.
- No en passant (since there is no double-step).

**Collision Resolution (when both pieces move to the same square):**
- Horseman vs. Footman: The Horseman captures the Footman.
- Horseman vs. Horseman: Both pieces are eliminated.
- Footman vs. Footman: Both pieces are eliminated.

**Footman Capture of Vacated Square:** If a Footman attempts to capture diagonally but the target piece moved away, the Footman's move is still executed as a diagonal non-capturing move to that square.

**Promotion:** When a Footman reaches the opponent's back rank, it is promoted to a Horseman -- but only if the player currently has fewer than 2 Horsemen on the board. If the player already has 2 Horsemen, the Footman remains a Footman on the last rank.

## Scoring / Victory Conditions

**Win by Elimination:** The first player to capture all 5 of the opponent's Footmen wins.

**Win by Penalty:** If a player accumulates 2 penalty points, they lose immediately.

**Draw:** If both players' last Footmen are eliminated simultaneously, the game is a draw.

## Special Rules & Edge Cases

- **Illegal Moves:** If a player writes an illegal move (e.g., moving a captured piece, moving off the board, or making an impossible move), they receive 1 penalty point. Their piece does not move. Two penalty points = immediate loss.
- **No Move Available:** If a player has no legal move, they must pass (write "pass"). This does not incur a penalty.
- **Simultaneous Elimination:** If both players lose their last Footman on the same turn, the game is a draw.
- **Horseman Stalemate:** Horsemen alone cannot win -- you need to eliminate all opposing Footmen. Horsemen capturing Horsemen does not affect the win condition directly.

## Player Reference

| Piece | Movement | Capture |
|-------|----------|---------|
| Horseman | L-shape (as chess knight) | Same as movement |
| Footman | 1 square forward | 1 square diagonally forward |

| Collision (same square) | Result |
|------------------------|--------|
| Horseman vs. Footman | Horseman wins |
| Same type vs. same type | Both eliminated |

| Condition | Result |
|-----------|--------|
| All enemy Footmen captured | You win |
| 2 penalty points | You lose |
| Simultaneous last Footman loss | Draw |

| Promotion | Footman reaching back rank becomes Horseman (if fewer than 2 Horsemen on board) |
|-----------|---|
