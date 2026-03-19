---
title: "Adaptoid"
bgg_id: 51195
player_count: "2"
play_time: "20 min"
designer: "Nestor Romeral Andres"
source_pdf: "adaptoid-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
---

## Overview

Adaptoid is an abstract strategy board game for two players. Each game lasts around 20 minutes. An adaptoid is a creature that constantly evolves to adapt itself to its surroundings. To survive, it needs to be fed. Two players confront their armies of adaptoids on a hexagonal board with the aim of eliminating the opponent's adaptoids. The first player to capture 5 enemy adaptoids wins.

## Components

- 1 hexagonal board with 37 circles
- 12 white adaptoids, 12 white legs, and 12 white pincers
- 12 black adaptoids, 12 black legs, and 12 black pincers
- 5 white counters and 5 black counters (for scoring captures)

## Setup

1. Randomly determine player colors (black or white).
2. Position the board in the middle of the table.
3. Each player takes all pieces of their color (adaptoids, legs, and pincers).
4. Each player positions one adaptoid (without legs or pincers) on the board in the designated starting position. Other initial positions are permitted by mutual agreement.
5. The white player plays first.

## Turn Structure

On each turn, a player performs the following three steps in order:

1. **Move (optional):** Move one of your adaptoids (see Movement and Capture). This may result in capturing an enemy adaptoid.
2. **Grow (mandatory):** Either create a new adaptoid of your color OR add a leg or pincer to one of your existing adaptoids on the board.
3. **Starve (mandatory):** Remove all enemy adaptoids that are not fed (see Feeding the Adaptoids).

After completing all three steps, the turn passes to the other player.

## Actions

### Movement and Capture

- An adaptoid can move up to as many free spaces as the number of legs it has, in any direction, not necessarily in a straight line.
- An adaptoid with no legs cannot move.
- An adaptoid cannot pass through an occupied space.
- An adaptoid may end its movement on a space occupied by an enemy adaptoid, triggering a capture:
  - The adaptoid with more pincers captures the enemy (removes it from the board).
  - If both have the same number of pincers, both are removed from the board.
  - An adaptoid with no pincers cannot capture.
- Captured pieces return to the player's supply and can be reused. Record captures by taking scoring discs of the opponent's color.

### Creating an Adaptoid

- Place a new adaptoid (without legs or pincers) on any empty space adjacent to one of your existing adaptoids.

### Adding Legs and Pincers

- Add one leg or one pincer to any of your adaptoids already on the board by inserting it into a free slot.
- An adaptoid can have a maximum of 6 extremities total (legs and pincers combined in any ratio).

### Feeding the Adaptoids

- At the end of each turn, check all enemy adaptoids.
- An adaptoid must be surrounded by at least as many free (empty) spaces as the total number of its extremities (legs + pincers).
- Any enemy adaptoid that does not meet this requirement is removed from the board, and the current player scores a capture.

## Scoring / Victory Conditions

- The first player to capture at least 5 enemy adaptoids wins the game.
- A player also loses if all of their adaptoids are removed from the board.
- In case of a tie (both conditions met simultaneously), the player who made the last move wins.

## Special Rules & Edge Cases

- **Super-Adaptoid Variant:** Requires a Super-Adaptoid set. Players can configure a custom board before the game by using 37 discs. The board does not need to have a hexagonal distribution. An adaptoid must be surrounded by at least as many free discs as its total number of extremities to survive.
- An adaptoid with no legs at the start of the game cannot move; it must first have legs added to it.
- An adaptoid with no pincers cannot initiate a capture, even if it can reach an enemy space.
- Movement through occupied spaces (friendly or enemy) is not allowed; only the destination space matters for capture.

## Player Reference

**Turn sequence:** Move (optional) -> Grow (mandatory) -> Starve enemy (mandatory)

| Action | Details |
|--------|---------|
| Move | Up to N spaces (N = number of legs), any direction, no passing through occupied spaces |
| Create | Place new bare adaptoid adjacent to a friendly adaptoid |
| Add part | Insert 1 leg or 1 pincer into an existing adaptoid (max 6 total parts) |
| Capture (movement) | Land on enemy; more pincers wins. Equal pincers = both removed. 0 pincers = cannot capture |
| Capture (starvation) | Enemy adaptoid removed if free adjacent spaces < total extremities |
| Win condition | First to capture 5 enemy adaptoids, or opponent has no adaptoids left |
