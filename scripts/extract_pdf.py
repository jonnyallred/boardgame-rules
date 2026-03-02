#!/usr/bin/env python3
"""Extract text from boardgame rulebook PDFs.

Usage:
    python -m scripts.extract_pdf source_pdfs/catan-rules.pdf
    python -m scripts.extract_pdf source_pdfs/catan-rules.pdf --output extracted/catan.txt
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

import fitz  # PyMuPDF

from scripts.registry import update_status, load_registry

EXTRACTED_DIR = "extracted"


def extract_text(pdf_path: str) -> str:
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            pages.append(text)
    doc.close()
    return "\n\n".join(pages)


def extract_text_pdfplumber(pdf_path: str) -> str:
    """Fallback extraction using pdfplumber (better for tables)."""
    import pdfplumber

    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text)

            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cells = [str(c) if c else "" for c in row]
                    pages.append(" | ".join(cells))

    return "\n\n".join(pages)


def clean_text(text: str) -> str:
    """Clean extracted PDF text: remove artifacts, normalize whitespace."""
    lines = text.split("\n")

    # Count line frequencies to detect repeated headers/footers
    line_counts = Counter(line.strip() for line in lines if line.strip())
    total_pages = text.count("\f") + 1
    threshold = max(3, total_pages // 2)

    cleaned_lines = []
    for line in lines:
        stripped = line.strip()

        # Remove standalone page numbers
        if re.match(r"^\d{1,3}$", stripped):
            continue

        # Remove repeated headers/footers
        if stripped and line_counts[stripped] >= threshold:
            continue

        # Collapse multiple spaces within a line
        line = re.sub(r"  +", " ", line)

        cleaned_lines.append(line)

    result = "\n".join(cleaned_lines)

    # Collapse 3+ consecutive blank lines to 2
    result = re.sub(r"\n{3,}", "\n\n", result)

    return result.strip()


def main():
    parser = argparse.ArgumentParser(description="Extract text from boardgame rulebook PDFs")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output", help="Output text file path (default: extracted/<name>.txt)")
    parser.add_argument("--method", choices=["pymupdf", "pdfplumber"], default="pymupdf",
                        help="Extraction method (default: pymupdf)")
    parser.add_argument("--registry", default="games.yaml", help="Path to games.yaml")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF not found: {args.pdf_path}")
        sys.exit(1)

    pdf_stem = Path(args.pdf_path).stem
    if args.output:
        output_path = args.output
    else:
        os.makedirs(EXTRACTED_DIR, exist_ok=True)
        output_path = os.path.join(EXTRACTED_DIR, f"{pdf_stem}.txt")

    print(f"Extracting text from {args.pdf_path} (method: {args.method})...")
    if args.method == "pdfplumber":
        raw_text = extract_text_pdfplumber(args.pdf_path)
    else:
        raw_text = extract_text(args.pdf_path)

    print(f"  Raw text: {len(raw_text)} characters")

    cleaned = clean_text(raw_text)
    print(f"  Cleaned text: {len(cleaned)} characters")

    with open(output_path, "w") as f:
        f.write(cleaned)
    print(f"  Saved to: {output_path}")

    # Update registry if we can match the game
    games = load_registry(args.registry)
    for game in games:
        slug = re.sub(r"[^a-z0-9]+", "-", game["name"].lower()).strip("-")
        if slug in pdf_stem.lower():
            update_status(args.registry, game["name"], "extracted")
            print(f"  Updated registry: {game['name']} → extracted")
            break


if __name__ == "__main__":
    main()
