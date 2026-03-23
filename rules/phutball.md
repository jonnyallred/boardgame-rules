---
title: "Phutball"
bgg_id: 25433
player_count: "2"
play_time: "30 minutes"
designer: "Elwyn Berlekamp, John Horton Conway, Richard K. Guy"
source_pdf: ""
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

## Overview

Phutball (Philosopher's Football) is a two-player abstract strategy game described in "Winning Ways for your Mathematical Plays." Players share a single white stone (the football) and place black stones (men) on a Go-like grid, using the men to jump the football toward the opponent's goal line.

## Components

- 1 board (typically a 19x19 Go board, though a 15x19 grid is also used)
- 1 white stone (the football)
- Unlimited supply of black stones (men)

## Setup

1. Place the football (white stone) on the center intersection of the board.
2. The board starts with no black stones.
3. Determine which player defends which goal line (the two short edges for a 15x19 board, or two opposite edges for a 19x19 board).

## Turn Structure

On your turn, choose one of two actions:
1. **Place a man:** Put a black stone on any empty intersection.
2. **Jump the football:** Make a series of jumps with the football.

You must do one or the other, not both.

## Actions

### Placing a Man
Place one black stone on any vacant intersection. Men belong to neither player; both players share all men on the board.

### Jumping the Football
The football jumps over one or more adjacent men in a straight line (horizontal, vertical, or diagonal) to the first empty intersection beyond them. All jumped men are immediately removed from the board.

- Multiple consecutive jumps are allowed in a single turn (the football can change direction between jumps).
- Each jump must land on an empty intersection.
- All men jumped over in any single straight-line segment are removed before the next jump.
- Jumping is optional; you are never forced to jump.

## Scoring / Victory Conditions

You win by moving the football onto or over your opponent's goal line. The goal lines are the edge rows of the board closest to your opponent.

If the football ends up on the goal line, the player whose goal line it is loses. If the football jumps completely over a goal line, the jumping player wins.

## Special Rules & Edge Cases

- Men are neutral; either player may jump over any men.
- A jump must clear at least one man in a straight line.
- The football can jump over multiple men in a single straight-line jump, as long as it lands on the first empty intersection beyond the group.
- Removed men are returned to the supply and may be placed again.
- There is no limit to the number of men on the board (other than available intersections).
- The game can theoretically be played on any grid size, but 19x19 (Go board) is standard.
- Unlike Go, stones are placed on intersections, not in squares.
- If a player has no legal move, they lose (extremely rare in practice).

## Player Reference

| Turn Option | Description |
|-------------|-------------|
| Place a man | Put 1 black stone on any empty intersection |
| Jump | Move football over men in straight lines; remove jumped men |

**Win:** Get the football onto or past your opponent's goal line.
