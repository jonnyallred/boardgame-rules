# Research Games Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a skill that bulk-researches boardgame rules by dispatching parallel subagents, plus extend `import_games.py` with dry-run reconciliation mode.

**Architecture:** Extend `import_games.py` with `--dry-run`/`--output`/`--type` flags to produce a candidates file. A new skill (`research-games`) reads this file, registers all games upfront, dispatches subagents in configurable batches, then consolidates results into `games.yaml` and `index.md`.

**Tech Stack:** Python 3.10+, PyYAML, Claude Code skills/commands, Agent tool

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `scripts/import_games.py` | Modify | Add `--dry-run`, `--output`, `--type` flags |
| `tests/test_import_games.py` | Modify | Add tests for new flags |
| `.claude/skills/research-games/SKILL.md` | Create | Skill definition for bulk research |
| `.claude/commands/research-games.md` | Create | `/research-games` command dispatcher |

---

## Chunk 1: Extend `import_games.py` with dry-run mode

### Task 1: Add `--type` filter to `import_from_database`

**Files:**
- Modify: `scripts/import_games.py:89-181`
- Test: `tests/test_import_games.py`

- [ ] **Step 1: Write the failing test**

In `tests/test_import_games.py`, add a test and a fixture with a `type` column:

```python
@pytest.fixture
def typed_mock_db(tmp_path):
    """Mock DB with a base game and an expansion."""
    games_dir = tmp_path / "typed_games"
    games_dir.mkdir()
    for game in [
        {"id": "agricola", "name": "Agricola", "year": 2007, "designer": ["Uwe Rosenberg"]},
        {"id": "catan", "name": "Catan", "year": 1995, "designer": ["Klaus Teuber"]},
        {"id": "catan-seafarers", "name": "Catan: Seafarers", "year": 1997, "designer": ["Klaus Teuber"]},
    ]:
        (games_dir / f"{game['id']}.yaml").write_text(yaml.dump(game))
    return str(games_dir)


@pytest.fixture
def typed_master_csv(tmp_path):
    """CSV with type column including boardgame and expansion."""
    csv_path = tmp_path / "master_list.csv"
    csv_path.write_text(
        "bgg_id,name,year,type,status,notes,yaml_id\n"
        "31260,Agricola,2007,boardgame,,,\n"
        "13,Catan,1995,boardgame,,,\n"
        "325,Catan: Seafarers,1997,boardgameexpansion,,,catan-seafarers\n"
    )
    return str(csv_path)


def test_import_type_filter(registry_path, typed_mock_db, typed_master_csv):
    """--type boardgame should exclude expansions."""
    # Without filter: all 3 imported
    stats_all = import_from_database(
        typed_mock_db, registry_path, typed_master_csv
    )
    assert stats_all["imported"] == 3

    # Reset registry
    Path(registry_path).write_text("games: []\n")

    # With filter: only boardgames
    stats_filtered = import_from_database(
        typed_mock_db, registry_path, typed_master_csv, game_type="boardgame"
    )
    reg = load_registry(registry_path)
    names = [g["name"] for g in reg]
    assert "Catan: Seafarers" not in names
    assert stats_filtered["imported"] == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `source .venv/bin/activate && python -m pytest tests/test_import_games.py::test_import_type_filter -v`
Expected: FAIL — `import_from_database() got an unexpected keyword argument 'game_type'`

- [ ] **Step 3: Add `game_type` parameter and type-filtering logic**

In `scripts/import_games.py`, update `build_bgg_lookup` to optionally return type info, and add filtering to `import_from_database`:

```python
def build_bgg_lookup(master_csv_path: str, game_type: str | None = None) -> dict[str, int]:
    """Read master_list.csv and build a slug -> bgg_id lookup dict.

    Uses the yaml_id column if present; otherwise slugifies the name.
    Only includes rows where bgg_id is non-empty.
    If game_type is specified, only includes rows matching that type.
    """
    lookup: dict[str, int] = {}
    with open(master_csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if game_type and row.get("type", "").strip() != game_type:
                continue
            bgg_id_str = row.get("bgg_id", "").strip()
            if not bgg_id_str:
                continue
            try:
                bgg_id = int(bgg_id_str)
            except ValueError:
                continue

            yaml_id = row.get("yaml_id", "").strip()
            if yaml_id:
                slug = yaml_id
            else:
                name = row.get("name", "").strip()
                if not name:
                    continue
                slug = slugify(name)

            lookup[slug] = bgg_id
    return lookup
```

Update `import_from_database` signature to accept `game_type`:

```python
def import_from_database(
    games_dir: str,
    registry_path: str,
    master_csv_path: str,
    limit: int = 0,
    game_type: str | None = None,
) -> dict[str, int]:
```

And pass it through:

```python
    bgg_lookup = build_bgg_lookup(master_csv_path, game_type=game_type)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `source .venv/bin/activate && python -m pytest tests/test_import_games.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/import_games.py tests/test_import_games.py
git commit -m "feat(import): add --type filter to exclude expansions"
```

---

### Task 2: Add `--dry-run` and `--output` flags

**Files:**
- Modify: `scripts/import_games.py:89-181`
- Test: `tests/test_import_games.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_dry_run_produces_candidates_file(tmp_path, registry_path, mock_db, mock_master_csv):
    """Dry-run should write candidates.txt without modifying registry."""
    output_path = str(tmp_path / "candidates.txt")
    stats = import_from_database(
        mock_db, registry_path, mock_master_csv, dry_run=True, output_path=output_path
    )
    # Registry should be unchanged
    reg = load_registry(registry_path)
    assert len(reg) == 0
    # Candidates file should exist with entries
    content = Path(output_path).read_text()
    lines = [l for l in content.strip().split("\n") if l]
    assert len(lines) == 2
    assert stats["imported"] == 2


def test_dry_run_output_format(tmp_path, registry_path, mock_db, mock_master_csv):
    """Each line should be 'Name (bgg_id)' format."""
    output_path = str(tmp_path / "candidates.txt")
    import_from_database(
        mock_db, registry_path, mock_master_csv, dry_run=True, output_path=output_path
    )
    content = Path(output_path).read_text()
    lines = content.strip().split("\n")
    for line in lines:
        assert re.match(r".+ \(\d+\)$", line), f"Bad format: {line}"


def test_dry_run_skips_existing(tmp_path, registry_path, mock_db, mock_master_csv):
    """Dry-run should skip games already in registry."""
    # First import Agricola normally
    from scripts.registry import add_game
    add_game(registry_path, name="Agricola", bgg_id=31260)

    output_path = str(tmp_path / "candidates.txt")
    stats = import_from_database(
        mock_db, registry_path, mock_master_csv, dry_run=True, output_path=output_path
    )
    content = Path(output_path).read_text()
    lines = [l for l in content.strip().split("\n") if l]
    assert len(lines) == 1  # Only Catan
    assert "Catan" in lines[0]
    assert stats["skipped"] == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && python -m pytest tests/test_import_games.py::test_dry_run_produces_candidates_file -v`
Expected: FAIL — `import_from_database() got an unexpected keyword argument 'dry_run'`

- [ ] **Step 3: Implement dry-run mode**

Add `dry_run` and `output_path` parameters to `import_from_database`. When `dry_run=True`, collect candidates instead of appending to the registry, then write them to the output file.

In `scripts/import_games.py`, update the function signature:

```python
def import_from_database(
    games_dir: str,
    registry_path: str,
    master_csv_path: str,
    limit: int = 0,
    game_type: str | None = None,
    dry_run: bool = False,
    output_path: str = "candidates.txt",
) -> dict[str, int]:
```

Add a `candidates` list at the top of the function. Inside the loop, replace the `games.append(entry)` block with a conditional that collects into `candidates` when dry-running. **Replace the existing unconditional `save_registry(registry_path, games)` call at the end of the function** with this conditional block:

```python
    candidates: list[tuple[str, int]] = []

    # ... inside the loop, replace the games.append(entry) + stats lines with:
        if dry_run:
            candidates.append((name, bgg_id))
        else:
            games.append(entry)
        existing_bgg_ids.add(bgg_id)
        existing_names.add(name.lower())
        stats["imported"] += 1

    # REPLACE the existing `save_registry(registry_path, games)` at the end with:
    if dry_run:
        with open(output_path, "w") as f:
            for name, bgg_id in candidates:
                f.write(f"{name} ({bgg_id})\n")
    else:
        save_registry(registry_path, games)
```

- [ ] **Step 4: Run all tests to verify they pass**

Run: `source .venv/bin/activate && python -m pytest tests/test_import_games.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/import_games.py tests/test_import_games.py
git commit -m "feat(import): add --dry-run and --output flags for candidates file"
```

---

### Task 3: Wire new flags into CLI `main()`

**Files:**
- Modify: `scripts/import_games.py:184-231`

- [ ] **Step 1: Add argparse arguments and pass them through**

In `scripts/import_games.py` `main()`, add the new arguments:

```python
    parser.add_argument(
        "--type",
        default=None,
        help="Filter by CSV type column (e.g., 'boardgame' to exclude expansions)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't register games, just output a candidates file",
    )
    parser.add_argument(
        "--output",
        default="candidates.txt",
        help="Output file for --dry-run mode (default: candidates.txt)",
    )
```

Pass them to `import_from_database`:

```python
    stats = import_from_database(
        args.games_dir,
        args.registry,
        master_csv,
        limit=args.limit,
        game_type=args.type,
        dry_run=args.dry_run,
        output_path=args.output,
    )
```

Update the print output to handle dry-run mode:

```python
    if args.dry_run:
        print(f"Dry run complete:")
        print(f"  Candidates: {stats['imported']}")
        print(f"  Skipped (already in registry): {stats['skipped']}")
        print(f"  Skipped (no BGG ID): {stats['no_bgg_id']}")
        print(f"  Written to: {args.output}")
    else:
        print(f"Import complete:")
        # ... existing output ...
```

- [ ] **Step 2: Manual test**

Run: `source .venv/bin/activate && python -m scripts.import_games ~/projects/boardgame-database/games/ --master-csv ~/projects/boardgame-database/master_list.csv --dry-run --type boardgame --limit 5 --output /tmp/test-candidates.txt`

Verify: `/tmp/test-candidates.txt` has 5 lines in `Name (bgg_id)` format, and `games.yaml` is unchanged.

- [ ] **Step 3: Run full test suite**

Run: `source .venv/bin/activate && python -m pytest tests/ -v`
Expected: ALL PASS

- [ ] **Step 4: Commit**

```bash
git add scripts/import_games.py
git commit -m "feat(import): wire --dry-run, --output, --type into CLI"
```

---

## Chunk 2: Create the research-games skill and command

### Task 4: Create the command file

**Files:**
- Create: `.claude/commands/research-games.md`

- [ ] **Step 1: Create the command file**

```markdown
---
allowed-tools: Read, Grep, Glob, Edit, Write, WebSearch, WebFetch, Bash, Agent
description: Research and add new games in bulk. Usage: /research-games <candidates-file> [--batch-size N] [--parallel N]
---

# Research Games

The user wants to bulk-research boardgame rules. Use the `research-games` skill to process the request.

**User's arguments:** $ARGUMENTS
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/research-games.md
git commit -m "feat: add /research-games command dispatcher"
```

---

### Task 5: Create the research-games skill

**Files:**
- Create: `.claude/skills/research-games/SKILL.md`

This is the core skill file. It instructs Claude Code how to parse arguments, register games, dispatch subagents, and consolidate results.

- [ ] **Step 1: Create the skill directory and file**

Write `.claude/skills/research-games/SKILL.md` with this content:

```markdown
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
```

- [ ] **Step 2: Verify skill appears in available skills**

Check that the skill shows up by looking at the skills directory structure:
```bash
ls -la .claude/skills/research-games/SKILL.md
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/research-games/SKILL.md
git commit -m "feat: add research-games skill for bulk game research"
```

---

### Task 6: End-to-end manual test with a small batch

**Files:** No new files — this is a validation task.

- [ ] **Step 1: Generate a small candidates file**

```bash
source .venv/bin/activate && python -m scripts.import_games ~/projects/boardgame-database/games/ \
  --master-csv ~/projects/boardgame-database/master_list.csv \
  --dry-run --type boardgame --limit 3 --output test-candidates.txt
```

Verify: `test-candidates.txt` has 3 lines in correct format.

- [ ] **Step 2: Test the skill with 1 game**

Create a 1-game test file:
```bash
head -1 test-candidates.txt > test-1-game.txt
```

Run: `/research-games test-1-game.txt --batch-size 1 --parallel 1`

Verify:
- Game is registered in `games.yaml`
- PDF downloaded to `source_pdfs/`
- Text extracted to `extracted/`
- Rules summary written to `rules/`
- Validation passes
- `games.yaml` status updated
- `index.md` updated with new entry

- [ ] **Step 3: Clean up test artifacts**

```bash
rm test-candidates.txt test-1-game.txt
```

- [ ] **Step 4: Commit any fixes discovered during testing**

```bash
git add -A
git commit -m "fix: address issues found during research-games testing"
```

---

## Chunk 3: Update project documentation

### Task 7: Update CLAUDE.md with skill documentation

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add research-games workflow to CLAUDE.md**

In the "Pipeline" section of `CLAUDE.md`, add a new subsection after "Batch PDF Finding":

```markdown
### Bulk Research (Parallel Subagents)

Generate a candidates file from boardgame-database, then bulk-research with parallel subagents:

1. Generate candidates: `python -m scripts.import_games ~/projects/boardgame-database/games/ --master-csv ~/projects/boardgame-database/master_list.csv --dry-run --type boardgame --limit 100 --output candidates.txt`
2. Run the skill: `/research-games candidates.txt --batch-size 20 --parallel 3`
3. Review results — check flagged games for issues

The skill registers all games upfront, dispatches subagents to find PDFs / extract / summarize, then consolidates results into `games.yaml` and `index.md`.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add bulk research workflow to CLAUDE.md"
```
