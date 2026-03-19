---
title: "Asteroyds"
bgg_id: 65200
player_count: "2-6"
play_time: "60 min"
designer: "Guillaume Blossier, Frédéric Henry"
source_pdf: "asteroyds-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
---

## Overview

Asteroyds is a real-time space racing game set in the Ujitos system. Players pilot spacecraft through a dangerous asteroid field, planning their moves under time pressure. The game features multiple modes: racing, targets, shooting, and drones. In the core racing mode, the goal is to take off from the platform and fly through 4 gates. Players simultaneously plan their moves within a time limit, then asteroids move according to dice, and finally spacecraft execute their planned manoeuvres.

## Components

- 1 board
- 6 spacecraft miniatures
- 1 stopwatch
- 3 dice (red, white, blue)
- 48 transparent tokens (8 per player in 6 colours)
- 36 asteroids (red, blue, white, white/red, white/blue)
- 6 Pilot tokens
- 24 Target tokens (sorted by type)
- 6 status charts
- Rules booklet

## Setup

1. Open the board and place it in the centre of the table.
2. Each player chooses a pilot and places their status chart in front of them.
3. Each player chooses a coloured craft and the transparent tokens of the same colour.
4. Place one token in the red column on the "Shield" icon of the status chart.
5. Place another token on the far left of the damage status row. Keep remaining tokens within reach.
6. Sort Target tokens by type and keep them near the board.
7. Place Pilot tokens to one side.
8. Implement the racing scenario (or chosen mode).
9. The last player to have flown becomes player one, taking the dice and stopwatch.
10. Asteroids are placed with random orientation (numbers on outlines do not all point the same direction).

## Turn Structure

Each round consists of 4 phases:

### 1. Planning (Timed)
- Player one rolls all 3 dice and places them by the board in Red/White/Blue order.
- Player one announces each die value out loud and starts the stopwatch.
- **All players simultaneously** plan their moves on their status charts by placing transparent tokens on pictograms in the 6 action columns (left to right order).
- **Time limit:** 50 seconds for beginners, 20 seconds for experts.
- When the stopwatch sounds, all players must stop immediately, even if planning is incomplete.

### 2. Moving the Asteroids
Player one stops the stopwatch. Players share the task of moving asteroids:

| Die Colour | Asteroids Affected | Movement | Blocking Rule |
|---|---|---|---|
| Red | Red asteroids, red gates, white/red asteroids | 2 spaces | Stops at last available space if blocked |
| White | White asteroids, white gates, white/red, white/blue asteroids | 1 space | Move is void if blocked |
| Blue | Blue asteroids, white/blue asteroids | 1 space | Pushes one other asteroid 1 space (if destination is free); blocked by craft/pods/platforms |

**Priority rule:** When two elements of the same colour target the same space, the one with the smallest priority number (shown in centre of asteroid) moves first and completes its full move.

### 3. Flying
In turn order, each player executes their planned moves from left to right on their status chart:

| Action | Effect |
|---|---|
| Move forward | Craft advances 1 hexagon |
| Move right | Craft pivots 1 notch right, then moves 1 hexagon |
| Move left | Craft pivots 1 notch left, then moves 1 hexagon |
| Turn back | Craft reverses orientation within current hexagon |
| Shield | Keeps energy shield active (reduces collision damage by 1) |

- If a craft collides with an asteroid, border, or fixed object, its planned progression **stops immediately**.
- Multiple spacecraft may occupy the same space (they cannot collide with each other).

### 4. End of Round
- Each player resets their status chart: reactivate shield, remove all tokens except the damage tracker.
- The player to the left of current player one becomes the new player one.

## Actions

### Collisions and Damage

Damage is tracked on the damage status row. If the last space is reached, the craft is **destroyed**.

| Collision Type | Damage (no shield) | Damage (shield active) |
|---|---|---|
| Asteroid hits craft (during asteroid movement) | 1 point | 0 points |
| Craft hits fixed object (border, platform, pod) | 2 points | 1 point |
| Craft hits asteroid | 2 points | 1 point |

### Destroying an Asteroid
- Once per game, a player may choose to destroy an asteroid their craft collides with.
- Cost: 4 damage points (3 with shield active).
- The pilot **must** have enough remaining damage capacity; otherwise the craft crashes and the asteroid stays.
- The destroyed asteroid is removed from the game.

### Gates
- Gates move like asteroids of their colour but can be **crossed without damage**.
- When a craft ends on the same space as a gate (by either gate or craft movement), the player takes a Target token matching the gate's symbol (unless they already have one for that symbol).

## Scoring / Victory Conditions

### Racing Mode
- The game ends when a player collects all 4 gate Target tokens (one per gate).
- The round continues to completion to check if other players also finish.
- **Tiebreaker:** The player who crossed their final gate earliest in the planning sequence (leftmost column) wins. If still tied, the player with the least accumulated damage wins.

### Targets Mode (Team Play)
- Two teams; each must destroy targets on the opposing side of the board.
- First team to eliminate all 6 of their assigned targets wins.

### Shooting Mode
- Like racing, but gates must be shot rather than crossed. Gates cannot be passed through and cause collision damage.

### Drones Mode
- Turrets send out drones (white/red movement, behave as asteroids).
- Drones have priority over asteroids; can be pushed by blue asteroids.
- First player to shoot 4 drones with different symbols wins. Tiebreaker: least damage.

## Special Rules & Edge Cases

- **Shield default:** The shield is automatically active at the start of each turn. Using the red energy column for other purposes deactivates it.
- **Asteroid orientation:** At setup, asteroid numbers are placed in random orientations; they do not all face the same direction.
- **Platform re-entry:** After takeoff, the platform becomes an obstacle and cannot be returned to (unless variant rules allow it).
- **Multiple drone kills:** If multiple players shoot the same drone in one round, they all receive a token. Order of shooting does not matter.
- **Difficulty variants:** Players may require returning to centre after completing gates; players may randomise die colour order each turn.
- **Reduced difficulty:** Remove some asteroids if the game feels too hard.

### Advanced Rules: Pilot Special Powers
Each pilot has a unique one-use ability activated by placing their Pilot token in a planning column:

| Pilot | Power |
|---|---|
| Hector | Moves forward twice |
| Dolorosa | Turns back and moves forward |
| Lawrence | Emergency shield cancels 1 damage (decided at damage time, not during planning) |
| Yayenek | Moves backward 1 space without changing orientation |
| M'Hand | Pivots twice before moving (left or right) |
| 1634 | Pivots once or twice without moving (left or right) |

## Player Reference

**Turn Sequence:** Roll dice → Start timer → Plan simultaneously → Stop timer → Move asteroids (Red → White → Blue) → Fly in turn order → Reset status charts → Pass dice left.

**Planning Time:** 50s (beginner) / 20s (expert)

**Movement Actions:** Forward, Right, Left, Turn Back, Shield

**Damage Thresholds:**
- 1 damage: asteroid-on-craft collision (shielded: 0)
- 2 damage: craft-on-object or craft-on-asteroid collision (shielded: 1)
- 4 damage: destroy asteroid (shielded: 3)

**Win Condition (Racing):** Collect all 4 gate tokens
