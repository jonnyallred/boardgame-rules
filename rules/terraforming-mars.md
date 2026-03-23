---
title: "Terraforming Mars"
bgg_id: 167791
player_count: "1-5"
play_time: "120 min"
designer: "Jacob Fryxelius"
source_pdf: "terraforming-mars-rules.pdf"
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

# Terraforming Mars

## Overview

In Terraforming Mars, players control corporations working together to terraform the planet Mars by raising three global parameters: temperature, oxygen level, and ocean coverage. Each generation (round), players buy and play project cards to increase their production, place tiles on the Martian surface, and advance global parameters. Players accumulate terraform rating (TR) and victory points through card play, tile placement, milestones, and awards.

## Components

- 1 Game board (Mars surface map with TR track, global parameter tracks)
- 5 Player boards (resource tracking with 6 resource types)
- 233 Project cards, 12 Corporation cards
- Resource cubes (bronze=1, silver=5, gold=10)
- Player markers (5 colors)
- Ocean tiles (9), Greenery tiles, City tiles, Special tiles
- Temperature marker, Oxygen marker, Generation marker
- First player marker
- Rulebook

## Setup

1. Place the board with temperature at -30C, oxygen at 0%, and generation marker at 1.
2. Each player takes a player board, places all production markers at 1, and places a marker on TR 20.
3. Deal each player 2 corporation cards and 10 project cards.
4. Players choose 1 corporation (gaining its starting resources/production) and buy project cards at 3 MC each.
5. The first generation skips the Player Order and Research phases.

## Turn Structure

Each generation has 4 phases:

### I. Player Order Phase
Pass the first player marker clockwise; advance the generation marker. (Skipped in generation 1.)

### II. Research Phase
Each player draws 4 cards and may buy any number at 3 MC each. (Skipped in generation 1.)

### III. Action Phase
Starting with the first player, players take turns performing 1-2 actions or passing. Continue clockwise until all players have passed.

### IV. Production Phase
1. All energy converts to heat.
2. Gain MC equal to TR + MC production (can be negative, but never below -5).
3. Gain other resources equal to their production values.
4. Remove player markers from used action cards.

## Actions

Players may perform 1-2 of the following actions per turn:

### A. Play a Project Card
Check requirements (global parameters, tags, production), pay the cost in MC (steel = 2 MC for building tags; titanium = 3 MC for space tags), and resolve the card's effects.

### B. Use a Standard Project
| Project | Cost | Effect |
|---|---|---|
| Sell Patents | Free | Discard cards for 1 MC each |
| Power Plant | 11 MC | +1 energy production |
| Asteroid | 14 MC | +1 temperature (+1 TR) |
| Aquifer | 18 MC | Place 1 ocean tile (+1 TR) |
| Greenery | 23 MC | Place greenery (+1 oxygen, +1 TR) |
| City | 25 MC | Place city (+1 MC production) |

### C. Claim a Milestone (8 MC)
| Milestone | Requirement |
|---|---|
| Terraformer | TR >= 35 |
| Mayor | Own >= 3 cities |
| Gardener | Own >= 3 greenery tiles |
| Builder | >= 8 building tags |
| Planner | >= 16 cards in hand |

Only 3 milestones may be claimed total. Each is worth 5 VP.

### D. Fund an Award (8 / 14 / 20 MC)
| Award | Criteria |
|---|---|
| Landlord | Most tiles on Mars |
| Banker | Highest MC production |
| Scientist | Most science tags |
| Thermalist | Most heat resources |
| Miner | Most steel + titanium |

Only 3 awards may be funded total. 1st place = 5 VP, 2nd = 2 VP.

### E. Use a Blue Card Action
Activate an action on a played blue card (once per generation, marked with red arrow).

### F. Convert Plants to Greenery
Spend 8 plants to place a greenery tile (+1 oxygen, +1 TR).

### G. Convert Heat to Temperature
Spend 8 heat to raise temperature 1 step (+1 TR).

## Scoring / Victory Conditions

The game ends when all three global parameters reach their goals:
- **Temperature:** +8C
- **Oxygen:** 14%
- **Oceans:** 9 tiles placed

Complete the current generation (including production). Then score:

1. **TR:** Final position on the TR track.
2. **Awards:** 5 VP for 1st, 2 VP for 2nd per funded award.
3. **Milestones:** 5 VP each.
4. **Greenery tiles:** 1 VP each.
5. **Cities:** 1 VP per adjacent greenery tile (any owner).
6. **Card VP:** Count VP symbols on all played cards.

Highest total wins. Ties broken by most MC.

## Special Rules & Edge Cases

- **Tile Placement:** Ocean tiles go only on reserved spaces, are unowned, and provide 2 MC to any player placing a tile adjacent later. Greenery tiles must be placed adjacent to your own tiles if possible. Cities cannot be placed adjacent to other cities (except Noctis City).
- **Global Parameter Cap:** Once a parameter reaches its goal, further increases are ignored (no TR gain).
- **Post-Game Plants:** After the final generation, players convert remaining plants to greenery in turn order before final scoring.
- **Tag System:** Tags affect costs (building = steel, space = titanium), requirements, milestones, and awards. Tags on events only apply during the play action.
- **Solo Mode:** Start at TR 14. Must complete all 3 parameters by end of generation 14 to win.
- **Card Types:** Green (automated, one-time), Blue (active, ongoing with actions), Red (events, played face-down after resolution).
- **No Hand Limit:** There is no maximum number of cards in hand.
- **Production Floor:** MC production can go negative (minimum -5), but other resources cannot go below 0.

## Player Reference

| Resource | Use |
|---|---|
| MC (MegaCredits) | Pay for cards, projects, milestones, awards |
| Steel | Worth 2 MC for building tags |
| Titanium | Worth 3 MC for space tags |
| Plants | 8 plants = 1 greenery tile |
| Energy | Converts to heat each generation |
| Heat | 8 heat = +1 temperature |

**Game End:** All 3 parameters at goal -> finish generation -> final scoring
