# Boardgame Rules Database

## Project Structure
- `games.yaml` — master game registry (name, bgg_id, status)
- `source_pdfs/` — downloaded PDFs (gitignored)
- `extracted/` — raw extracted text from PDFs
- `rules/` — final structured markdown files with YAML frontmatter
- `scripts/` — Python pipeline tools

## Pipeline

### Adding a Single Game (Manual)

- [ ] Run `python -m scripts.find_rulebook "Game Name" --bgg-id <ID>` to fetch metadata from BGG and register the game.
- [ ] Download the rulebook PDF manually to `source_pdfs/<slug>-rules.pdf`. Check: 1j1ju.com, BGG's files page, or the publisher's site.
- [ ] Run `python -m scripts.extract_pdf source_pdfs/<slug>-rules.pdf` to extract text.
- [ ] Summarize interactively with Claude Code, or run `python -m scripts.summarize extracted/<slug>-rules.txt --game "Game Name"`.
- [ ] Run `python -m scripts.validate` to check the rules file.
- [ ] Commit the extracted text, rules file, and updated `games.yaml`.

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

## Testing
```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

## Requirements
- Python 3.10+
- BGG API token in `.env` (register at https://boardgamegeek.com/applications)
- Anthropic API key in `.env` (for batch summarization)
- Virtualenv at `.venv/` — activate with `source .venv/bin/activate`
