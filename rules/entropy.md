---
title: "Entropy"
bgg_id: 1329
player_count: "2"
play_time: "30 min"
designer: "Eric Solomon"
source_pdf: "entropy-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
---

## Overview

Entropy is a two-player abstract strategy game based on the conflict between order and chaos. One player plays as Order, trying to create palindromic patterns in rows and columns. The other plays as Chaos, trying to prevent those patterns. Chaos draws colored counters from a bag and places them on the board, while Order slides existing counters to form scoring patterns. After one game, players swap roles, and the highest combined score wins.

## Components

- 1 square board divided into a 7x7 grid (5x5 variant also possible)
- 49 counters: 7 each of 7 different colors
- 1 small bag

## Setup

1. Place the board between the two players.
2. Put all 49 counters in the bag.
3. Decide who plays Order and who plays Chaos first.

## Turn Structure

The game alternates between Chaos and Order actions:
1. **Chaos** draws one counter from the bag (without looking) and places it on any empty square.
2. **Order** may then slide any one counter on the board (including the one just placed) vertically or horizontally over any number of vacant squares, like a rook in chess. Only one counter may occupy a square.

This alternation continues until the board is full.

## Actions

### Chaos (Placing)
- Draw one counter blindly from the bag.
- Place it on any empty square on the board.
- Goal: prevent Order from forming patterns.

### Order (Sliding)
- After Chaos places a counter, slide any one counter on the board.
- Movement is vertical or horizontal, any number of empty squares (rook-like movement).
- Cannot move through or onto occupied squares.
- Goal: create palindromic patterns in rows and columns.

## Scoring / Victory Conditions

### Patterns
A pattern is any sequence of counters in a row or column that reads the same forwards and backwards (a palindrome). A pattern scores points equal to the number of counters it contains.

All sub-patterns within a pattern also score. For example:
- Red-Green-Blue-Green-Red scores 5 (the full pattern) + 3 (Green-Blue-Green) = 8
- Red-Green-Red-Green-Red scores 5 + 3+3+3 = 14
- Red-Red-Red-Red scores 4 + 3+3 + 2+2+2 = 16

### End of Game
When the board is completely full, score every horizontal and vertical line for patterns.

### Winning
After scoring, players swap roles (Chaos becomes Order and vice versa) and play again. The player with the higher total score across both games wins.

### Benchmarks
- Average score: approximately 75
- Good score: 100
- Poor score: 50

## Special Rules & Edge Cases

- Order can slide the counter that Chaos just placed.
- Only one counter per square at all times.
- Counters slide in straight lines and cannot jump over other counters.
- The game can also be played on a 5x5 board with 5 colors (25 counters: 5 of each).
- Tournament rules using a timing clock exist.

## Player Reference

**Board:** 7x7 grid, 49 counters (7 colors x 7 each)

**Chaos turn:** Draw 1 counter blindly, place on any empty square

**Order turn:** Slide 1 counter horizontally or vertically any distance (rook movement)

**Scoring:** Palindromic sequences in rows/columns; all sub-patterns also score

**Win condition:** Highest combined score over both games (each player plays both roles)
