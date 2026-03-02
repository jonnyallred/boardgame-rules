# Boardgame Rules Database — Design

## Purpose

A boardgame rule database that stores official rulebook content in a structured, AI-friendly format. Primary consumers: Claude (direct context), RAG/embedding pipelines, and standalone human reference.

## Requirements

- Semi-automated PDF sourcing: given game names, find and download official rulebook PDFs from BGG
- PDF extraction to clean plaintext
- Interactive summarization via Claude Code — precision over brevity
- Output: Markdown files with YAML frontmatter
- Initial scale: ~10-20 games
- Both extracted text and final summaries tracked in version control

## Approach: Flat File Pipeline

No database or server. Scripts + directory structure. Files are the product.

## Directory Structure

```
boardgame-rules/
  games.yaml              # master registry: game name, bgg_id, pdf_url, status
  source_pdfs/            # original PDFs (gitignored)
  extracted/              # raw extracted text (tracked)
  rules/                  # final markdown files (tracked) — the product
  scripts/
    find_rulebook.py      # game name → BGG search → download PDF
    extract_pdf.py        # PDF → clean plaintext
    validate.py           # checks rules files for completeness
  requirements.txt
```

## Game Registry (games.yaml)

```yaml
- name: Catan
  bgg_id: 13
  pdf_source: "https://..."
  status: summarized  # pending | downloaded | extracted | summarized
```

Status tracks pipeline progress per game.

## Rules Markdown Format

```markdown
---
title: "Game Name"
bgg_id: 123
player_count: "2-4"
play_time: "60-120 min"
designer: "Designer Name"
source_pdf: "filename.pdf"
extracted_date: "YYYY-MM-DD"
summarized_date: "YYYY-MM-DD"
rulebook_version: "Edition"
---

# Game Name

## Overview
## Components
## Setup
## Turn Structure
## Actions
## Scoring / Victory Conditions
## Special Rules & Edge Cases
## Player Reference
```

Precision-focused: all edge cases, exceptions, exact numbers preserved. Sections provide structure for scanning; content within is comprehensive.

## Pipeline Scripts

### find_rulebook.py

1. Searches BGG XML API for game → gets BGG ID, metadata
2. Checks BGG file listings for official rulebook PDFs
3. Auto-downloads PDFs to `source_pdfs/`
4. Updates `games.yaml` with metadata and status

### extract_pdf.py

1. Primary extractor: PyMuPDF (fitz) — fast, handles most layouts
2. Fallback: pdfplumber for table-heavy content
3. Cleans PDF artifacts (headers/footers, page numbers, column merging)
4. Outputs to `extracted/{game_name}.txt`
5. Updates status in `games.yaml`

### validate.py

- Checks required frontmatter fields present
- Verifies all expected sections exist
- Flags games in registry missing rules files

## Summarization Workflow

Interactive via Claude Code (not automated):

1. Open extracted text
2. Claude Code reads extracted text + template format
3. Collaboratively produce rules markdown
4. Save to `rules/{game_name}.md`

## Tech Stack

- Python 3
- PyMuPDF (fitz) — PDF text extraction
- pdfplumber — fallback for tables
- PyYAML — games.yaml management
- requests — HTTP for BGG API and PDF downloads
- beautifulsoup4 — parsing BGG HTML for file listings

## Decisions

- **Flat files over SQLite**: For 10-20 games, files are simpler and more portable. Can add SQLite later if scaling up.
- **Precision over brevity**: All edge cases and exact numbers preserved. AI can always summarize down; it can't recover lost detail.
- **YAML frontmatter + Markdown body**: Single file per game, version-controllable, readable by humans and machines.
- **PDFs gitignored**: Large binary files don't belong in git. URLs tracked in games.yaml for reproducibility.
- **Extracted text tracked**: Enables diffing re-extractions and gives Claude Code direct access.
