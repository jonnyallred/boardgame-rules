# Boardgame Rules Database

## Project Structure
- `games.yaml` — master game registry (name, bgg_id, status)
- `source_pdfs/` — downloaded PDFs (gitignored)
- `extracted/` — raw extracted text from PDFs
- `rules/` — final structured markdown files with YAML frontmatter
- `scripts/` — Python pipeline tools

## Pipeline
1. `python -m scripts.find_rulebook "Game Name"` — search BGG, download PDF
2. `python -m scripts.extract_pdf source_pdfs/game.pdf` — extract text
3. Interactive summarization with Claude Code
4. `python -m scripts.validate` — check completeness

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
- Virtualenv at `.venv/` — activate with `source .venv/bin/activate`
