# Boardgame Rules Database

## Project Structure
- `games.yaml` — master game registry (name, bgg_id, status)
- `source_pdfs/` — downloaded PDFs (gitignored)
- `extracted/` — raw extracted text from PDFs
- `rules/` — final structured markdown files with YAML frontmatter
- `scripts/` — Python pipeline tools
- `index.md` — GitHub Pages landing page (game list + usage instructions)
- `_config.yml` — Jekyll config for GitHub Pages

## Pipeline

### Adding a Single Game (Manual)

- [ ] Run `python -m scripts.find_rulebook "Game Name" --bgg-id <ID>` to fetch metadata from BGG and register the game. Use `--bgg-id` to skip interactive search (find the ID on the game's BGG page URL). The script will attempt to download the PDF, but BGG blocks automated scraping — you'll likely need to download manually.
- [ ] Download the rulebook PDF manually. Check these sources in order: 1j1ju.com (good coverage of manuals), BGG's files page, or the publisher's site. Save it to `source_pdfs/<slug>-rules.pdf`. Tip: create the empty file first with `touch source_pdfs/<slug>-rules.pdf` so the user can "Save As" directly over it with the correct name.
- [ ] Run `python -m scripts.extract_pdf source_pdfs/<slug>-rules.pdf` to extract text. Use `--method pdfplumber` if tables are mangled. Review `extracted/<slug>-rules.txt` for quality.
- [ ] If extracted text has gaps or garbled tables, render the PDF pages to images for visual inspection: `python -c "import fitz; doc=fitz.open('source_pdfs/<slug>-rules.pdf'); [doc[i].get_pixmap(matrix=fitz.Matrix(2,2)).save(f'/tmp/<slug>-p{i+1}.png') for i in range(len(doc))]"` then use the Read tool on the resulting PNGs to read tables and diagrams directly.
- [ ] Summarize interactively with Claude Code: read the extracted text, produce `rules/<slug>.md` following the template format. Precision over brevity — keep all edge cases and exact numbers.
- [ ] Run `python -m scripts.validate` to check the rules file has all required frontmatter and sections.
- [ ] Add the new game to the table in `index.md` (alphabetical order) so it appears on the GitHub Pages site.
- [ ] Commit the extracted text, rules file, updated `games.yaml`, and `index.md`.

### Batch Processing (Scalable Pipeline)

**Import games from boardgame-database:**
```bash
python -m scripts.import_games /path/to/boardgame-database/games/ \
  --master-csv /path/to/boardgame-database/master_list.csv \
  --limit 100
```

**Find PDFs (interactive with Claude Code + Playwright):**
See "Batch PDF Finding" section below.

**Process pipeline stages:**
```bash
# Download all found PDFs
python -m scripts.process_batch --stage download --limit 50

# Extract text from downloaded PDFs
python -m scripts.process_batch --stage extract --limit 50

# Summarize extracted text via Claude API
python -m scripts.process_batch --stage summarize --limit 20

# Quality check summarized rules
python -m scripts.process_batch --stage quality_check

# Check overall pipeline status
python -m scripts.process_batch --status
```

**Status flow:** `queued → found → downloaded → extracted → summarized → validated`
Terminal states: `not_found`, `flagged` (need human attention)

### Bulk Research (Parallel Subagents)

Generate a candidates file from boardgame-database, then bulk-research with parallel subagents:

1. Generate candidates: `python -m scripts.import_games ~/projects/boardgame-database/games/ --master-csv ~/projects/boardgame-database/master_list.csv --dry-run --type boardgame --limit 100 --output candidates.txt`
2. Run the skill: `/research-games candidates.txt --batch-size 20 --parallel 3`
3. Review results — check flagged games for issues

The skill registers all games upfront, dispatches subagents to find PDFs / extract / summarize, then consolidates results into `games.yaml` and `index.md`.

### Batch PDF Finding (Interactive)

To find rulebook PDFs for queued games using Playwright browser tools:

1. Check queue: `python -m scripts.process_batch --status`
2. Ask Claude Code: "Find rulebook PDFs for the next 20 queued games"
3. Claude searches (in priority order): 1j1ju.com, Google, BGG files page
4. For each game found, update registry: `status: found`, `pdf_url: "..."`
5. For games not found: `status: not_found`, `notes: "reason"`
6. Then run: `python -m scripts.process_batch --stage download`

Queue management helpers:
```python
from scripts.registry import get_games_by_status, update_game

# Get next batch
games = get_games_by_status("games.yaml", "queued", limit=20)

# Record a found PDF
update_game("games.yaml", "Agricola", status="found",
            pdf_url="https://1j1ju.com/rules/agricola-en.pdf")

# Record not found
update_game("games.yaml", "Obscure Game", status="not_found",
            notes="No English rulebook found")
```

## Rules File Format
YAML frontmatter (title, bgg_id, player_count, play_time, designer, source_pdf, extracted_date, summarized_date, rulebook_version) + Markdown body with sections: Overview, Components, Setup, Turn Structure, Actions, Scoring / Victory Conditions, Special Rules & Edge Cases, Player Reference.

## Expansions

Expansions are tracked as separate entries linked to their base game. The pipeline is the same as for base games, with two differences:

1. **Registry:** Add `base_game_bgg_id: <int>` to the expansion's `games.yaml` entry, pointing to the base game's BGG ID.
2. **Rules file:** Use expansion sections instead of base game sections:
   - Overview (what the expansion adds/changes)
   - New Components (new pieces, cards, boards)
   - Setup Changes (how setup differs from base game)
   - Rule Changes (modified or new mechanics)
   - Special Rules & Edge Cases
   - Player Reference

Frontmatter must include `base_game_bgg_id` to trigger expansion validation.

**Helper functions:**
```python
from scripts.registry import find_expansions, find_base_game

# Get all expansions for Catan (bgg_id=13)
find_expansions("games.yaml", 13)

# Find the base game for an expansion
find_base_game("games.yaml", 325)  # returns Catan entry
```

**Display:** In `index.md`, list expansions indented under their base game with `↳` prefix.

## Testing
```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

## GitHub Pages Site
The rules are published at `https://jonnyallred.github.io/boardgame-rules/`. GitHub Pages builds automatically from the `main` branch using Jekyll. The `_config.yml` excludes non-site directories (scripts, source_pdfs, extracted, tests, etc.). When adding a new game, update `index.md` with the new entry in alphabetical order.

## Requirements
- Python 3.10+
- BGG API token in `.env` (register at https://boardgamegeek.com/applications)
- Anthropic API key in `.env` (for batch summarization)
- Virtualenv at `.venv/` — activate with `source .venv/bin/activate`
