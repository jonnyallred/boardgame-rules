---
title: "Parade"
bgg_id: 56692
player_count: "2-6"
play_time: "30 minutes"
designer: "Naoki Homma"
source_pdf: "parade-rules.pdf"
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

## Overview

Parade is a card game set in Wonderland where players play cards to a central line (the parade) while trying to avoid collecting cards from it. Points are bad -- the player with the lowest score wins.

## Components

- 66 cards in 6 colors (values 0-10 in each color)
- 1 score pad

## Setup

1. Determine start player randomly; play proceeds clockwise.
2. Shuffle the deck and deal 5 cards face down to each player.
3. Place 6 cards face up in a row in the center of the table to form the initial parade. Place the game box at one end to mark the front.
4. Place remaining cards face down as the draw pile.

## Turn Structure

On your turn, perform these 3 steps in order:

1. **Play a card** from your hand to the end of the parade.
2. **Remove cards** from the parade if required (see removal rules below).
3. **Draw a card** from the draw pile to refill your hand to 5 cards.

## Actions

### Card Removal Rules

When you play a card, count the number of cards already in the parade (not counting the card you just played):

- If the number of cards in the parade is **less than or equal to** the value of the played card, no cards are removed.
- If the number of cards in the parade is **greater than** the value of the played card, some cards enter "removal mode."

**Determining removal mode:** Starting from the end of the parade (nearest to where you placed your card), number the cards 1, 2, 3, etc. Cards with a position number **greater than** the played card's value are in removal mode.

**Which cards in removal mode are actually removed:**
- All cards of the **same color** as the played card
- All cards with a value **less than or equal to** the played card's value

Removed cards go face up in front of the player, sorted by color with values visible.

**Special case:** If a card with value **0** is played, all cards in the parade enter removal mode.

## Scoring / Victory Conditions

### Triggering the Last Round
The last round begins when either:
- A player collects cards of all 6 colors, OR
- The draw pile is exhausted

After the triggering condition, every player (including the trigger player) plays one more turn without drawing cards.

### Final Scoring
1. Each player chooses 2 cards from their hand and discards them. The remaining 2 hand cards are added to their collected cards.
2. For each color, determine who has the **majority** (most cards of that color). Those cards are flipped face down and count as **1 point each** instead of face value.
3. All face-up cards score their printed value.
4. Sum all points (face-down cards at 1 each + face-up card values).

**The player with the lowest total score wins.** Tiebreaker: fewest total cards.

## Special Rules & Edge Cases

- **2-player rule:** A player has majority only if they have **2 or more cards** of a color than the other player.
- If multiple players tie for majority in a color, all tied players flip their cards (each counting as 1 point).
- Cards remaining in the parade at game end are discarded and do not score.
- The played card itself never counts when determining which cards are in the parade for removal purposes.
- Gaps in the parade are closed by sliding remaining cards together after removals.

## Player Reference

| Step | Action |
|------|--------|
| 1 | Play 1 card to the end of the parade |
| 2 | Remove qualifying cards from parade to your collection |
| 3 | Draw 1 card from draw pile |

**Removal check:** Cards at position > played card's value enter removal mode. Remove those that match the played card's color OR have value <= played card's value.

**Scoring:** Majority in a color = cards count as 1 point each. Non-majority cards = face value. Lowest score wins.
