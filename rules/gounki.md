---
title: "Gounki"
bgg_id: 8548
player_count: "2"
play_time: "10-30 min"
designer: "Christophe Malavasi"
source_pdf: "gounki-rules.pdf"
extracted_date: "2026-03-20"
summarized_date: "2026-03-20"
---

## Overview

Gounki is an abstract strategy game for 2 players on an 8x8 board. Each player controls 16 pieces (8 circles and 8 squares). The goal is to be the first player to move one of your pieces beyond the opposite side of the board. Players can stack pieces to form compound pieces that move faster and more flexibly, creating a race-like dynamic where speed and positioning matter more than capturing.

## Components

- 1 standard 8x8 game board
- 16 white pieces (8 circles and 8 squares)
- 16 black pieces (8 circles and 8 squares)

## Setup

1. Each player chooses a color (white or black).
2. Place pieces on the first two rows: squares on dark spaces, circles on light spaces, alternating.
3. White plays first.

## Turn Structure

On each turn, a player selects one piece (simple or compound) and either:
1. **Moves** it according to its movement rules, OR
2. **Deploys** it (splits a compound piece into its simple components)

A player may stack pieces during movement to form compound pieces (max 3 simple pieces per stack).

## Actions

### Movement of Simple Pieces
- **Circle:** Moves 1 step diagonally forward
- **Square:** Moves 1 step forward or sideways (not diagonally, not backward)

### Compound Pieces (Stacks)
Pieces can be stacked during movement (max 3 simple pieces). The stacking order does not matter.

| Compound Piece | Movement |
|---|---|
| Double circle | Like a circle, 1 or 2 steps |
| Double square | Like a square, 1 or 2 steps |
| Square-circle | Like a square OR like a circle (choose one) |
| Triple circle | Like a circle, 1, 2, or 3 steps |
| Triple square | Like a square, 1, 2, or 3 steps |
| Square-square-circle | Like a double square OR like a simple circle |
| Circle-circle-square | Like a double circle OR like a simple square |

**Movement restrictions for compound pieces:**
- Cannot be split during movement (must move as a whole)
- Cannot change direction during movement
- Cannot jump over other pieces

### Deployment
To split a compound piece, "deploy" it by placing each simple piece one at a time onto adjacent spaces according to its normal movement rules.

**Deployment rules:**
- If a compound piece has both circles and squares, deploy all circles first OR all squares first (no alternating)
- Each simple piece is placed according to its normal movement: circles go diagonally forward, squares go forward or sideways
- Multiple circles must be deployed in the same diagonal direction; multiple squares in the same direction
- Cannot deploy over opponent's pieces
- Cannot stop deployment before the piece is fully split
- Can deploy over your own pieces, as long as no resulting stack exceeds 3 simple pieces

### Rebounds
Compound pieces can bounce off the sides of the board during movement or deployment. This is not considered a change of direction. The piece rebounds like a tennis ball off a wall.

### Captures
- Moving onto a space occupied by an opponent's piece (simple or compound) captures and removes it
- Captures can only happen during **movement**, not during deployment
- If all opponent pieces are captured, you win (rare)

## Scoring / Victory Conditions

**Primary win condition:** Be the first player to place one of your pieces beyond the opposite side of the board. A winning deployment ends the instant a piece is placed beyond the board edge.

**Secondary win condition:** Capture all of your opponent's pieces (rare).

## Special Rules & Edge Cases

- You can never move backward (toward your own starting side)
- You can never jump over pieces
- Stacking order within a compound piece has no effect on movement
- A winning deployment ends immediately when a piece crosses the far edge, even if the compound piece is not fully deployed
- During deployment, you cannot pass through spaces occupied by opponent pieces, but you can pass through your own pieces (as long as no stack exceeds 3)
- Rebounds off board edges are allowed and do not count as direction changes

## Player Reference

| Piece | Movement | Steps |
|-------|----------|-------|
| Simple circle | Diagonal forward | 1 |
| Simple square | Forward or sideways | 1 |
| Double circle | Diagonal forward | 1-2 |
| Double square | Forward or sideways | 1-2 |
| Square-circle | Either type | 1 |
| Triple circle | Diagonal forward | 1-3 |
| Triple square | Forward or sideways | 1-3 |
| SSC (2 sq + 1 ci) | Double square OR simple circle | varies |
| CCS (2 ci + 1 sq) | Double circle OR simple square | varies |

**Key rule:** Max 3 simple pieces per compound piece.

**Turn choice:** Move OR Deploy (never both).
