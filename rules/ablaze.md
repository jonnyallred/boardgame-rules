---
title: "Ablaze!"
bgg_id: 65516
player_count: "2-4"
play_time: "45-60 min"
designer: "Heinrich Glumpler"
source_pdf: "ablaze-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
---

## Overview

Ablaze! (originally published as Feurio!) is a tile-laying and area-control game by Mayfair Games. The box includes three separate games — Wild Fire!, Volcano!, and On the Run! — all using the same components. In the core Wild Fire! game, players are firefighters placing tiles to build a spreading wildfire and strategically positioning their firefighter pawns to claim valuable groups of burning tiles. The key tension is between expanding the fire (high-value tiles) and maintaining access to water (free edges) for scoring.

## Components

- Forest tiles (numbered 0–9 on one side, forest art on the other; the number represents fire intensity)
- Player pawns (one color per player, multiple pawns each)
- Game board / play area (tiles are placed to form the fire)

## Setup

1. Shuffle all forest tiles with the 0 (forest) side facing up.
2. The oldest player selects and arranges initial tiles (one per player) to form a starting fire cluster.
3. The player to their left takes the first turn.
4. Each player takes all pawns of their chosen color.

## Turn Structure

On each turn, a player performs the following steps in order:

1. **Flip and place a tile:** Flip over one face-down forest tile to reveal its number. Place it adjacent to the existing fire where the combined fire intensity (sum of numbers on adjacent tiles) is highest. If multiple spots are tied for highest, the active player chooses among them.
2. **Place pawns (optional):** After placing the tile, the player may place one or more of their pawns on any tile(s) in the fire. The number of pawns a tile can hold is limited by the number of free edges (sides not touching other tiles) that tile currently has. A tile with zero free edges cannot accept new pawns.
3. **Pass:** Play moves to the next player clockwise.

Continue until all forest tiles have been flipped and placed. After all tiles are placed, players may only place pawns or pass. The game ends when all players consecutively pass.

## Actions

### Tile Placement Rules

- Each tile must be placed adjacent to the existing fire layout.
- The tile goes to the position where the sum of adjacent tiles' numbers is highest.
- Ties are broken by the active player's choice.

### Pawn Placement Rules

- Pawns may be placed on any tile in the fire (not just the one just placed).
- The maximum number of pawns on a tile equals the number of its free (open) edges.
- If a tile becomes surrounded (no free edges), no new pawns can be placed on it, but existing pawns remain.

## Scoring / Victory Conditions

After the game ends, score each connected group of tiles where you have pawns:

1. **Identify groups:** A group is a set of connected tiles (sharing edges) where you have at least one pawn.
2. **Check for free edges:** If the group has no free edges at all (completely enclosed), the group scores **zero points**.
3. **Calculate score:** For groups with at least one free edge, add up all the numbers on the tiles in the group. Then divide that total by the lowest-numbered tile in the group that has a free edge. Round down if necessary.
4. **Total:** Sum the scores from all your groups. The player with the highest total score wins.

**Tiebreaker:** The player with the single most valuable scoring group wins.

## Special Rules & Edge Cases

- A tile's capacity for pawns changes as the fire grows — placing a new tile adjacent to an existing tile reduces the existing tile's free edges (and thus its pawn capacity). Existing pawns are never removed due to lost edges.
- Tiles numbered 0 can be critical: they represent the divisor in scoring, so a group containing a 0-tile with a free edge would require dividing by 0, which typically means that tile cannot serve as the divisor (use the next-lowest tile instead).
- **Variant games included:**
  - **Volcano!** (reimplements Vulkan!): Players pilot fire-fighting planes trying to quench bushfire around an active volcano, isolating fire areas so ground units can extinguish them.
  - **On the Run!**: Lightning has started a brush fire and wildlife is fleeing. Different rules apply using the same components.
- Optional rules include firebreaks, adjusted single-tile scoring, and cooperative play modes.

## Player Reference

| Phase | Action |
|-------|--------|
| 1. Flip tile | Reveal number, place at highest-intensity spot |
| 2. Place pawns | Optional; on any tile with free edges; max pawns = free edges |
| 3. Pass | Next player clockwise |

**Scoring per group:** (Sum of tile numbers) / (Lowest number on a tile with a free edge in the group). No free edges = 0 points.
