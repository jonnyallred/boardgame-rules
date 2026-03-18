---
name: research-games
description: Bulk-research boardgame rules by dispatching parallel subagents. Each subagent finds PDFs, extracts text, and writes rule summaries for a batch of games. Use when the user wants to add many games at once from a candidates file.
---

# Research Games Skill

Bulk-research and add boardgame rule summaries by dispatching parallel subagents.

## Input Format

The user provides a candidates file path and optional parameters:

```
candidates.txt
candidates.txt --batch-size 20 --parallel 2
```

**Candidates file format:** one game per line, `Name (bgg_id)`:
```
Wingspan (266192)
Everdell (199792)
Root (237182)
```

**Defaults:** `--batch-size 80`, `--parallel 3`

## Main Agent Workflow

### Step 1: Parse Arguments

Parse the input to extract:
- `file`: path to candidates file (required, first positional arg)
- `--batch-size N`: games per subagent (default: 80)
- `--parallel N`: max concurrent subagents (default: 3)

Read the candidates file. Parse each line with regex: `^(.+) \((\d+)\)$` to extract name and bgg_id.

### Step 2: Detect Slug Collisions

Slugify each game name (lowercase, replace non-alphanumeric runs with `-`, strip leading/trailing `-`). Check for duplicate slugs. If collisions found, print a warning listing the colliding games and skip duplicates (keep the first occurrence).

### Step 3: Register Games

Register all candidate games in `games.yaml` using the registry module. For each game:

```bash
source .venv/bin/activate && python3 -c "
from scripts.registry import add_game
add_game('games.yaml', name='<GAME_NAME>', bgg_id=<BGG_ID>, status='queued')
"
```

Skip games that are already in the registry (add_game handles this by bgg_id check). Print count of newly registered vs skipped.

### Step 4: Chunk and Dispatch Subagents

Split the game list into chunks of `batch-size`. Dispatch one Agent per chunk, up to `parallel` at a time.

Each Agent call should use:
- `subagent_type`: `general-purpose`
- `description`: `"Research games batch N"`
- The prompt must include:
  1. The full game list for this chunk as a JSON array of `{"name": "...", "bgg_id": N, "slug": "..."}` objects
  2. The complete subagent instructions (see Subagent Instructions below)
  3. The working directory path

If there are more chunks than `parallel`, wait for the first wave to complete before dispatching the next wave.

### Step 5: Collect Results and Update Registry

Each subagent returns a results summary. Parse the results and update `games.yaml` for each game:

```bash
source .venv/bin/activate && python3 -c "
from scripts.registry import update_game
update_game('games.yaml', '<GAME_NAME>', status='<STATUS>', notes='<NOTES>')
"
```

Status values: `summarized`, `not_found`, `flagged`

### Step 6: Update index.md

For each successfully summarized game (where `rules/<slug>.md` exists and is valid), add a row to the Available Games table in `index.md`:

```
| [Game Name](rules/<slug>/) | <player_count> | <play_time> | <designer> |
```

Insert in alphabetical order within the existing table. Read `index.md` first, find the table, and insert each new row at the correct position.

### Step 7: Report Results

Print a summary:

```
## Research Complete

| Status | Count |
|--------|-------|
| Summarized | N |
| Not Found | N |
| Flagged | N |
| Total | N |

### Flagged Games (need attention)
- Game Name: <reason>
```

---

## Subagent Instructions

Include these instructions verbatim in each subagent's prompt:

---

You are processing a batch of boardgames. For each game in your assigned list, perform the following steps sequentially. Work through the ENTIRE list — do not stop early.

**Working directory:** Use the provided working directory path for all file operations.

**For each game (name, bgg_id, slug):**

#### 1. Find the Rulebook PDF

Search for an English rulebook PDF in this priority order:

**a) 1j1ju.com** — This site hosts many boardgame rulebooks.
- Try WebFetch: `https://www.1j1ju.com/regle/<slug>` (French site, but hosts English PDFs)
- Also try: `https://en.1jour-1jeu.com/rules/<slug>/`
- Look for a direct PDF download link on the page

**b) Google Search** — Search for the rulebook.
- WebSearch: `"<game name>" rulebook filetype:pdf`
- WebSearch: `"<game name>" rules pdf`
- Look for links from publishers, BGG, or rulebook hosting sites
- Prefer official publisher PDFs when available

**c) BGG Files Page** — Check the game's BGG page.
- WebFetch: `https://boardgamegeek.com/boardgame/<bgg_id>/files`
- Look for English rulebook files

If no PDF is found after all three sources, record the game as `not_found` with a note explaining what was tried, and move to the next game.

#### 2. Download the PDF

```bash
source .venv/bin/activate && python3 -c "
import urllib.request
urllib.request.urlretrieve('<PDF_URL>', 'source_pdfs/<slug>-rules.pdf')
"
```

Verify the download: check the file exists and is >10KB. If download fails, record as `flagged` with the error.

#### 3. Extract Text

```bash
source .venv/bin/activate && python -m scripts.extract_pdf source_pdfs/<slug>-rules.pdf
```

If extraction produces very little text (<500 chars), try with pdfplumber:
```bash
source .venv/bin/activate && python -m scripts.extract_pdf source_pdfs/<slug>-rules.pdf --method pdfplumber
```

Read the extracted file at `extracted/<slug>-rules.txt`. If it's still inadequate (<500 chars), record as `flagged` with note "extraction produced insufficient text".

#### 4. Write Rules Summary

Read the extracted text from `extracted/<slug>-rules.txt`. Write a comprehensive rules summary to `rules/<slug>.md`.

**Format — YAML frontmatter:**
```yaml
---
title: "<Game Name>"
bgg_id: <bgg_id>
player_count: "<range>"
play_time: "<range> min"
designer: "<name>"
source_pdf: "<slug>-rules.pdf"
extracted_date: "2026-03-17"
summarized_date: "2026-03-17"
---
```

Fill in player_count, play_time, and designer from the extracted text. If not found, omit those fields (title and bgg_id are required).

**Format — required sections (H2 headings):**
1. `## Overview` — What the game is about, core loop, victory condition
2. `## Components` — Complete inventory of all pieces, cards, tokens
3. `## Setup` — Step-by-step setup procedure
4. `## Turn Structure` — Phases within a turn, order of operations
5. `## Actions` — All available actions with full details
6. `## Scoring / Victory Conditions` — How to score, how to win, end-game triggers
7. `## Special Rules & Edge Cases` — Exceptions, corner cases, commonly missed rules
8. `## Player Reference` — Quick-reference tables, key numbers, phase checklists

**Quality guidelines:**
- Precision over brevity — include ALL exact numbers, thresholds, costs, limits
- Include every edge case and exception from the rulebook
- Use tables for structured data (costs, scoring, etc.)
- Use bullet lists for sequential steps or inventories

#### 5. Validate

```bash
source .venv/bin/activate && python -m scripts.validate rules/<slug>.md
```

If validation fails, fix the issues (usually missing sections or frontmatter fields) and re-validate.

#### 6. Record Result

After processing each game, track the result. At the end, return a summary of ALL results in this exact format:

```
RESULTS_START
name: <Game Name> | bgg_id: <N> | status: <summarized|not_found|flagged> | notes: <details or empty>
name: <Next Game> | bgg_id: <N> | status: <status> | notes: <details>
RESULTS_END
```

**Important rules:**
- Do NOT modify `games.yaml` — the main agent handles registry updates
- Do NOT modify `index.md` — the main agent handles this
- DO create files in `source_pdfs/`, `extracted/`, and `rules/`
- If a step fails, record the failure and continue to the next game
- Process ALL games in your list — do not stop early

---

## Common Mistakes

- **Don't dispatch subagents that modify `games.yaml`** — only the main agent writes to the registry
- **Don't forget to register games before dispatching** — subagents expect files can be written without registration
- **Don't exceed `--parallel`** — if you have 5 chunks and parallel=3, dispatch 3, wait, then dispatch 2
- **Don't skip the index.md update** — new games need to appear on the site
- **Don't forget to validate** — `python -m scripts.validate rules/<slug>.md` catches missing sections
