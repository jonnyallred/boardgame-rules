---
title: "Pax Pamir: Second Edition"
bgg_id: 256960
player_count: "1-5"
play_time: "45-120 min"
designer: "Cole Wehrle"
source_pdf: "pax-pamir-second-edition-rules.pdf"
extracted_date: "2026-03-03"
summarized_date: "2026-03-03"
rulebook_version: "Second Printing (2020)"
---

# Pax Pamir: Second Edition

## Overview

Players assume the roles of nineteenth-century Afghan leaders attempting to forge a new state after the collapse of the Durrani Empire. The game is a tableau-building card game set on a map of Afghanistan during the period known as "The Great Game." Players purchase cards from a central market and play them into their court (a single row of cards in front of them). Playing cards places units on the map and grants access to card-based actions that disrupt opponents and shape the political landscape. Players organize into one of three coalitions -- British (pink), Russian (yellow), or Afghan (green) -- and can change loyalty throughout the game. Victory points are awarded during Dominance Checks (special event cards). If a single coalition is dominant, loyal players score based on influence; if no coalition is dominant, all players score based on their personal presence on the board. The game ends either when a player leads by 4+ victory points after any Dominance Check, or after the final Dominance Check is resolved.

## Components

### Map
- 6 regions: Herat, Kabul, Kandahar, Punjab, Persia, Transcaspia
- Regions are connected by borders where roads can be placed
- Victory point track around the border
- Favored suit marker space

### Coalition Blocks (36 total)
- 12 blocks per coalition (British/pink, Russian/yellow, Afghan/green)
- A block in a region = **army** (placed upright)
- A block on a border = **road** (placed on its side)
- Coalition blocks only help players currently loyal to that coalition

### Player Cylinders (11 per player, 55 total)
- 1 gold-design cylinder per player for the VP track
- 10 remaining cylinders per player, representing:
  - **Tribe** when placed in a region
  - **Spy** when placed on a court card
- Cylinders always belong to their owner regardless of loyalty changes

### Money Supply
- 36 coins, each worth 1 rupee
- Rupees represent political capital (largely zero-sum)

### Cards (142 total)
- **Court cards (100):** The main cards players purchase and play. Each has a region, suit, rank (1-3 stars), card-based actions, and impact icons. Some have special abilities, prizes, and/or patriot status.
- **Event cards (16):** Resolved immediately when purchased or when discarded from the market during cleanup. 4 of these are **Dominance Check** cards that trigger scoring. Each event card has a top effect (triggered on discard) and a bottom effect (triggered on purchase).
- **Wakhan AI cards (24 + 2 aid):** Used only for the solo/two-player automated opponent.

### Other Pieces
- Ruler tokens (1 per region)
- Loyalty dials (1 per player)
- Player boards (1 per player)
- Favored suit marker

### Court Card Anatomy
- **Region:** Where the card is based (affects play bribes, impact icon placement, and the Overthrow Rule)
- **Suit:** Economic, Military, Political, or Intelligence
- **Rank:** 1-3 stars; determines action strength and contributes to suit privileges
- **Card-based actions:** Up to 3 action icons per card
- **Impact icons:** Resolved top-to-bottom when the card is played
- **Special ability (some cards):** Text box with a persistent effect while in court
- **Prize (some cards):** Can be claimed via the betray action; counts as influence
- **Patriot (some cards):** Colored bar indicating coalition loyalty; playing a patriot of a different coalition forces a loyalty change

## Setup

1. **Starting Favored Suit:** Place the favored suit marker on the political suit.
2. **Build the Draw Deck:**
   - Separate court cards and event cards.
   - Shuffle court cards. Create 6 face-down piles, each with 5 + (number of players) court cards. Remaining court cards are removed from the game.
   - Remove the 4 Dominance Check event cards. Place 1 in each of the 4 rightmost piles (#3, #4, #5, #6).
   - Shuffle remaining event cards. Place 2 in pile #2, and 1 in each of piles #3 through #6. The 6 remaining event cards are removed from the game.
   - Separately shuffle each of the 6 piles. Stack them so that the 4 piles containing Dominance Checks are on the bottom (pile #1 on top, pile #6 on bottom). Do NOT shuffle the combined deck.
3. **Create the Market:** Draw cards to fill a 2-row x 6-column grid (12 cards total). Fill each column top-first, starting from the leftmost column. Place the draw deck to the right of the market.
4. **Player Pieces:** Each player receives 11 cylinders, 1 loyalty dial, 1 player board, and 4 rupees. Place 1 cylinder per player on the 0 space of the VP track; remaining cylinders go on the player board.
5. **Bank and Blocks:** Place remaining coins and coalition block tray nearby.
6. **Starting Loyalty:** Starting with a random player and proceeding clockwise, each player chooses a starting loyalty (British, Russian, or Afghan). The last player to choose takes the first turn.

## Turn Structure

Each turn consists of **up to 2 actions** followed by **cleanup**. Bonus actions (from cards matching the favored suit) do not count against the 2-action limit. A player may choose to take fewer than 2 actions (including zero).

### Actions Available

Every player always has access to:
- **Purchase** (core action)
- **Play** (core action)

Additionally, each court card grants access to the actions printed on it. Each card can only be used for **one action per turn**, even if it has multiple action icons.

### Cleanup (4 steps, in order)

1. **Court limit:** If you have more court cards than 3 + (sum of purple/political stars in your court), discard court cards down to the limit.
2. **Hand limit:** If you have more hand cards than 2 + (sum of blue/intelligence stars in your court), discard hand cards down to the limit.
3. **Discard leftmost market events:** Discard any event cards in the leftmost market column (top row first, then bottom row). Rupees on discarded events stay in their position. Resolve the top-of-card effect for each discarded event (affects all players).
   - **Instability:** If a Dominance Check card is revealed during market refill and there is already a Dominance Check in the market, immediately perform a Dominance Check, then discard both Dominance Check cards and refill. If the final Dominance Check is discarded this way, it counts as the final check.
4. **Refill the market:** Slide all remaining market cards (with their rupees) leftward to fill gaps. Draw new cards to fill rightmost empty spaces. If a card slides into a space with rupees from a previously discarded event, those rupees go onto the new card.

## Actions

### Core Actions

#### Purchase

Buy a card from the market and add it to your hand. Receive any rupees already on the purchased card.

**Cost:** Depends on the card's column position (0-indexed from left):

| Column | 1 (leftmost) | 2 | 3 | 4 | 5 | 6 (rightmost) |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| Cost (rupees) | 0 | 1 | 2 | 3 | 4 | 5 |

Pay by placing 1 rupee on each card in the same row to the left of the purchased card. If a market slot is vacant, pay to the card in the same column in the other row. **You cannot purchase a card you placed a rupee on this turn.**

**Military favored:** If the military suit is favored, purchase costs are **doubled** (place 2 rupees per card to the left instead of 1).

**Event cards:** Event cards (including Dominance Checks) are resolved immediately upon purchase -- they never enter a player's hand. Persistent events are placed below your court or near the map.

#### Play

Play a card from your hand to your court (added to either the left or right end).

**Bribe:** If another player rules the card's region, you must pay them a bribe equal to the number of their tribes in that region. The ruler may waive any portion. If no one rules the region (or you rule it), no bribe is needed. If you decline to pay, you keep your action (it is not spent).

**Patriots:** If the card is a patriot whose coalition does not match your current loyalty, you must first discard all your current patriots and prizes, remove all gifts, and change your loyalty dial to match the patriot.

**Impact Icons (resolved top to bottom after playing):**

| Icon | Effect |
|------|--------|
| Army | Place 1 coalition block of your loyalty in the card's region |
| Road | Place 1 coalition block of your loyalty on any border of the card's region |
| Tribe | Place 1 of your cylinders in the card's region |
| Spy | Place 1 of your cylinders on any court card (any player) matching the played card's region |
| Rupees (Leveraged) | Take 2 rupees from the bank. Card is leveraged -- if later discarded, you must return 2 rupees (for each rupee you cannot pay, discard 1 card from hand or court) |
| Favored Suit Change | Move the favored suit marker to the indicated suit |

### Card-Based Actions

These actions require a court card displaying the corresponding action icon. Each card can be used for only **one** action per turn.

**Bonus Actions:** Actions taken with cards matching the current favored suit are free (do not count against the 2-action limit). Each card can still only be used once per turn.

**Action Costs:** Some actions require paying rupees to the market. Pay by placing rupees on the rightmost market cards (1 rupee per card, both rows), skipping vacant slots. If you place a rupee on a market card, you cannot purchase it this turn. If the market has fewer cards than the cost, excess rupees are removed from the game.

**Hostage Rule:** If a single enemy player has more spies on your court card than every other player, that card's actions are held hostage. You must pay a bribe to the hostage-holder equal to their number of spies on the card to use any action on it. The holder may waive any portion. Special abilities are never held hostage.

#### Tax

Take rupees up to the acting card's rank from:
- **Players** who have at least one court card associated with a region you rule, AND/OR
- **Market cards** (regardless of region)

You may split across multiple sources as long as the total does not exceed the card's rank.

**Tax Shelter:** A player's gold/economic stars in their court protect that many rupees from taxation. Only rupees held in excess of the tax shelter are vulnerable.

#### Gift

Place 1 of your cylinders on an empty gift space on your loyalty dial. Each gift counts as 1 influence point in your current coalition.

| Gift Space | 1st | 2nd | 3rd |
|------------|:---:|:---:|:---:|
| Cost (rupees) | 2 | 4 | 6 |

Gifts are **lost** (cylinders returned to supply) whenever you change loyalty.

#### Build

Place up to 3 armies and/or roads among regions that you rule. Roads may be placed on any border adjacent to a ruled region. Any combination of unit types is allowed.

**Cost:** 2 rupees per unit placed (paid to the market).

You must rule the region to build there.

#### Move

Move loyal armies and/or spies a number of times equal to the acting card's rank. The same unit can be moved multiple times. Moves can be split across multiple units.

- **Armies:** Move from one region to an adjacent region. There must be a road matching the army's coalition on the border being crossed.
- **Spies:** Move along court cards (all players' courts form a single continuous clockwise track). Each move advances 1 card in either direction.

#### Betray

Discard 1 court card (any player's court, including your own) where you have at least 1 spy. All spies on the betrayed card are returned to their owners' supplies.

**Cost:** Always 2 rupees (paid to the market).

After discarding, you may take the betrayed card as a **prize** (tuck it behind your loyalty dial). If the prize's coalition differs from your current loyalty, remove all gifts, discard all prizes and patriots matching your previous loyalty, and change your loyalty dial to match the new prize.

Betrayals may trigger the leveraged penalty and/or the Overthrow Rule.

#### Battle

Start a battle at a single site: either a region on the map or a court card. Remove any combination of enemy pieces at that site equal to the acting card's rank.

**Restrictions:**
- You cannot remove more units than you have armies (in a region battle) or spies (in a court card battle) at the site.
- You cannot remove armies or roads of your own coalition's color.
- You cannot remove tribes belonging to players who share your loyalty. However, you CAN remove their spies.

**In a region:** You remove enemy tribes, armies, and/or roads (up to the card's rank, limited by your own army count there).

**On a court card:** You remove enemy spies (up to the card's rank, limited by your own spy count there).

#### Spy (Impact Icon Only)

Spies are placed via impact icons when playing cards (not a standalone action). They are placed on court cards matching the played card's region.

## Scoring / Victory Conditions

### Dominance Checks

Dominance Check event cards are resolved when purchased or when discarded from the market during cleanup. When resolved:

1. **Determine dominance:** Count coalition blocks (armies + roads) on the map for each coalition. A coalition is **dominant** if it has the most blocks AND at least **4 more** than every other coalition individually.

2. **Score based on result:**

#### Successful Check (One Coalition is Dominant)

Only players loyal to the dominant coalition score. Scoring is based on **influence points** (1 base + number of patriots in court + number of prizes + number of gifts).

| Rank | Victory Points |
|------|:--------------:|
| Most influence | 5 |
| 2nd most influence | 3 |
| 3rd most influence | 1 |

**Ties:** Add VP for tied positions and divide by number of tied players (round down). Example: two players tied for 1st each get (5+3)/2 = 4 VP.

After scoring a successful check, **remove all coalition blocks from the map**.

#### Unsuccessful Check (No Coalition is Dominant)

All players score based on **cylinders in play** (any cylinder not on the player board counts, including spies, tribes, gifts, and the VP tracker -- essentially all cylinders placed anywhere).

| Rank | Victory Points |
|------|:--------------:|
| Most cylinders in play | 3 |
| 2nd most cylinders in play | 1 |

**Ties:** Same tie-breaking method as successful checks (add and divide, round down).

### Final Dominance Check

All victory points earned during the **final** Dominance Check are **doubled**. The doubling occurs **before** any splitting for ties.

### Game End

The game ends in one of two ways:

1. **Early end:** After scoring any Dominance Check, if one player leads all others by at least **4 victory points**, that player wins immediately.
2. **Final check:** After the final (4th) Dominance Check is resolved, the game always ends. The player with the most VP wins.

### Tiebreakers (at game end)

1. Most red/military stars in court among tied players
2. Most rupees among tied players
3. Best chopan kebab cook (humorous tiebreaker from the rulebook)

## Special Rules & Edge Cases

### Loyalty and Influence

- Players are always loyal to exactly one coalition: British, Russian, or Afghan.
- Your loyalty determines which coalition blocks you place (via play/build actions).
- **Influence** = 1 (base) + number of patriots in court + number of prizes + number of gifts.
- **Changing loyalty** occurs when you play a patriot of a different coalition or take a prize of a different coalition via betray. When you change loyalty:
  1. Return all gifts to your supply.
  2. Discard all prizes and patriots matching your previous loyalty.
  3. Adjust your loyalty dial.

### Ruling a Region

To rule a region, you must have:
1. **At least 1 tribe** in the region, AND
2. A **strict plurality** of ruling pieces (more than any other individual player).

**Ruling pieces** = your tribes + armies loyal to your coalition. Enemy armies count against you even if no enemy tribes are present. If tied, no one rules.

Benefits of ruling:
- Access to the **build** action in that region
- Special taxing privileges (tax players with court cards in that region)
- Collect **bribes** from other players who play cards associated with that region

### The Overthrow Rule

- If you lose your **last tribe** in a region, immediately discard all political cards associated with that region from your court.
- If you lose the **last political card** in your court associated with a region, immediately remove all your tribes in that region.
- This is bidirectional and can cascade.

### Discarding a Court Card (General Effects)

Whenever a court card is discarded (for any reason):
- All spies on the card are returned to their owners' supplies.
- If the card has the **leveraged** icon, you must return 2 rupees to the bank. For each rupee you cannot pay, discard 1 card from your hand or court.

### The Four Suits and Star Privileges

| Suit | Color | Stars Provide |
|------|-------|--------------|
| Economic | Gold | **Tax Shelter:** Protect that many rupees from taxation |
| Military | Red | **Tiebreaker:** Used to break VP ties at game end |
| Political | Purple | **Court Size:** Base court limit is 3 + purple stars |
| Intelligence | Blue | **Hand Size:** Base hand limit is 2 + blue stars |

### Favored Suit

- One suit is always designated as favored (starts as political).
- Actions on cards matching the favored suit are **bonus actions** (do not count against the 2-action limit).
- The favored suit changes when certain cards with the favored-suit-change impact icon are played.
- **If military is favored:** Purchase costs are doubled.

### Component Limits

- If you must place a unit but have none in supply, take a piece of the required shape/color from anywhere in play (excluding pieces placed this turn). You may convert one unit type to another (e.g., take your own tribe and place it as a spy).

### Card Precedence

- Special abilities on court cards and event card effects take precedence over the standard rules whenever there is a conflict.
- Special abilities on court cards are active as long as the card remains in your court.

### Negotiation

- Players may freely discuss and coordinate during play.
- All agreements are **non-binding**.
- Cards may never be transferred between players.
- Money can only be transferred when explicitly allowed by rules (taxation, bribes, hostage payments).

### Instability (Dominance Check Timing)

If a Dominance Check card is revealed during market refill and another Dominance Check is already in the market, immediately resolve a Dominance Check, then discard both Dominance Check cards and refill the market. If the final Dominance Check is triggered this way, it counts as the final check (points doubled).

### Deck Construction Summary

| Pile | Position | Court Cards | Dominance Checks | Other Events |
|------|----------|:-----------:|:-----------------:|:------------:|
| #1 | Top of deck | 5 + n | 0 | 0 |
| #2 | 2nd | 5 + n | 0 | 2 |
| #3 | 3rd | 5 + n | 1 | 1 |
| #4 | 4th | 5 + n | 1 | 1 |
| #5 | 5th | 5 + n | 1 | 1 |
| #6 | Bottom | 5 + n | 1 | 1 |

(n = number of players)

## Player Reference

### Key Numbers

| Item | Value |
|------|-------|
| Actions per turn | 2 (bonus actions from favored suit cards are free) |
| Starting rupees | 4 |
| Starting court cards | 0 |
| Cylinders per player | 10 (+ 1 VP tracker = 11 total) |
| Coalition blocks per coalition | 12 |
| Total coins in game | 36 |
| Market size | 2 rows x 6 columns = 12 cards |
| Base court limit | 3 + purple stars |
| Base hand limit | 2 + blue stars |
| Dominance Check threshold | 4+ more blocks than each other coalition |
| Early game end threshold | 4+ more VP than all other players |

### Action Costs

| Action | Cost | Notes |
|--------|------|-------|
| Purchase | 0-5 rupees (paid to market cards left of purchased card) | Doubled if military is favored |
| Play | Bribe to ruler (0 to N rupees, N = ruler's tribes in region) | Free if you rule or no one rules |
| Tax | Free | Takes up to rank in rupees from players/market |
| Gift | 2 / 4 / 6 rupees (1st / 2nd / 3rd gift) | Paid to market |
| Build | 2 rupees per unit (up to 3 units) | Paid to market; must rule the region |
| Move | Free | Rank = number of moves |
| Betray | 2 rupees | Paid to market |
| Battle | Free | Rank = number of removals |
| Hostage bribe | N rupees (N = hostage-holder's spies on card) | Paid to holding player |

### Dominance Check Scoring

**Successful (coalition dominant):**

| Place | VP (Normal) | VP (Final Check) |
|-------|:-----------:|:----------------:|
| 1st influence | 5 | 10 |
| 2nd influence | 3 | 6 |
| 3rd influence | 1 | 2 |

**Unsuccessful (no dominant coalition):**

| Place | VP (Normal) | VP (Final Check) |
|-------|:-----------:|:----------------:|
| 1st cylinders in play | 3 | 6 |
| 2nd cylinders in play | 1 | 2 |

### Influence Calculation

Influence = 1 (base) + patriots in court + prizes held + gifts placed

### Suit Privileges Summary

| Suit | Stars Protect/Grant |
|------|-------------------|
| Gold (Economic) | Tax shelter: protect N rupees from tax |
| Red (Military) | Tiebreaker at game end |
| Purple (Political) | Court size: 3 + N cards |
| Blue (Intelligence) | Hand size: 2 + N cards |

### Loyalty Change Triggers

1. Play a patriot of a different coalition
2. Take a prize of a different coalition via betray

When changing: lose all gifts, discard previous-loyalty patriots and prizes, adjust dial.

### Battle Restrictions Checklist

- Cannot remove more units than you have at the site (armies in region, spies on card)
- Cannot remove armies/roads of your own coalition
- Cannot remove tribes of players sharing your loyalty
- CAN remove spies of players sharing your loyalty
