---
title: Oust
bgg_id: 30936
player_count: "2"
play_time: "30-60 minutes"
designer: Mark Steere
source_pdf: "web-sourced"
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

## Overview

Oust is an abstract strategy game designed by Mark Steere, considered his most influential creation. Two players alternate placing stones on an empty board, forming groups and capturing opponent stones. The game combines elements of Go-like connection with unique capturing mechanics. The objective is to capture all of the opponent's stones.

## Components

- 1 game board (base-11 grid of intersections)
- Stones in 2 colors (Black and White)

## Setup

1. The board starts completely empty.
2. Black places first.

## Turn Structure

Players alternate turns. On each turn, place exactly one stone of your color on any empty intersection, following placement rules.

## Actions

There are two types of moves:

### 1. Non-Capturing Move
Place a stone on any empty intersection that does **not** connect to (enlarge) any of your existing groups. This creates a new isolated stone.

### 2. Capturing Move
Place a stone that **does** enlarge one of your groups (connects orthogonally to friendly stones). This is legal **only if**:
- The enlarged group touches at least one opponent's stone, AND
- **All** opponent groups touching your enlarged group must be **smaller** than your group.

When a legal capture occurs:
- All opponent groups touching your group are **removed** from the board.
- You must then make **another move** in the same turn (which may trigger additional captures -- a chain reaction).

## Scoring / Victory Conditions

**Win:** Capture **all** of the opponent's stones on the board.

There is no point scoring -- the game ends when one player has no stones remaining.

## Special Rules & Edge Cases

- A **group** is one stone or two or more same-colored, orthogonally connected stones.
- You can only enlarge your own group if doing so results in a legal capture (all touching enemy groups must be smaller).
- Chain captures: After each capture, you must immediately place another stone. This can trigger further captures.
- The game cannot end in a draw -- one player will always be able to capture all opponent stones.
- **Strategy:** Try to force your opponent into creating many small groups while keeping your own groups manageable. Only capture when you must.
- Sacrificing stones to fragment opponent groups is a common opening tactic.

## Player Reference

**Turn:** Place 1 stone -- either non-capturing (new isolated stone) or capturing (enlarge group + remove smaller enemy groups)

**Non-capturing:** Must NOT connect to any friendly group

**Capturing:** Must connect to friendly group AND all touching enemy groups must be smaller

**After capture:** Must place another stone immediately (chain reaction possible)

**Win:** Capture all opponent's stones
