---
title: "Twilight Struggle"
bgg_id: 12333
player_count: "2"
play_time: "120-180 min"
designer: "Ananda Gupta, Jason Matthews"
source_pdf: "twilight-struggle-rules.pdf"
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

# Twilight Struggle

## Overview

Twilight Struggle is a two-player strategy game simulating the Cold War between the United States and Soviet Union from 1945-1989. Over 10 turns (each representing 3-5 years), players play cards for either their Operations value or Event text, managing influence in countries worldwide while competing for regional dominance. The game balances careful influence placement with the constant threat of nuclear war (DEFCON).

## Components

- 1 Game map (world divided into 6 regions with countries and influence tracks)
- Influence markers (US and USSR)
- 110 Cards (Early War, Mid War, Late War decks)
- VP marker and track (-20 to +20)
- DEFCON marker (levels 1-5)
- Military Operations markers
- Space Race track
- Turn/Action Round markers
- 2 Six-sided dice
- China Card
- Player aid cards

## Setup

**USSR Influence (15 markers):** 1 Syria, 1 Iraq, 3 North Korea, 3 East Germany, 1 Finland, 6 anywhere in Eastern Europe.

**US Influence (25 markers):** 2 Canada, 1 Iran, 1 Israel, 1 Japan, 4 Australia, 1 Philippines, 1 South Korea, 1 Panama, 1 South Africa, 5 United Kingdom, 7 anywhere in Western Europe.

Set DEFCON to 5, VP to 0, Turn marker to 1. Deal 8 Early War cards to each player. USSR receives the China Card face-up.

## Turn Structure

Each turn (10 total) follows this sequence:

1. **Improve DEFCON:** If below 5, increase by 1.
2. **Deal Cards:** Bring hand to 8 (turns 1-3) or 9 (turns 4-10).
3. **Headline Phase:** Both players simultaneously reveal 1 card; higher Operations value resolves first (ties favor US). Events only -- no Operations points.
4. **Action Rounds:** USSR plays first, then alternate. 6 rounds (turns 1-3) or 7 rounds (turns 4-10) per turn. Each card is played for either Event or Operations.
5. **Check Military Operations:** Lose VP if Military Ops are below the current DEFCON level.
6. **Flip China Card:** If passed face-down, flip face-up.
7. **Advance Turn:** At end of turn 3, shuffle Mid War cards into the deck. At end of turn 7, shuffle Late War cards in.

## Actions

When playing a card for Operations, spend ALL Operations points on ONE action:

### 1. Place Influence
- Cost: 1 OP per influence marker in friendly/uncontrolled countries; 2 OP in enemy-controlled countries.
- Markers must be placed in or adjacent to countries where you already have influence (exception: your superpower's adjacent countries are always available).

### 2. Realignment Rolls
- Cost: 1 OP per roll.
- Each player rolls a die with modifiers: +1 per adjacent controlled country, +1 for more influence in target, +1 if your superpower is adjacent.
- Higher roll removes difference from opponent's influence. Ties = no effect.
- Never adds friendly influence.

### 3. Coup Attempts
- Roll die + Operations value. If result > (Stability x 2), success.
- Remove opponent's influence equal to excess; if insufficient, add your own.
- Military Ops marker advances by card's Operations value.
- Coups in Battleground countries degrade DEFCON by 1.
- Subject to DEFCON geographic restrictions.

### 4. Space Race
- Discard a card with sufficient Operations value (matching box requirement).
- Roll die; if within target range, advance on Space Race track.
- VP awarded for reaching certain boxes.
- Limit: 1 Space Race attempt per turn (upgradeable).

### Event Play
- Your event: triggers automatically.
- Opponent's event on your card: event still triggers even when playing for Operations.
- Cards with * are removed after their event occurs.
- Scoring cards must be played during the turn they are drawn.

## Scoring / Victory Conditions

### Instant Victory
- **DEFCON 1:** The phasing player (who caused it) immediately loses.
- **VP Track:** Reaching +20 (US) or -20 (USSR) = instant win.
- **Control of Europe:** If one player controls all European Battleground countries during European scoring.

### Regional Scoring (via Scoring cards)
Three levels per region:
- **Presence:** Control >= 1 country.
- **Domination:** Control more countries AND more Battleground countries; must have >= 1 of each.
- **Control:** Control more countries AND ALL Battleground countries.

VP varies by region and control level. Additional VP per controlled Battleground country and per adjacent enemy superpower country.

### Final Scoring (end of Turn 10)
Score all regions simultaneously. Highest VP wins.

### Military Operations Check
Each turn, Military Ops must >= DEFCON level. Shortfall = opponent gains 1 VP per missing point.

## Special Rules & Edge Cases

- **DEFCON Restrictions:** At DEFCON 4: no coups/realignment in Europe. DEFCON 3: add Asia. DEFCON 2: add Middle East. DEFCON 1: game over.
- **China Card:** Playable as a regular Operations card. +1 OP if all Operations spent in Asia. Cannot be played in Headline Phase. Passed face-down to opponent after use; flipped face-up at turn end.
- **Scoring Cards:** Must be played during the turn drawn. Cannot be held. Cannot be discarded for events.
- **Opponent's Events:** When you play a card with your opponent's event for Operations, the event still triggers. You choose whether event resolves before or after Operations.
- **Permanent Events (underlined):** Stay in effect for the entire game.
- **Country Control:** Requires influence >= Stability Number AND exceeding opponent's influence by at least the Stability Number.
- **War Cards:** Korean, Arab-Israeli, Indo-Pakistani, Brush War, Iran-Iraq -- these use special resolution rules.
- **Satellite Countries:** US/USSR spaces are out-of-play but count as "adjacent controlled" for modifiers.
- **Forced Card Play:** If you have insufficient cards for all Action Rounds, you sit out remaining rounds.

## Player Reference

| Operations Use | Cost | Effect |
|---|---|---|
| Place Influence | 1 OP (friendly) or 2 OP (enemy-controlled) | Add influence markers |
| Realignment | 1 OP per roll | Remove opponent influence |
| Coup | All OP | Roll + OP vs 2x Stability |
| Space Race | Card discard | Advance Space Race track |

**DEFCON Track:** 5 (peace) -> 1 (nuclear war = phasing player loses)

**VP:** -20 to +20 | Instant win at either extreme

**Control:** Influence >= Stability AND lead >= Stability
