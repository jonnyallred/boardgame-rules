# Audit Findings — manual-nemesis-lockdown

Single-game manual audit (not a real pipeline batch id). Audited 2026-08-26.
`rules/nemesis-lockdown.md` compared against `extracted/nemesis-lockdown-rules.txt`
(~3264 lines). Line numbers below refer to the extracted text file.

---

## nemesis-lockdown — MAJOR

**Verdict: MAJOR** — Two confident, independently-sufficient findings: (1) the
Search Action's actual resolution procedure (draw 2 Item cards, keep 1,
discard the other) is completely absent from the summary, which instead
implies Items are simply "found"; Searching is one of the two ways to
acquire ongoing Items and is used repeatedly across a full game. (2) The
Player Reference's "Basic Rooms 'I' — all present every game" table is both
wrong (it claims CSS Rooms B and C are always-present Basic rooms, when the
source places them among the variable Additional "II" rooms — the summary's
own Additional Rooms "II" list separately, and correctly, lists them there
too) and incomplete (it omits an entire named Basic Room, "Cave Entrance",
whose Room Action is never once described even though the summary
name-drops "the Cave Entrance Room Action" elsewhere as a rule players need).
Everything else checked — victory/game-end conditions in both directions,
the 3-step Victory Check order, the Fire/Malfunction pool sizes and their
13th/11th-marker game-end triggers, the Isolation Room open condition, the
Night Stalker token Darkness mechanic, the full Turn Structure, Combat,
Contamination, Knowledge/Weakness, Power/Darkness, Game Modes, and
Nemesis-crossover sections, and dozens of component numbers — matched the
source precisely, including many places where the summary faithfully
preserves genuinely confusing/self-referential source wording (Power
Thresholds, Restore Power) rather than simplifying it incorrectly. This is
an unusually accurate summary overall; the verdict is MAJOR strictly because
of the two findings below, each of which would cause a table to misplay a
frequently-recurring core action or leave a guaranteed room's action
completely unresolved.

### Findings

1. **MAJOR — Search Action procedure omitted (draw 2, keep 1, discard the other).**
   - Summary (Items and Objects → Searching): *"Searching: Item colors are
     Red (military), Yellow (technical), Green (medical), all found via a
     Search Action card matching the searched Room's color (a white Room
     lets you pick any 1 of the 3 decks). Searching reduces that Room's Item
     Counter by 1; at 0 it can no longer be searched."*
   - Source (Survivor's actual Search Action card, l.1466-1472): *"S U R V I
     V O R SEArCH Reduce the Item Counter by 1. **Draw 2 Item cards of the
     same color as the Room you are in. Pick one and discard the other to
     the bottom of its deck.**"* Corroborated by the general rule (l.2637-2640:
     *"When searching in a white Room, the player can choose to draw from
     any 1 of these 3 decks... Item Counter of that Room is reduced by
     1..."*) and by the worked example (l.2614-2623: *"the Survivor can draw
     2 Item cards from any one Item deck... decides to keep the Weapon
     Battery and discards (face-down) the Glowstick to the bottom of the Red
     Item deck"*).
   - Impact: this is not a flavor detail — it is the entire resolution
     procedure for one of only two ways Characters acquire ongoing Items
     (Searching and Crafting; see the summary's own "Sources" list), invoked
     many times over a game. A table using only the summary would not know a
     Search draws 2 cards with a keep-1/discard-1 choice; they would likely
     assume 1 card is simply granted, materially changing the loot economy
     and hiding a real decision point (choosing which of 2 cards to keep,
     face-down, in secret) every time this action is used.

2. **MAJOR — Basic Rooms "I" reference table wrongly includes CSS Rooms B/C and omits the Cave Entrance room entirely.**
   - Summary (Player Reference): *"### Room Actions (Basic Rooms "I" — all
     present every game) ... - **CSS Rooms A/B/C** — Enter the matching CSS
     Pod (only when the Time token shares a slot with a CSS token and that
     Pod space is empty)."* The summary's own next section then says:
     *"### Additional Rooms "II" (6 of 9 appear each game) - **CSS Rooms
     B/C, CSS Control System** — as above..."* — the same two rooms are
     asserted to be both always-present and only-sometimes-present.
   - Source: CSS Room A is described under the *"BASiC rooMS "I""* heading
     (l.300-301: *"All the 10 Basic Rooms, indicated by the number 'I' on
     their back, are present in each game"*; the CSS Pod A action itself at
     l.364-365: *"System a / Enter the CSS Pod A / Cargo Sending System
     A"*). CSS Rooms B and C are instead described under the separate
     *"ADDiTioNAL rooMS "II""* heading (l.444-452: *"ADDiTioNAL rooMS "II"
     Each game, only 6 randomly chosen Additional Rooms are used, out of the
     9 available... Enter the CSS Pod B ... Enter the CSS Pod C"*) — i.e.
     the source itself places B and C in the variable pool, not the
     guaranteed one, exactly where the summary's Additional Rooms II list
     (correctly) has them.
   - Compounding the same table: the Basic Rooms "I" heading claims to list
     rooms "all present every game" but never lists a 10th real Basic Room,
     "Cave Entrance", whose action is stated in the source at l.316-321
     (immediately preceding the "Cooling System" room in the same Basic
     Rooms "I" listing): *"Move through Technical Corridors: You may move to
     a chosen explored Room with a Technical Corridors Entrance. Draw and
     resolve an Attack card (treat it as an Attack from an Adult Intruder in
     Darkness)."* The room's name is confirmed twice elsewhere in the source
     (l.1737: *"The Vents Action card from the Survivor Action deck, Cave
     Entrance Room Action and the Cave Plans Item card are the only
     exceptions to this rule"*; l.3126: *"Cave Entrance Room Action"*). The
     summary itself names *"the Cave Entrance Room Action"* in its Technical
     Corridors passage as one of the three ways to bypass Technical Corridor
     restrictions, but never once states what that action actually does or
     costs anywhere in the document.
   - Impact: (a) a table would believe all 3 CSS evacuation Pods are
     guaranteed to exist in their Facility, when 2 of the 3 are drawn from a
     pool of 9 optional tiles (only 6 used per game) and might not appear at
     all — directly relevant to planning the "evacuate via CSS Pod" survival
     path that the Victory condition depends on; (b) a table that draws the
     Cave Entrance tile (guaranteed every game) and wants to resolve its
     Room Action — a rule the summary itself flags as one of only three
     Technical-Corridor-access exceptions — has no rules text anywhere in
     the summary telling them what it does or what it costs.

3. **MINOR — "Stop Autodestruction after lock-in" note misattributed to the wrong action.**
   - Summary (Autodestruction sequence): *"while yellow, it can still be
     stopped via the Power Generator's Stop Autodestruction Action (even if
     a Character has already locked into the Isolation Room)."*
   - Source (l.986-990): *"Note: If the token would go over the Time track,
     simply place it on the last slot... IMPORTANT: The sequence can still
     be **initiated**, even when any Character has already locked themselves
     in the Isolation Room! More on **initiating** Autodestruction sequence
     – see Room sheet, page 27."* The source's highlighted exception is
     about **starting** the sequence (the Cooling System Room Action) after
     a lock-in, not about the Power Generator's ability to **stop** it. The
     correct fact is stated properly elsewhere in the same summary (Special
     Rooms → Isolation Room: *"Other Characters can still start
     Autodestruction after someone has locked in"*), so no rule is missing
     end-to-end, but this sentence reassigns a specific source callout to
     the wrong action/direction.
   - Not upgraded to MAJOR because nothing in the source suggests the Power
     Generator's Stop action is actually restricted after a lock-in, so the
     misattributed sentence does not, on its own, produce a wrong ruling at
     the table — it just cites the wrong reason.

### Verification quota completed

- **Victory / game-end / tiebreaker rules, both directions**: the 2-part
  win condition (Objective + Survive via Isolation Room/CSS Pod/Bunker,
  l.855-861), all 3 end-of-game triggers (Time token reaches final "S" slot,
  l.1143-1148; Autodestruction-blocked-advance OR 13th Fire/11th Malfunction,
  l.1149-1154; last living Character resolves, l.1156-1168), and the 3-step
  Victory Check (Contingency l.1173-1181, Contamination l.1182-1193,
  Objective l.1202-1208) all match the summary sentence-for-sentence in both
  directions — no source condition is missing from the summary and no
  summary claim is unsupported.
- **Every number in Scoring/Victory Conditions**: Fire pool 12 / 13th
  triggers destruction (l.539, 1829-1831, 1150-1151); Malfunction pool 10 /
  11th triggers destruction (l.550, 1860-1863, 1150-1151); Isolation Room
  opens at white slot "8" (l.960-962); Alert Procedure = current slot ÷ 2
  rounding down (l.1131-1133); all match.
- **≥5 procedural claims from Turn Structure/Actions**: draw to hand of 5
  (l.1220-1222); First Player token passes left, skipped round 1
  (l.1226-1229); pass forces discard of 2nd Action and locks out further
  Actions (l.1236-1242); Fire wound applies once per round even if others
  still act (l.1243-1245, matches summary l.81 exactly); Event card
  resolution order (Intruder movement then Event effect, l.1270-1290);
  Intruder bag development per-token-type effects (l.1294-1316) — all
  confirmed matching.
- **Every term-of-art the victory rules depend on**: "Survive" (three exact
  options, l.858-861), "Nemesis Survivor" (Survivor, Lab Rat, all
  Nemesis/Aftermath characters, l.887-889), each Objective-type definition
  (l.872-934) — all match the summary's Objective-types section precisely.
- **Exhaustion/pool-depletion rules**: Action deck reshuffle-from-discard
  (l.1223-1225), Event deck reshuffle (l.1291-1293), Intruder Attack deck
  reshuffle (l.2175-2177), Contamination discard-to-bottom (l.2251-2252),
  Door token pool fallback (l.1900-1902), Adult miniature 8-cap
  retreat-and-replace (l.1774-1780), Fire pool 12 / Malfunction pool 10
  destruction triggers (above) — all match; no invented reshuffle/replenish
  rule found anywhere.
- **Night Stalker Darkness mechanic**: source (l.2018-2027): *"The first,
  lower number if the Character is not in Darkness. The second, higher
  number if the Character is in Darkness"* — matches summary exactly, and
  matches the worked Encounter example (l.1983-1996, Power on → lower number
  used).
- **CSS Pods launch table (3 outcomes)**: source's 3 outcomes (l.1013-1026)
  are individually reproduced correctly by the summary without claiming to
  know which icon maps to which outcome — appropriately hedged given the
  icon graphics were lost in extraction.

### Numbers checked (24 checked, 23 supported, 1 omitted entirely)

| # | Claim | Source | OK |
|---|---|---|---|
| 1 | 12 Fire markers / 13th triggers destruction | l.539, 1829-1831, 1150-1151 | Y |
| 2 | 10 Malfunction markers / 11th triggers destruction | l.550, 1860-1863, 1150-1151 | Y |
| 3 | 27 Night Stalker tokens (8/3/12/2/1/1) | l.542-545 | Y |
| 4 | Intruder bag start: 1 Blank, 4 Larvae, 1 Creeper, 1 Queen, 3 Adults, +1/player | l.654-657 | Y |
| 5 | 7 CSS tokens, 1 returned unused | l.531, 641-643 | Y |
| 6 | 5 Eggs in Nest at setup, 3 Weakness cards | l.646-649 | Y |
| 7 | Isolation Room opens at slot "8" (white) | l.960-962 | Y |
| 8 | Knowledge thresholds 3 / 5 / 8 | l.2364, 2367 | Y |
| 9 | Analyze Object = +3 Knowledge | l.2326-2327 | Y |
| 10 | Archive Action = +2 Knowledge | l.2333, 2340 | Y |
| 11 | Discover Nest = +1 Knowledge | l.2331 | Y |
| 12 | Computer Action = +1 Knowledge | l.2330 | Y |
| 13 | Hand size 5, 6 if starting round in Isolation Room | l.1222, 2972 | Y |
| 14 | 2 Actions per turn | l.1233-1234 | Y |
| 15 | 3 Serious Wounds + 1 more = death | l.2295-2296 | Y |
| 16 | 3 Light Wounds convert to 1 Serious Wound | l.2280-2283 | Y |
| 17 | Craft Item: discard 2 Item cards | l.1413-1414, 2599-2601 | Y |
| 18 | Autodestruction: +3 slots (yellow, 2 empty between), then +3 more (red) | l.966-975 | Y |
| 19 | Alert Procedure = slot ÷ 2, rounding down | l.1131-1133 | Y |
| 20 | Neutralizer requires 4+ Knowledge | l.492-494 | Y |
| 21 | Heavy Items/Objects cap: 2 in hand | l.2491 | Y |
| 22 | Solo mode: draw 2 Objectives, 2 Neutral Pool tokens | l.2999-3002 | Y |
| 23 | Solo mode Item halving (1-2→1, 3-4→2) | l.3005-3007 | Y |
| 24 | Search Action: draw 2, keep 1, discard other | l.1469-1472 | **N (omitted from summary — see Finding 1)** |

---

## Summary

| Slug | Verdict |
|---|---|
| nemesis-lockdown | MAJOR |
