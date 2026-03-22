---
title: "Mastermind"
bgg_id: 2392
player_count: "2"
play_time: "20 min"
designer: "Mordecai Meirowitz"
source_pdf: "mastermind-rules.pdf"
extracted_date: "2026-03-21"
summarized_date: "2026-03-21"
---

## Overview

Mastermind is a classic code-breaking game for 2 players. One player (the Codemaker) creates a secret code of 4 colored pegs, and the other player (the Codebreaker) tries to deduce the code through a series of guesses, receiving feedback after each attempt. The game challenges deductive reasoning and logical elimination.

## Components

- 1 game board with rows of peg holes and a hidden code area
- Code pegs in 6 colors (red, blue, green, yellow, white, black)
- Key pegs in 2 colors (black and white, smaller pegs for feedback)
- Shield to hide the code

## Setup

1. Place the board between players with the shield at one end.
2. The Codemaker creates a secret code: place 4 colored pegs in any order behind the shield. Colors may be repeated. Blanks may optionally be used as a 7th "color."
3. The Codebreaker sits on the opposite side.

## Turn Structure

The game proceeds through a series of guesses (typically up to 10 or 12 rows):

1. The **Codebreaker** places 4 colored pegs in the first available row as their guess.
2. The **Codemaker** provides feedback using key pegs:
   - **Black key peg:** Correct color in the correct position.
   - **White key peg:** Correct color but wrong position.
   - **Empty hole:** That color is not in the code (or all instances are accounted for).
3. The Codebreaker uses the feedback to refine their next guess.
4. Play continues until the code is solved or all rows are used.

## Actions

### Making a Guess
Place 4 pegs in the current row, choosing any combination of the available colors.

### Providing Feedback
The Codemaker places key pegs for each correct element:
- 1 black peg per correct color in correct position
- 1 white peg per correct color in wrong position
- Key pegs are placed in any order (their position does not correspond to specific guess pegs)

## Scoring / Victory Conditions

### Single Round
- If the Codebreaker solves the code, count the number of guesses used. This is their score.
- If the Codebreaker fails to solve the code within the allowed guesses, the Codemaker wins that round.

### Multi-Round Game
Players alternate roles. After an agreed number of rounds, the player with the lowest total score (fewest guesses) wins.

## Special Rules & Edge Cases

- **Duplicate colors:** The code may contain the same color multiple times. Feedback must be precise about duplicates.
- **Key peg priority:** Black pegs (exact matches) are assigned first, then white pegs for remaining matches.
- **Advanced variant:** Allow blank spaces in the code as a 7th option, making deduction harder.
- The Codemaker must provide honest and accurate feedback -- incorrect feedback invalidates the game.
- With 6 colors and 4 positions (with repeats), there are 1,296 possible codes.

## Player Reference

| Key Peg | Meaning |
|---------|---------|
| Black | Right color, right position |
| White | Right color, wrong position |
| Empty | Color not in code (or already matched) |

**Standard game:** 6 colors, 4 positions, 10-12 guesses allowed
