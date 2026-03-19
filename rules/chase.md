---
title: "Chase"
bgg_id: 316
player_count: "2"
play_time: "30-60 min"
designer: "Tom Kruszewski"
source_pdf: "chase-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
---

## Overview

Chase is a two-player abstract strategy game that uses dice as playing pieces, but the dice are never rolled. Instead, a die's top face value represents its speed (movement range). Players capture enemy dice by landing on them by exact count, and when a piece is captured, its speed must be absorbed by the surviving teammates to maintain a constant team total of 25. When a player is reduced to 4 dice, they can no longer maintain the total and lose.

## Components

- 1 hexagonal gameboard (81 hexes) with a central "fission chamber"
- 10 red dice
- 10 blue dice
- Carrying case

## Setup

1. One player takes blue (goes first), the other takes red.
2. Place the board between players with a CHASE logo to each player's left.
3. Each player places 9 dice on their starting positions as depicted in the rulebook, with values summing to 25.
4. Keep the 10th die nearby as a spare for splitting.

## Turn Structure

On your turn, you must do exactly one of the following:
- **Transfer speed** between two of your adjacent dice, OR
- **Move** one of your dice

## Actions

### Transfer Speed

Choose two of your adjacent dice and transfer 1 or more speed from one to the other. Neither die may go below 1 or above 6.

### Movement

Move one die its full speed value (number of pips showing) in a straight orthogonal line through hex sides (not corners), in any of the 6 directions.

**Movement restrictions:**
- Must move the full speed value (exact count)
- Must travel in a straight line
- Cannot move through a space occupied by any die
- Cannot move through the fission chamber

**Special movement:**
- **Wrap around:** The left and right edges of the board are connected (as if on a cylinder). A hex on the left is adjacent to the same-row hex on the right.
- **Ricochet:** A die moving toward the near or far edge with remaining speed reflects off the edge (angle of incidence = angle of reflection) and continues.

### Capture

Move your die by exact count onto a space occupied by an opponent's die to capture it. The captured die is removed from play. The captured die's speed must be **absorbed** by the opponent's slowest die still in play (choose if tied). If that die reaches 6 without absorbing all speed, repeat with the next slowest, and so on, until the team total returns to 25.

### Bump

Move your die by exact count onto a space occupied by one of **your own** dice. The bumped die moves 1 space in the same direction. The bumped die can in turn capture an enemy die or bump another friendly die (chain bumps). Ricochet applies during bumps. You cannot bump a die into the fission chamber.

### Split (Fission Chamber)

Move a die by exact count onto the central fission chamber. The die splits into 2 dice of half its speed. If the speed is odd, the higher-value die goes in the **leftward** direction (relative to entry). The two halves emerge 1 space outward on diverging paths.

Use your 10th die or a previously captured die as the second half. If no spare die is available or the original die was a 1, the die simply emerges unchanged on the leftward path.

Emerging halves behave as bumped dice (can capture enemies or bump friendlies in their landing spaces).

## Scoring / Victory Conditions

When a player is reduced to **4 dice**, they can no longer maintain their team's total speed of 25 (maximum possible with 4 dice is 24). That player loses the game immediately.

## Special Rules & Edge Cases

- A die in a half-hex (at the board edge) is considered to be in both halves of that hex.
- Transfer speed does not count as a move -- it is the alternative action for your turn.
- Chain bumps must resolve fully before the turn ends.
- A bump that would push a die into the fission chamber is illegal; the entire move is not allowed.
- The fission chamber blocks movement through it but can be a destination for splitting.

## Player Reference

**Turn options (choose one):**
1. Transfer speed between 2 adjacent friendly dice (neither below 1 or above 6)
2. Move 1 die its full speed in a straight line

**Movement types:**

| Type | Description |
|------|------------|
| Normal | Straight line, exact count, through hex sides |
| Wrap | Left-right edges connected |
| Ricochet | Reflects off near/far edges |
| Capture | Land on enemy die (exact count) |
| Bump | Land on friendly die; it moves 1 space same direction |
| Split | Land on fission chamber; die splits into 2 halves |

**Capture absorption:** Captured die's speed goes to opponent's slowest die (max 6 per die).

**Loss condition:** Reduced to 4 dice (cannot total 25).
