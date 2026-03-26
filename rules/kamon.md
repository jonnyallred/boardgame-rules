---
title: "Kamon"
bgg_id: 28738
player_count: "2"
play_time: "15 min"
designer: "Bruno Cathala"
source_pdf: "kamon-rules.pdf"
extracted_date: "2026-03-20"
summarized_date: "2026-03-20"
---

## Overview

Kamon is a two-player abstract strategy game played on a hexagonal grid of 37 spaces. Players place tokens with six different colors and six different symbols, creating a unique board each game. On each turn, a player must place their piece on a token that matches either the color or symbol of the previously played token. The goal is to connect two opposite edges of the board with your color, create a loop, or force your opponent into an impossible move.

## Components

- Hexagonal board with 37 hex spaces
- 36 tokens (6 colors x 6 symbols, each combination appearing once)
- 1 blank token
- Black hexagonal pieces (for one player)
- White hexagonal pieces (for one player)
- 1 golden hexagon marker

## Setup

1. Shuffle all 37 tokens (36 printed + 1 blank) and randomly place one token face-up on each hex space of the board.
2. Decide which player plays black and which plays white.
3. The black player goes first.

## Turn Structure

Players alternate turns. On your turn:
1. Place one of your colored hexagons on any token that matches either the **color** or the **symbol** of the token your opponent just played on.
2. Place the golden hexagon on top of your piece as a reminder of the constraint for the next player.

## Actions

### Placement
- You must place your piece on a token that shares either the same color or the same symbol as the token that was just covered by your opponent's last move.
- There may be multiple valid placement options each turn.
- The blank token acts as a wild -- it can always be played on and always matches.

### First Move
- The black player's first move has no constraint -- they may place on any token along the edge of the board (except corners).

## Scoring / Victory Conditions

There are three ways to win:
1. **Edge Connection:** Be the first to create an unbroken chain of your hexagons connecting two edges of the board that share the same color border.
2. **Loop:** Create a closed loop (cycle) with your hexagons.
3. **Forced Pass:** Force your opponent into a position where they have no legal placement -- they cannot find any uncovered token matching the required color or symbol.

## Special Rules & Edge Cases

- The board is randomized each game, so the strategic landscape is always different.
- The golden hexagon serves as a memory aid to track which token was last played on.
- Corner hexes are not valid for the first move.
- The blank token is always a valid target and always creates a wild constraint for the next player.
- Creating a connection requires an unbroken path of your hexagons from one colored edge to the matching colored edge on the opposite side.

## Player Reference

| Win Condition | Description |
|---------------|-------------|
| Edge Connection | Connect two same-colored edges with your pieces |
| Loop | Create a closed loop of your pieces |
| Forced Pass | Opponent has no legal move |

| Key Numbers | Value |
|-------------|-------|
| Board spaces | 37 hexes |
| Token types | 36 (6 colors x 6 symbols) + 1 blank |
| Players | 2 |
| Play time | ~15 minutes |
