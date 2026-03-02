# Boardgame Rules Database

## Project Structure
- `games.yaml` — master game registry (name, bgg_id, status)
- `source_pdfs/` — downloaded PDFs (gitignored)
- `extracted/` — raw extracted text from PDFs
- `rules/` — final structured markdown files with YAML frontmatter
- `scripts/` — Python pipeline tools

## Pipeline

### Adding a New Game

- [ ] Run `python -m scripts.find_rulebook "Game Name" --bgg-id <ID>` to fetch metadata from BGG and register the game. Use `--bgg-id` to skip interactive search (find the ID on the game's BGG page URL). The script will attempt to download the PDF, but BGG blocks automated scraping — you'll likely need to download manually.
- [ ] Download the rulebook PDF manually from BGG's files page or the publisher's site. Save it to `source_pdfs/<slug>-rules.pdf`.
- [ ] Run `python -m scripts.extract_pdf source_pdfs/<slug>-rules.pdf` to extract text. Use `--method pdfplumber` if tables are mangled. Review `extracted/<slug>-rules.txt` for quality.
- [ ] Summarize interactively with Claude Code: read the extracted text, produce `rules/<slug>.md` following the template format. Precision over brevity — keep all edge cases and exact numbers.
- [ ] Run `python -m scripts.validate` to check the rules file has all required frontmatter and sections.
- [ ] Commit the extracted text, rules file, and updated `games.yaml`.

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
