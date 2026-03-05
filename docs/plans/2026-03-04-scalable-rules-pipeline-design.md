# Scalable Rules Pipeline Design

**Date:** 2026-03-04
**Goal:** Scale the boardgame-rules pipeline from manual (7 games) to automated (1000s of games) by adding browser-based PDF discovery, automated summarization, and quality tiers.

## Architecture

4-stage pipeline, each independently runnable:

```
boardgame-database ──import──► Queue (games.yaml)
                                  │
                          ┌───────▼────────┐
                          │  Stage 1: FIND  │  Browser agent searches for PDFs
                          │  (Playwright)   │  Outputs: download URLs or failures
                          └───────┬────────┘
                                  │
                          ┌───────▼────────┐
                          │ Stage 2: DOWNLOAD│  Fetch PDFs to source_pdfs/
                          │  (requests/curl) │
                          └───────┬────────┘
                                  │
                          ┌───────▼────────┐
                          │ Stage 3: EXTRACT │  PDF → text (existing extract_pdf.py)
                          │  (PyMuPDF)       │
                          └───────┬────────┘
                                  │
                          ┌───────▼────────┐
                          │ Stage 4: SUMMARIZE│  Text → rules markdown (Claude API)
                          │  + VALIDATE       │  Quality flags for human review
                          └─────────────────┘
```

### Status Flow

`queued → searching → found → downloaded → extracted → summarized → validated → flagged`

- Games progress through statuses as each stage completes
- `not_found` / `flagged` are terminal states requiring human attention
- Batch orchestrator (`process_batch.py`) advances games through stages

## Stage 1: Find (Browser Agent)

A Claude agent with Playwright browser tools searches for rulebook PDFs per game.

### Search Strategy (priority order)

1. **1j1ju.com** — Search for game name, look for English rulebook PDF link
2. **Publisher site** — If publisher known, search `"{game name}" rules filetype:pdf site:{publisher-domain}`
3. **Google search** — `"{game name}" rulebook pdf` — look for direct PDF links
4. **BGG files page** — `boardgamegeek.com/boardgame/{bgg_id}/files` — parse for rulebook downloads (browser handles JS rendering)

### Output

Updates `games.yaml` per game:
- Success: `status: found`, `pdf_url: "https://..."`
- Failure: `status: not_found`, `notes: "reason"`

### Batch Size

20-50 games per session. Sequential within a session.

## Stage 2: Download

Simple HTTP download from found URLs to `source_pdfs/<slug>-rules.pdf`.

- Handles redirects, retries on transient errors
- Verifies PDF file integrity (check magic bytes / file size > 10KB)
- Updates status to `downloaded` on success

## Stage 3: Extract

Existing `extract_pdf.py` — no changes needed.

- PyMuPDF (default) with pdfplumber fallback for tables
- Cleans headers/footers, page numbers, whitespace
- Output to `extracted/<slug>-rules.txt`
- Updates status to `extracted`

## Stage 4: Summarize + Quality Tiers

### Summarization

Call Claude API with:
- Extracted rulebook text
- Target template (all 8 required sections)
- Game metadata (player count, play time, designer) for frontmatter
- Instructions: "Precision over brevity — keep all edge cases and exact numbers"

Output: `rules/<slug>.md` with YAML frontmatter + markdown body.

### Quality Scoring

After generation, automatically check:

| Check | Flag condition |
|-------|---------------|
| Extraction quality | Extracted text < 2KB |
| Section completeness | Any required section empty or < 50 words |
| Hallucination risk | Rules mention mechanics not in extracted text |
| Validation | `validate.py` fails |
| Confidence | Model expresses uncertainty ("unclear from the text") |

### Quality Tiers

- **Auto-accept**: Passes all checks → status `validated`
- **Flagged**: Fails 1+ checks → status `flagged` with `review_notes`

### Calibration Phase

First 20-30 summaries reviewed manually to calibrate quality. Once confident, switch to auto-accept for remaining games.

## Integration with boardgame-database

**One-way import only.** A script reads game names + bgg_ids from boardgame-database YAML files and creates queue entries in this project's `games.yaml`. No changes to boardgame-database.

## New Scripts

| Script | Purpose |
|--------|---------|
| `scripts/import_games.py` | Import games from boardgame-database into queue |
| `scripts/find_pdf.py` | Browser agent: search for rulebook PDFs |
| `scripts/download_pdf.py` | Download PDFs from found URLs |
| `scripts/summarize.py` | Claude API: generate rules markdown from extracted text |
| `scripts/quality_check.py` | Score summaries, assign auto-accept vs flagged |
| `scripts/process_batch.py` | Orchestrator: run stages for N games |

## Reused Scripts

- `extract_pdf.py` — as-is
- `validate.py` — extended with quality scoring
- `registry.py` — extended with new statuses
- `bgg.py` / `bgg_files.py` — used within find stage as fallback

## Config

- `ANTHROPIC_API_KEY` in `.env` for summarization
- `BGG_API_TOKEN` in `.env` (existing)
- Search site preferences in config (optional)

## Decisions

- **Full summaries** at current quality level (all 8 sections, ~200-300 lines per game)
- **Browser-first** PDF acquisition via Playwright
- **Auto-accept with calibration** — review first batch, then auto-accept
- **Independent projects** — rules pipeline imports from boardgame-database but doesn't modify it
