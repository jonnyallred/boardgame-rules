---
title: "Accasta"
bgg_id: 9060
player_count: "2"
play_time: "30-45 min"
designer: "Dieter Stein"
source_pdf: "accasta-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
---

# Accasta

## Overview

Accasta is a pure abstract stacking game for two players on a 37-space hexagonal board. Each player commands 20 pieces of three types (Shields, Horses, Chariots) that move different distances. Players stack pieces on top of each other to capture and control them, aiming to place at least 3 of their own stacks in the opponent's castle (the 9 specially marked home spaces). The game features a unique stack-height limit and the ability to chain multiple moves in a single turn by splitting stacks.

## Components

- 1 Hexagonal board with 37 spaces and 9 castle spaces per side
- 40 Pieces total (20 per player in two colors):
  - Shields (move 1 space)
  - Horses (move up to 2 spaces)
  - Chariots (move up to 3 spaces)

## Setup

Place all 40 pieces in the fixed starting position: each player's 20 pieces are placed on their side of the board on the 9 castle spaces and adjacent spaces. White moves first; players alternate turns. Passing is not allowed.

## Turn Structure

On your turn, you must move at least one piece. You may make multiple moves in a single turn through stack splitting (see Actions). Your turn ends when you either have no more pieces to split off, or when you release an enemy piece.

## Actions

### Movement

All pieces move in a straight line along one of the six hexagonal directions. They cannot change direction during a move and cannot jump over other pieces.

| Piece | Movement Range |
|-------|---------------|
| Shield | Exactly 1 space |
| Horse | Up to 2 spaces |
| Chariot | Up to 3 spaces |

A piece's movement range does not change based on its position in a stack.

### Stacking

Pieces can land on friendly or enemy pieces/stacks, creating stacks. The topmost piece (the "head") dominates the entire stack. All enemy pieces within a stack controlled by your head piece are captured -- their owner cannot access them.

**Stack Height Limit**: A stack may contain **no more than 3 pieces of the same color**. This applies when landing on both friendly and enemy stacks.

### Stack Splitting

When moving, the top piece of a stack can "lead" any number of pieces below it. You can split a stack at any point, moving the top portion (led by the head piece) according to the head piece's movement rules.

### Multiple Moves (Chaining)

When you split a stack and a **friendly** piece is uncovered underneath, that piece may also move on the same turn. This can chain further if more friendly pieces are uncovered. However, if you uncover (release) an **enemy** piece, your turn ends immediately.

### Safe Stacks

A stack containing 3 captured enemy pieces is **invulnerable** -- it cannot be captured again because doing so would violate the 3-pieces-of-same-color rule. Safe stacks are a central tactical element.

### Recapture

By capturing a stack, all previously captured friendly pieces within it are liberated, and all previously dominating enemy pieces become captured.

## Scoring / Victory Conditions

A player wins by controlling at least **3 stacks** in the **enemy's castle** at the **beginning** of their turn. The stacks must be topped by the winning player's pieces.

## Special Rules & Edge Cases

- **No releasing in your own castle**: It is illegal to release (uncover) an enemy piece within your own castle. This prevents both suicide positions and simultaneous victory conditions.
- **Passing is not allowed**: You must make a move on every turn.
- **White moves first**.
- A safe stack in the enemy's castle is extremely strong since it is invulnerable and serves as a stable platform for other pieces to enter.
- The only defense against a safe stack in the castle is to block it with your own pieces.

## Player Reference

### Piece Movement
| Piece | Range | Symbol |
|-------|-------|--------|
| Shield | 1 | S |
| Horse | 1-2 | H |
| Chariot | 1-3 | C |

### Key Rules
- Max 3 same-color pieces in any stack
- Uncovering a friendly piece = continue moving
- Uncovering an enemy piece = turn ends
- Win = 3 stacks in enemy castle at start of your turn
- No releasing enemy pieces in your own castle
