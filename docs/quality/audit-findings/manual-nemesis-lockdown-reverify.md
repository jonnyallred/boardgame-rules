# Re-Audit Findings — manual-nemesis-lockdown (independent re-verify)

Independent re-verification of the repair commit (`15f988e`, "Repair MAJOR audit
findings in Nemesis: Lockdown summary") applied to `rules/nemesis-lockdown.md`,
following up on the original audit in
`docs/quality/audit-findings/manual-nemesis-lockdown.md` (verdict: MAJOR).
Compared independently against `extracted/nemesis-lockdown-rules.txt`
(~3264 lines) — the original audit's claims were used only as a pointer to
what to look at, not trusted directly. Re-audited 2026-08-26.

## Verdict: PASS

All three original findings are confirmed fixed/correct against the source.
A fresh pass over victory/game-end conditions and the Player Reference
sections adjacent to the edits found nothing newly broken.

## Repair scope, confirmed via git diff

`git show 15f988e -- rules/nemesis-lockdown.md` touches exactly two hunks:
the "Autodestruction sequence" paragraph and the "Searching" bullet. The
Basic Rooms "I" / Additional Rooms "II" tables are byte-identical between the
file's first commit (`395637c`) and the repair commit — i.e. whatever state
Finding 2 describes, the table has been in its current (correct) form since
the file was first committed. This matches the repair commit's own message
("one of which had already been fixed by a pre-audit self-review"), but that
claim is not taken on faith below — the current table is checked directly
against the source instead.

---

## Finding 1 (originally MAJOR) — Search Action procedure

**Original finding:** the summary omitted that Searching draws 2 Item cards
and lets you keep 1, discarding the other to the bottom of the deck.

**Current summary** (`rules/nemesis-lockdown.md`, Special Rules & Edge Cases
→ Items and Objects → Searching):
> "A Search reduces that Room's Item Counter by 1, then draws 2 Item cards
> from the chosen deck — keep 1 and discard the other face down to the
> bottom of that deck. At Item Counter 0 the Room can no longer be
> searched."

**Source** (Survivor's Search Action card, l.1466-1472):
> "SEArCH Reduce the Item Counter by 1. Draw 2 Item cards of the same color
> as the Room you are in. Pick one and discard the other to the bottom of
> its deck."

Corroborated by the general rule (l.2637-2640: "the Item Counter of that
Room is reduced by 1. When the Item Counter reaches 0, the Room has been
emptied and cannot be searched anymore") and the worked example
(l.2619-2623: "The player decides ... to keep the Weapon Battery and
discards (face-down) the Glowstick to the bottom of the Red Item deck").

**Status: CONFIRMED FIXED.** Procedure, order of operations (reduce counter
→ draw 2 → keep 1 / discard 1 face-down to the bottom), and the Counter-0
exhaustion condition now all match the source. Checked every other mention
of Searching in the document (Actions section's "Pick Up Heavy Object"
aside, Fire/Malfunction marker notes, Nest, Contaminated Room, Special
Rooms header) for a contradicting or stale description — none found.

---

## Finding 2 (originally MAJOR) — Basic Rooms "I" table

**Original finding:** the table wrongly included CSS Rooms B/C as
always-present Basic Rooms and omitted an entire 10th Basic Room, Cave
Entrance.

**Current summary** (Player Reference → "Room Actions (Basic Rooms 'I' —
all present every game)") lists exactly 10 entries: Archive, Cave Entrance,
Cooling System, Decon Room, Emergency Room, Laboratory, Cargo Sending System
A, Nest, Power Generator, Transmitter Control Room. CSS B/C do not appear in
this list.

> "**Cave Entrance** — Move through Technical Corridors: move to a chosen
> explored Room with a Technical Corridors Entrance, then draw and resolve
> an Attack card (treat it as an Attack from an Adult Intruder in
> Darkness)."

**Source** (l.300-443, under "BASiC rooMS 'I' / All the 10 Basic Rooms,
indicated by the number 'I' on their back, are present in each game"):
walking the listing top to bottom yields exactly 10 room actions — Examine
the Archives (l.303-315); an unlabeled action (graphic room name lost in
extraction, cross-referenced elsewhere as Cave Entrance) reading "Move
through Technical Corridors: You may move to a chosen explored Room with a
Technical Corridors Entrance. Draw and resolve an Attack card (treat it as
an Attack from an Adult Intruder in Darkness)" (l.316-321); Cooling System
(l.322-334); Decontamination (l.335-342); Emergency Room (l.343-348);
Analyze 1 Object / Laboratory (l.349-363); CSS Pod A (l.364-381); Nest
(l.382-401); Power Generator (l.416-427); Transmitter Control Room
(l.428-441) — immediately followed by the header change to "ADDiTioNAL
rooMS 'II'" (l.444: "Each game, only 6 randomly chosen Additional Rooms are
used, out of the 9 available"), under which CSS Pod B (l.447-448) and CSS
Pod C (l.449-452) actually live. The Cave Entrance room name is confirmed by
two cross-references: l.1737 ("Cave Entrance Room Action") and l.3126
("Cave Entrance Room Action").

The current summary's Additional Rooms "II" section correctly places CSS
B/C there instead, alongside 7 other rooms (CSS Control System, Defense
Control Room, Guard Room, Contaminated Room, Surgery, Testing Lab, Vent
Control Room) — 9 total, matching "9 available." Room names spot-checked
against source cross-references: "Guard Room" at l.1788, "Surgery Room" at
l.2224/l.2238/l.3175.

**Status: CONFIRMED CORRECT.** Both the 10-room Basic "I" list and the Cave
Entrance action text match the source exactly; CSS B/C are absent from Basic
"I" and present in Additional "II," as the source requires. (As noted above,
git history shows this section was never touched by the repair commit — it
has read this way since the file's first commit — but it is verified here
directly against the source rather than assumed correct from that history.)

---

## Finding 3 (originally MINOR) — Autodestruction misattribution

**Original finding:** the summary attributed the "still usable after an
Isolation Room lock-in" exception to the Power Generator's Stop
Autodestruction Action, when the source's highlighted exception is that the
sequence can still be *initiated* (Cooling System) after a lock-in.

**Current summary** (Special Rules & Edge Cases → Autodestruction sequence):
> "while yellow, it can still be stopped via the Power Generator's Stop
> Autodestruction Action. The sequence can still be *initiated* via the
> Cooling System even after a Character has already locked into the
> Isolation Room."

**Source** (l.986-990):
> "IMPORTANT: The sequence can still be initiated, even when any Character
> has already locked themselves in the Isolation Room! More on initiating
> Autodestruction sequence – see Room sheet, page 27."

Corroborated by the Isolation Room's own "CHANGE" callout (l.2989-2991):
"Other Players still can initiate the Autodestruction sequence when a
Character is already locked in the Isolation Room."

**Status: CONFIRMED FIXED.** The "stopped" and "initiated" claims are now
two separate sentences, each correctly attributed: the Stop-via-Power-
Generator sentence carries no lock-in caveat (correct — the source states no
such restriction on Stop), and the lock-in exception is attached only to
"initiated" via the Cooling System. This is now also consistent with the
parallel statement in Player Reference → Special Rooms → Isolation Room
("Other Characters can still start Autodestruction after someone has locked
in.").

---

## Fresh pass (per instructions: lighter, but real, since core systems were already checked once)

**Victory / game-end conditions** — re-checked directly against source
(untouched by the repair, but re-verified rather than trusted from the prior
audit's account):
- Win condition (Objective + Survive via Isolation Room / CSS Pod / Bunker):
  matches l.855-861 exactly, including the "not cooperative, other players'
  success is irrelevant" framing (l.851-854).
- All 3 end-of-game triggers match l.1143-1168 in both directions: final
  "S" slot purge with Intruders surviving and Queen/Nest objectives failing
  (l.1143-1148); Autodestruction-blocked-advance OR 13th Fire / 11th
  Malfunction destroying everyone including Isolation-Room Characters and
  the Queen (l.1149-1154); last-living-Character trigger with the dual
  Alert-Procedure/Autodestruction handling, "they both count as the way of
  ending the game" (l.1156-1168).
- 3-step Victory Check (Contingency → Contamination → Objective) matches
  l.1172-1208 exactly, including the Contamination check's Scanner/
  skip-to-step-B-if-already-Larva logic and the draw-top-4 rule.
- Objective-type definitions (l.864-934: Player X cannot survive, only
  survivor, no Nemesis Survivor, Send the Signal, Discover a Weakness,
  Destroy the Nest, Knowledge X, Activate Knowledge token, explore Sections
  X/Y) all match the summary's "Objective types" list.
No discrepancies found in either direction.

**Player Reference entries near the edited Basic/Additional Rooms tables**,
spot-checked against source:
- All 10 Basic Rooms "I" entries checked sense-for-sense against
  l.303-441 (see Finding 2) — accurate, including the Archive's
  peek-then-keep-the-token detail (l.918-920 vs. l.309-310+353 region) and
  the Nest's "no Searching / Malfunction never placed here" caveats
  (l.398-401).
- All 9 Additional Rooms "II" entries spot-checked against l.444-510 —
  accurate (CSS Control System's move restrictions, Defense Control Room's
  Item-Counter-or-Malfunction cost choice, Vent Control Room's
  door-reopened/Player-Phase-end timing all match).
- Special Rooms section (Alert Room, Backup Power Supply, Elevator Rooms,
  Emergency Staircases, Repository, Isolation Room), checked against
  l.2899-2991 — all 6 entries accurate, including the Repository's
  "only one of two Component symbols needed" build discount (l.2963-2968)
  and the Isolation Room's Malfunction exception on its passive card draw
  (l.2973-2975).
- "Critical gameplay moments" list checked against l.935-943 — all 4
  moments match, including the 4th ("Autodestruction becomes unstoppable" —
  correctly about the Stop ability ending, distinct from the Finding-3
  "initiated" exception, so the two nearby claims do not contradict each
  other).

**Nothing new found.** No invented mechanics, no reversed claims, no new
numeric errors, and no formatting/markdown damage in or around either edited
paragraph (verified both by direct reading and by the git diff showing a
clean two-hunk change with no stray edits elsewhere).

---

## Verdict

**PASS.** Both original MAJOR-contributing findings (Search Action
procedure; Basic Rooms "I" table) are fixed correctly and completely, and
the MINOR finding (Autodestruction misattribution) is fixed correctly. The
repair was surgical (confirmed via `git show 15f988e`) and introduced no new
errors in the edited text or its immediate surroundings. The fresh pass over
victory/game-end conditions and the adjacent Player Reference sections found
nothing further.

| Slug | Verdict |
|---|---|
| nemesis-lockdown | PASS |
