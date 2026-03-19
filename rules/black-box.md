---
title: "Black Box"
bgg_id: 165
player_count: "1-2"
play_time: "30 min"
designer: "Eric Solomon"
source_pdf: "black-box-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
---

## Overview

Black Box is a deduction board game for 1–2 players designed by Eric Solomon. One player (the codemaker) secretly places a number of "atoms" (balls) inside an 8×8 grid. The other player (the codebreaker) fires rays from the edges of the grid to determine where the hidden atoms are located. Rays interact with atoms in predictable ways — they can be absorbed, deflected, or reflected. Using the results of each probe, the codebreaker deduces atom positions. The goal is to locate all hidden atoms using the fewest probes and incurring the lowest score (lower is better).

## Components

- 1 game board with an 8×8 grid and 32 numbered entry/exit ports along the edges (8 per side)
- 4–5 atom balls (yellow balls in the Parker Brothers edition; metal balls in the Waddingtons edition)
- Ray markers or tokens to track entry/exit points
- Score pad or scoring track

## Setup

1. Place the game board between the two players so the codemaker can see inside the grid and the codebreaker cannot (or use a screen/shield).
2. The codemaker secretly places the agreed number of atoms (typically 4 or 5) on squares within the 8×8 grid.
3. The codebreaker prepares to track probe results.

## Turn Structure

The game is played in a series of probes:

1. **Fire a Ray**: The codebreaker selects an entry port along the edge of the grid and announces it.
2. **Determine Result**: The codemaker traces the ray's path through the grid according to the interaction rules and announces the result:
   - **Hit (H)**: The ray struck an atom directly — it is absorbed and does not exit.
   - **Reflection (R)**: The ray was reflected back out its entry port.
   - **Detour**: The ray exits at a different port — the codemaker announces the exit port number.
   - **Miss**: The ray passes straight through and exits directly opposite (this is a special case of detour).
3. **Record Result**: The codebreaker marks the result on their tracking sheet.
4. **Repeat**: Continue firing rays until the codebreaker feels confident about the atom positions.
5. **Guess**: The codebreaker announces their guesses for all atom positions.
6. **Reveal and Score**: The codemaker reveals the actual positions and the score is calculated.

## Actions

### Ray Interactions
- **Straight Path**: A ray with no atoms nearby travels in a straight line through the grid and exits directly opposite.
- **Hit**: A ray aimed directly at an atom is absorbed. The result is "H" and the ray does not exit. Costs 1 point.
- **Deflection**: When a ray passes to the immediate side of an atom (diagonally adjacent), it deflects 90° away from the atom. Multiple deflections are possible in a single ray path.
- **Reflection**: Occurs when (a) an atom sits at the edge and the ray enters the adjacent port, or (b) two deflections cancel out, sending the ray back the way it came. The result is "R." Costs 1 point.
- **Detour**: A ray that is deflected one or more times and exits at a different port from where it entered. Both entry and exit ports are marked. Costs 2 points (1 for entry + 1 for exit).

### Deduction
- The codebreaker uses the accumulated probe results to reason about which squares must contain atoms.
- Patterns of hits, reflections, and detour paths constrain possible atom locations.

## Scoring / Victory Conditions

- **Hits and Reflections**: 1 point each.
- **Detours**: 2 points each (1 for entry port + 1 for exit port).
- **Misidentified atoms**: 5 points penalty per incorrect guess (Parker Brothers edition) or 10 points (Waddingtons edition).
- **Correctly placed atoms**: No additional cost.
- The codebreaker's total score is the sum of probe costs plus any penalties.
- **Lower score is better.** Players typically switch roles and play again, with the lower combined score winning.

## Special Rules & Edge Cases

- A ray entering a port immediately adjacent to an atom at the grid edge is reflected (R), not deflected.
- A ray can be deflected multiple times by multiple atoms on a single path.
- Two atoms side by side can create a "tunnel" that deflects a ray around them.
- In solitaire mode, one player places atoms randomly (or has a partner place them) and attempts to solve the puzzle.
- The Parker Brothers edition uses 5 atoms; the Waddingtons edition typically uses 4.
- If a ray would be simultaneously deflected in two opposite directions, it is reflected.

## Player Reference

| Ray Result | Description | Point Cost |
|-----------|-------------|------------|
| Hit (H) | Ray strikes atom directly | 1 |
| Reflection (R) | Ray bounces back to entry | 1 |
| Detour | Ray exits at different port | 2 |
| Miss | Ray passes straight through | 2 |

| Penalty | Points |
|---------|--------|
| Incorrect atom guess (Parker Bros) | 5 per atom |
| Incorrect atom guess (Waddingtons) | 10 per atom |

| Goal | Lowest total score wins |
|------|------------------------|
