---
title: "Turing Machine"
bgg_id: 356123
player_count: "1-4"
play_time: "20 min"
designer: "Fabien Gridel, Yoann Levet"
source_pdf: "turing-machine-rules.pdf"
extracted_date: "2026-03-22"
summarized_date: "2026-03-22"
---

# Turing Machine

## Overview

Turing Machine is a competitive deduction game where players race to find a secret 3-digit code by querying an analog computer made of perforated cards. Each round, players propose a code and verify it against criteria cards using a unique physical mechanism. By analyzing the yes/no responses from verifiers, players narrow down possibilities and attempt to crack the code before their opponents. The game includes 20 built-in problems plus millions more available online.

## Components

- 1 Machine tile (card holder)
- 48 Verification cards (perforated)
- 95 Criteria cards
- 1 Criteria card holder
- 5 Punch cards (number selectors)
- Note sheets (deduction grids)
- Problem booklet (20 problems)
- Rulebook

## Setup

1. Select a problem from the booklet (or generate one online at turingmachine.info).
2. Place the criteria cards specified by the problem on the criteria card holder.
3. Stack the corresponding verification cards behind each criteria card on the machine tile.
4. Give each player a note sheet and access to the punch cards.
5. Determine first player.

## Turn Structure

The game plays in simultaneous rounds:

### 1. Compose Phase
Each player secretly selects a 3-digit code by choosing three punch cards (one for each digit, values 1-5). The code consists of a triangle digit, a square digit, and a circle digit.

### 2. Verification Phase
Each player may verify their code against **up to 3 verifiers** (out of 4-6 depending on the problem). For each verification:

1. Slide your three punch cards behind the chosen verification card.
2. Look through the perforated holes to see a color: **green checkmark = your code satisfies this criterion** or **red X = it does not**.
3. Record the result on your note sheet.

You do not need to use all 3 verification attempts. Fewer verifications = better score if you solve it.

### 3. Deduction Phase
Using the results from your verifications and logical deduction, analyze your note sheet to narrow down the possible codes.

### 4. Solution Phase
If any player believes they know the secret code, they announce it. Multiple players may guess in the same round.

## Actions

- **Select Code:** Choose 3 punch cards to form a 3-digit code (each digit 1-5).
- **Verify:** Test your code against a verifier to receive a yes/no result. Maximum 3 verifications per round.
- **Deduce:** Use logic to eliminate impossible codes based on accumulated results.
- **Guess:** Announce your proposed solution.

## Scoring / Victory Conditions

**Correct Guess:** The player who correctly identifies the secret code wins. Verify the answer using the problem booklet or online tool.

**Multiple Correct Guesses:** If multiple players guess correctly in the same round, the winner is the one who used fewer total verifications throughout the game. If still tied, share the victory.

**Wrong Guess:** If a player guesses incorrectly, they are eliminated from the game. The remaining players continue.

**Solo Mode:** Try to solve the problem in as few rounds/verifications as possible. Compare your score to the difficulty rating.

## Special Rules & Edge Cases

- **Verification Limit:** Maximum 3 verifications per round. You may verify with fewer or none.
- **Verification Honesty:** The physical mechanism ensures results are objective and tamper-proof.
- **Criteria Types:** Criteria test various properties of digits: comparisons between digits, sums, counts of even/odd numbers, specific digit values, ascending/descending patterns, etc.
- **Problem Difficulty:** Problems range from easy (4 verifiers, few criteria) to extremely hard (6 verifiers, complex criteria). Difficulty ratings indicate expected rounds to solve.
- **Online Problems:** The turingmachine.info website generates millions of unique problems beyond the 20 included.
- **Nightmares Mode:** Advanced variant where some criteria are deceptive or have hidden conditions.
- **Note Sheet Strategy:** The deduction grid helps track which codes are possible. Cross-referencing multiple verifier results is key.
- **No Repeat Verifiers:** You cannot verify with the same verifier twice in one round.
- **Code Range:** Each digit is 1-5, making 125 possible codes (5x5x5).

## Player Reference

| Phase | Action | Limit |
|---|---|---|
| Compose | Choose 3-digit code | 1 code per round |
| Verify | Check code vs verifier | Up to 3 per round |
| Deduce | Analyze results | No limit |
| Guess | Announce solution | Optional, eliminates if wrong |

**Code:** 3 digits, each 1-5 (125 possible codes)

**Green = criterion satisfied | Red = criterion not satisfied**

**Victory:** First correct guess (fewest verifications breaks ties)
