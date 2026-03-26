---
title: "Kulami"
bgg_id: 108831
player_count: "2"
play_time: "30 min"
designer: "Andreas Kuhnekath"
source_pdf: "kulami-rules.pdf"
extracted_date: "2026-03-20"
summarized_date: "2026-03-20"
---

## Overview

Kulami is a two-player abstract strategy game where players place glass marbles on a field of interconnecting wooden panels. Each player tries to control as many panels as possible by having a majority of their colored marbles on each panel. The player with the most points from controlled panels wins.

## Components

- 17 wooden panels of various sizes: 4x6-field panels, 5x4-field panels, 4x3-field panels, 4x2-field panels
- 28 red glass marbles
- 28 black glass marbles

## Setup

1. Arrange the 17 panels into a game field. Two standard layouts exist:
   - **Closed square**: equal rows with 8 fields per row
   - **Irregular**: extended area with a maximum of 10 fields in any direction
2. Each player selects a color (red or black) and takes 28 marbles.
3. Determine first player: one player hides a red marble in one hand and black in the other; the opponent picks a hand to reveal the first player's color.

## Turn Structure

Players alternate turns, each placing one marble on any available space following the placement rules.

## Actions

### Placement Rules
1. **First marble**: Place anywhere on the field.
2. **Subsequent marbles**: Must be placed in one of the two rows (horizontal or vertical) that intersect with the position of the **previous** marble.
3. **Off-limits rule**: Cannot place on the same panel as the previous marble, NOR on the panel used the turn before that (the two most recently used panels are off-limits).
4. Rows continue across gaps or holes in the field.

### Key Terms
- **Panel**: A single wooden piece (2, 3, 4, or 6 fields)
- **Field**: A single circular space on a panel
- **Row**: A horizontal or vertical line across the game field (can cross panel boundaries and gaps)
- **Chain**: A straight line of same-colored marbles
- **Area**: A contiguous group of same-colored marbles (orthogonal adjacency only, not diagonal)

## Scoring / Victory Conditions

### Basic Scoring
1. Disconnect the panels for easier counting.
2. Each panel where one player has more marbles than the other is won by that player.
3. A won panel scores points equal to the **total number of fields** on that panel (not the number of marbles placed).
4. Panels with a tied number of each color are excluded from scoring.
5. **Winner**: Most total points.

### Advanced Level 1
Score panels as normal, then also score the **largest contiguous area** of each color (orthogonal adjacency only, not diagonal). The player with the larger area earns bonus points equal to the difference in area sizes.

### Advanced Level 2
Score panels and largest area as in Level 1, plus score **chains** of 5+ same-colored marbles in a straight line:
- 5 marbles = 5 points
- 6 marbles = 6 points, etc.

All bonus points are added to panel points. Highest total wins.

## Special Rules & Edge Cases

- **Game end**: When all marbles are placed, OR when a player cannot legally place a marble (both valid rows are fully occupied, or the off-limits rule prevents placement in any available space).
- **Off-limits**: Only the two most recently used panels are blocked. Panels used earlier can be used again.
- **Rows span gaps**: A row continues across any holes or missing panels in the field.
- **Panel scoring**: The full field count of the panel scores, regardless of how many marbles are actually on it. A 6-field panel always scores 6 points if won.

## Player Reference

**Placement**: Must go in a row intersecting the last marble's position, but NOT on the last 2 panels used.

**Scoring**:
| Panel Size | Points if Won |
|------------|---------------|
| 6 fields | 6 |
| 4 fields | 4 |
| 3 fields | 3 |
| 2 fields | 2 |

**Win condition**: Most points from controlled panels (+ bonuses in advanced modes).
