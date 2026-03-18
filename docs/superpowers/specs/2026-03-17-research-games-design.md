# Research Games Skill — Design Spec

**Date:** 2026-03-17
**Status:** Draft

## Overview

A skill and supporting script for bulk-researching and adding boardgame rule summaries. The workflow bridges the `boardgame-database` project (~3,880 games) with `boardgame-rules` (~22 games) by reconciling the two, then dispatching parallel subagents to find PDFs, extract text, and write rule summaries.

## Components

### 1. Reconciliation via `import_games.py` extension

Rather than a new script, extend the existing `scripts/import_games.py` with `--dry-run` and `--output` flags to produce a candidates file without registering games.

**CLI:**
```bash
# Existing behavior (registers games directly)
python -m scripts.import_games ~/projects/boardgame-database/games/ \
  --master-csv ~/projects/boardgame-database/master_list.csv --limit 100

# New: dry-run mode outputs candidates file
python -m scripts.import_games ~/projects/boardgame-database/games/ \
  --master-csv ~/projects/boardgame-database/master_list.csv \
  --dry-run --output candidates.txt --limit 100 --type boardgame
```

**New arguments:**
| Arg | Default | Description |
|-----|---------|-------------|
| `--dry-run` | false | Don't register games, just output candidates |
| `--output PATH` | `candidates.txt` | Output file path (only with `--dry-run`) |
| `--type TYPE` | no filter | Filter by CSV `type` column (e.g., `boardgame` to exclude expansions) |

**Matching logic (existing):**
- Primary match: `bgg_id` (most reliable)
- Fallback: case-insensitive name match
- Entries without a `bgg_id` are skipped

**Output format (`candidates.txt`):**
```
Wingspan (266192)
Everdell (199792)
Root (237182)
```

One game per line, `name (bgg_id)`.

**Console output:**
```
Found 3200 candidates (3880 in CSV, 22 already tracked, 658 missing bgg_id)
Written to candidates.txt
```

### 2. Research Games Skill (`.claude/skills/research-games/SKILL.md`)

**Invocation:**
```
/research-games candidates.txt
/research-games candidates.txt --batch-size 20 --parallel 2
```

**Parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| `file` | (required) | Path to candidates file (one `name (bgg_id)` per line) |
| `--batch-size` | 80 | Number of games per subagent |
| `--parallel` | 3 | Max concurrent subagents |

#### Main Agent Workflow

1. **Parse candidates file** — read lines, extract `name` and `bgg_id` for each
2. **Detect slug collisions** — slugify all names, flag duplicates. Skip colliding games with a warning.
3. **Register all games** in `games.yaml` serially using `add_game(name, bgg_id, status="queued")`. Skip any already present.
4. **Chunk** the game list into batches of `batch-size`
5. **Dispatch subagents** — one per chunk, up to `parallel` at a time. Each subagent receives its chunk as a list of `(name, bgg_id, slug)` tuples.
6. **Collect results** — each subagent returns a results list: `[(name, bgg_id, status, notes), ...]`
7. **Update `games.yaml`** — main agent applies all status updates serially (no concurrent writes)
8. **Update `index.md`** — add all games that have a validated `rules/<slug>.md` file (alphabetical order)
9. **Report results** — print summary table of successes, failures, not-found

#### Subagent Workflow (per game in chunk)

For each game in the assigned chunk, sequentially:

1. **Find PDF URL** — search in priority order:
   - 1j1ju.com: `https://www.1j1ju.com/regle/<slug>` or search the site
   - Google: `"<game name>" rulebook filetype:pdf`
   - BGG files page: check the game's BGG files section
2. **If PDF not found:** record `(name, bgg_id, "not_found", "reason")` in results, continue to next game
3. **Download PDF** to `source_pdfs/<slug>-rules.pdf`
4. **Extract text:** run `python -m scripts.extract_pdf source_pdfs/<slug>-rules.pdf`
5. **Read extracted text** from `extracted/<slug>-rules.txt`
6. **Write rules summary** to `rules/<slug>.md` — following the standard template format (YAML frontmatter + 8 required sections for base games). Precision over brevity.
7. **Validate:** run `python -m scripts.validate rules/<slug>.md` (specific file, not all)
8. **Record result:** `(name, bgg_id, "summarized", "")` on success

**Error handling:** if any step fails for a game, record `(name, bgg_id, "flagged", "<error description>")` and continue to the next game.

**Important:** Subagents do NOT write to `games.yaml` or `index.md`. They only produce output files (`source_pdfs/`, `extracted/`, `rules/`) and return a results list. The main agent handles all registry and index updates.

### 3. Command File (`.claude/commands/research-games.md`)

Thin dispatcher that passes `$ARGUMENTS` to the skill.

```yaml
---
allowed-tools: Read, Grep, Glob, Edit, Write, WebSearch, WebFetch, Bash, Agent
description: Research and add new games in bulk. Usage: /research-games <candidates-file> [--batch-size N] [--parallel N]
---
```

## Architecture Decisions

### Projects stay separate
`boardgame-database` and `boardgame-rules` remain independent repositories. The reconciliation script bridges them by reading the CSV. The database could later add a `rules_summary` field pointing to the GitHub Pages URL.

### Extend `import_games.py`, don't create `reconcile.py`
The existing `import_games.py` already handles CSV parsing, BGG ID matching, and duplicate detection. Adding `--dry-run` and `--output` flags reuses this logic rather than duplicating it in a new script.

### Register upfront, update after
All games are registered in `games.yaml` by the main agent before subagents launch. Subagents produce only output files (PDFs, extracted text, rules markdown) and return a results list. The main agent applies all status updates to `games.yaml` serially after subagents complete. This eliminates concurrent write conflicts entirely.

### Subagents summarize directly
Subagents are Claude — they read extracted text and write rule summaries themselves, rather than calling `scripts/summarize.py` (which calls the external Claude API). This removes the API key dependency and rate-limit bottleneck.

### Configurable parallelism
Batch size (default 80) and parallel agent count (default 3) are configurable so the user can experiment to find the optimum. Prior experience with a similar workflow in `boardgame-database` suggests ~80 games per agent is a good starting point.

### Expansions are out of scope
The `--type boardgame` filter on `import_games.py` excludes expansions from candidates. Expansions require different rules sections and a `base_game_bgg_id` link — handling them in bulk research adds complexity without proportional value. They can be added individually via the manual pipeline.

### Slug collision detection
Before dispatching subagents, the main agent slugifies all candidate names and checks for collisions. Colliding games are skipped with a warning. This prevents subagents from silently overwriting each other's output files.

## File Layout

```
.claude/
  skills/research-games/SKILL.md    # Skill definition
  commands/research-games.md        # /research-games command dispatcher
scripts/
  import_games.py                   # Extended with --dry-run, --output, --type
```

No new scripts. Existing scripts are extended or used as-is.

## Dependencies

- Existing: `scripts/import_games.py`, `scripts/extract_pdf.py`, `scripts/registry.py`, `scripts/validate.py`
- External: web access for PDF finding (1j1ju.com, Google, BGG)
- No new Python dependencies required
