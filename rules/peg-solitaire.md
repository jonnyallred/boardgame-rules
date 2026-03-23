---
title: "Peg Solitaire"
bgg_id: 13713
player_count: "1"
play_time: "10-30 minutes"
designer: "Uncredited (traditional)"
source_pdf: ""
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

## Overview

Peg Solitaire is a single-player board puzzle. The standard English board has 33 holes arranged in a cross shape. The objective is to remove all pegs except one, ideally leaving the final peg in the center hole.

## Components

- 1 board with 33 holes (cross-shaped: 3x3 center with four 2x3 extensions)
- 32 pegs

## Setup

1. Fill every hole with a peg except the center hole, which remains empty.

## Turn Structure

On each move:
1. Choose a peg that can jump over an adjacent peg (horizontally or vertically) into an empty hole directly beyond it.
2. Remove the jumped peg from the board.
3. Continue making moves until no more valid jumps exist.

## Actions

| Action | Rules |
|--------|-------|
| Jump | A peg jumps over one adjacent peg into an empty hole beyond it |
| Direction | Horizontal or vertical only (no diagonal jumps) |
| Removal | The jumped-over peg is removed from the board |

Multiple jumps with the same peg in sequence are allowed (like checkers) but each jump is a separate move decision.

## Scoring / Victory Conditions

- **Perfect solution:** 1 peg remaining in the center hole -- "genius" level
- **Good solution:** 1 peg remaining in any hole
- **Partial success:** 2-3 pegs remaining
- **Poor result:** 4+ pegs remaining

## Special Rules & Edge Cases

- Diagonal jumps are never allowed.
- Each jump must go exactly 2 holes (over one peg into one empty hole).
- The jumped peg must be immediately adjacent (no gaps).
- Chain jumps with a single peg are common and encouraged but not required.
- The French board variant uses 37 holes in a different pattern.
- Triangle Peg Solitaire is a different game using a triangular board with 15 holes and allows diagonal jumps.

## Player Reference

| Start | 32 pegs, center hole empty |
|-------|---------------------------|
| Move | Jump over adjacent peg into empty hole; remove jumped peg |
| Goal | 1 peg remaining (ideally in center) |
| No move | Game ends when no valid jumps remain |
