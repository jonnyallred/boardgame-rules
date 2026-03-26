---
title: "BattleCON: War of Indines"
bgg_id: 89409
player_count: "2"
play_time: "20-60 min"
designer: "D. Brad Talton Jr."
source_pdf: "battlecon-war-of-indines-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
---

## Overview

BattleCON: War of Indines is a two-player card game inspired by 2D fighting video games. Each player selects a unique character and fights duels by simultaneously selecting attack pairs (a Style card + a Base card). Attacks are revealed simultaneously, and priority determines who strikes first. Characters move along a 7-space linear board, using positioning, timing, and their unique abilities to reduce their opponent's life to zero. A match consists of best-of-three duels.

## Components

- 18 Unique character cards with special abilities
- Style cards (unique per character)
- Base cards (shared generic set per character)
- 7-space linear game board
- Life trackers (20 life points per player)
- Tokens and counters

## Setup

1. Each player selects a different character.
2. Each player takes their character's Style cards and Base cards.
3. Place both character tokens on the board: one on space 2, the other on space 5 (3 spaces apart).
4. Set both players' life to 20.
5. Determine first player randomly.

## Turn Structure

Each turn is called a "beat." Beats follow this sequence:

### 1. Select Attacks (Simultaneous)
Both players secretly choose one Style card and one Base card from their hand to form their attack pair. Place them face-down.

### 2. Reveal Attacks
Both players flip their attack pairs face-up simultaneously.

### 3. Determine Priority
Compare the combined Priority values of each player's attack pair. The player with the higher Priority is the "active player" and attacks first. If tied, the player who was hit last beat goes first (or the one closer to their starting side).

### 4. Active Player's Attack
The active player performs their attack:
- **Start of Beat effects** resolve.
- **Movement**: Move your character based on the attack's movement effects.
- **Range Check**: Your attack hits if the opponent is within the attack's minimum and maximum range.
- **Damage**: If the attack hits, deal damage equal to the attack's Power to the opponent.
- **Stun Check**: If damage dealt meets or exceeds the opponent's Stun Guard, the opponent is stunned and does not get to attack this beat.

### 5. Reactive Player's Attack (if not stunned)
If not stunned, the reactive player performs their attack using the same procedure.

### 6. End of Beat
- **Recycle**: Move attack pairs from 2 beats ago back to your hand (cards used last beat and this beat remain unavailable).
- **Discard**: Place this beat's cards in the "1 beat ago" area.

## Actions

### Attack Pair Components

**Style Cards** (unique per character):
- Provide modifiers to Priority, Range, Power, and Stun Guard.
- May include special abilities (Before Activating, On Hit, After Activating, etc.).

**Base Cards** (shared set):
| Base | Priority | Range | Power | Special |
|------|----------|-------|-------|---------|
| Strike | 3 | 1-2 | 4 | Standard attack |
| Shot | 2 | 3-5 | 3 | Ranged attack |
| Drive | 4 | 1 | 3 | Advance 1-2 spaces |
| Burst | 1 | 2-3 | 3 | Retreat 1-2 spaces |
| Grasp | 5 | 1 | 2 | Move opponent 1 space |
| Dash | 9 | - | - | Move 1-3 spaces; no attack |

### Movement
- Movement is along the 7-space linear board.
- "Advance" = move toward opponent.
- "Retreat" = move away from opponent.
- "Move" = move in either direction.
- A character cannot move through or land on the opponent's space.

### Stun
If you take damage equal to or greater than your Stun Guard (from your attack pair), you are stunned and lose your attack for this beat.

## Scoring / Victory Conditions

- Each duel starts at 20 life. Reduce opponent to 0 life to win the duel.
- A match is best-of-three duels. Win 2 duels to win the match.
- If both players are reduced to 0 in the same beat, the player with more life remaining wins. If still tied, the active player loses.
- If 15 beats pass without a winner, the player with more life wins.

## Special Rules & Edge Cases

- **Card Rotation**: Cards used this beat and last beat are unavailable. Cards from 2 beats ago return to hand. This creates a "hand cycle" that prevents spamming the same attack.
- **Unique Abilities**: Each character has a Unique Ability that defines their playstyle (e.g., one character gains power from taking hits, another can teleport).
- **Overdrive Finish**: A powerful special attack available once per duel when opponent is low on life. Costs 7+ life to attempt.
- **Ante**: Before revealing, players may ante tokens (if their character has them) for additional effects.
- **Clash**: If both attacks hit and both are stunned simultaneously, neither attack resolves (both miss).
- **Board Edges**: Characters cannot move past space 1 or space 7.

## Player Reference

### Beat Sequence
1. Both players select Style + Base face-down
2. Reveal simultaneously
3. Higher Priority attacks first
4. Active player: move, range check, deal damage, stun check
5. Reactive player (if not stunned): same steps
6. Recycle cards from 2 beats ago; discard this beat's cards

### Key Stats
| Stat | Effect |
|------|--------|
| Priority | Determines who attacks first |
| Range | Min-Max distance to hit |
| Power | Damage dealt on hit |
| Stun Guard | Damage threshold to avoid being stunned |

### Quick Reference
- Starting life: 20
- Board size: 7 spaces
- Match: Best of 3 duels
- Card cycle: 2-beat cooldown
- Beat limit: 15 beats per duel
