---
title: "Kingdoms"
bgg_id: 119
player_count: "2-4"
play_time: "45 min"
designer: "Reiner Knizia"
source_pdf: "kingdoms-rules.pdf"
extracted_date: "2026-03-20"
summarized_date: "2026-03-20"
---

## Overview

In Kingdoms, players establish castles across a 5x6 grid, placing resource tiles and hazard tiles to manipulate the value of rows and columns. Each castle scores based on the combined tile values in its row and column, multiplied by the castle's rank. The game plays over three epochs (rounds), and the player with the most gold after three epochs wins.

## Components

- 40 plastic castles (4 colors): 16 Rank 1 (4 per color), 12 Rank 2 (3 per color), 8 Rank 3 (2 per color), 4 Rank 4 (1 per color)
- 1 game board (5 rows x 6 columns grid, epoch track, tile supply area, gold bank)
- 64 gold coins: 19x value 1, 12x value 5, 20x value 10, 8x value 50, 4x value 100
- 1 epoch counter
- 23 tiles:
  - 12 Resource tiles (+1 to +6)
  - 6 Hazard tiles (-1 to -6)
  - 2 Mountain tiles
  - 1 Dragon tile
  - 1 Gold Mine tile
  - 1 Wizard tile

## Setup

1. Each player chooses a color and takes castles based on player count:
   - Castle allocation varies by player count (Rank 1 count changes; all players get all Rank 2, 3, 4 castles)
2. Sort gold coins by denomination in the gold bank area.
3. Give each player 50 gold.
4. Shuffle all tiles face-down in the tile supply area.
5. Each player draws 1 tile, looks at it secretly, and places it face-down (their starting tile).
6. Place epoch counter on space 1.
7. Randomly choose first player.

## Turn Structure

Play proceeds clockwise. On your turn, you must take **one** of three actions:

1. **Place One Castle**: Place one of your castles onto an empty space on the board.
2. **Draw and Place One Tile**: Draw a random face-down tile from the supply, look at it, and place it face-up on any empty space.
3. **Place Starting Tile**: Place your starting tile face-up on any empty space (one-time use per epoch).

You may only pass if unable to take any action. Once placed, castles and tiles cannot be moved for the rest of the epoch.

## Actions

The three available actions are placing castles or tiles (see Turn Structure). Strategic placement is the core of the game.

### Special Tile Effects (during scoring)

| Tile | Effect |
|------|--------|
| **Mountain** | Divides its row and column into two parts, each scored separately |
| **Gold Mine** | Doubles the value of all other tiles in its row and column (both positive and negative) |
| **Wizard** | Increases the rank of each orthogonally adjacent castle by 1 |
| **Dragon** | Cancels all resource tiles in its row and column; only hazard tiles count |

## Scoring / Victory Conditions

### Epoch Scoring
An epoch ends when there are no empty spaces on the board. Score each row (top to bottom), then each column (left to right):

1. **Calculate base value**: Sum all resource tile values (+) and subtract all hazard tile values (-) in that row/column.
2. **Apply special tiles**: Mountains split scoring; Gold Mine doubles; Dragon cancels resources; Wizard boosts adjacent castles.
3. **Multiply**: Each player multiplies the base value by the total ranks of their castles in that row/column.
4. **Collect or pay**: Positive result = collect gold from the bank. Negative result = pay gold to the bank.

Each tile and castle scores **twice** per epoch: once for its row, once for its column.

### Between Epochs
1. Remove all castles. Return Rank 1 castles to players; return all other ranks to the box.
2. Remove all tiles, reshuffle face-down in the supply area.
3. Each player draws a new starting tile.
4. Advance epoch counter.
5. Player with the most gold takes the first turn in the next epoch.

### Game End
After three epochs, the player with the most gold wins.

## Special Rules & Edge Cases

- **Negative gold**: Players can owe gold (pay to the bank) if their castles are in rows/columns with net negative values.
- **Starting gold**: Each player begins with 50 gold.
- **Castle availability**: Rank 2, 3, and 4 castles are used only once across all epochs (returned to box after each epoch). Only Rank 1 castles return to players.
- **Wizard adjacency**: Only orthogonal adjacency counts (not diagonal). The Wizard increases rank by 1 per adjacent castle.
- **Gold Mine doubling**: Affects both resource and hazard tile values (can make negative values worse).
- **Dragon**: Completely eliminates resource tiles from scoring in its row and column, but hazard tiles still count.
- **Mountain splitting**: Each side of the mountain is scored independently.

### Variants
- **Down to the Last Castle**: No epoch counter. All castles used every epoch. Game ends when any player places their last castle. Empty spaces count as value 0.
- **No Luck**: All tiles placed face-up at start. No starting tile drawn. Players choose which tile to place.
- **Score as You Go**: Score each row/column immediately when filled, rather than waiting for the end of the epoch.

## Player Reference

**Turn**: Place 1 castle OR draw and place 1 tile OR place your starting tile

**Scoring Formula**: (Sum of resource values - Sum of hazard values) x Total castle ranks = Gold gained/lost

**Special Tiles Quick Reference**:
| Tile | Scoring Effect |
|------|---------------|
| Mountain | Splits row/column |
| Gold Mine | Doubles all tile values |
| Wizard | +1 rank to adjacent castles |
| Dragon | Cancels all resource tiles |

**Epoch Flow**: Play → Score → Remove castles & tiles → Reshuffle → Draw starting tile → Next epoch
