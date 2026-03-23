#!/usr/bin/env python3
"""Collect subagent results and update games.yaml registry.

Parses RESULTS_START/RESULTS_END blocks from subagent output (stdin or file)
and updates the registry with the status of each game.

Usage:
    # From a file:
    python -m scripts.collect_results results.txt

    # Pipe from multiple files:
    cat batch1.txt batch2.txt | python -m scripts.collect_results

    # With explicit registry path:
    python -m scripts.collect_results results.txt --registry games.yaml
"""

from __future__ import annotations

import argparse
import re
import sys

from scripts.registry import update_game


def _extract_text_from_jsonl(raw: str) -> str:
    """Extract assistant text content from JSONL conversation log files.

    Subagent output files are JSONL where each line is a JSON object.
    The RESULTS block lives inside assistant message content fields.
    Falls back to returning the raw text if it's not JSONL.
    """
    import json

    texts = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            texts.append(line)
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            texts.append(line)
            continue
        # Extract text from assistant message content
        msg = obj.get("message", {})
        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block["text"])
    return "\n".join(texts)


def parse_results(text: str) -> list[dict]:
    """Parse RESULTS_START/RESULTS_END blocks from subagent output.

    Handles both plain text and JSONL conversation log formats.
    Each result line: name: <Name> | bgg_id: <N> | status: <status> | notes: <notes>
    """
    # Try extracting from JSONL if plain-text parsing finds nothing
    text = _extract_text_from_jsonl(text)

    results = []
    in_block = False

    for line in text.splitlines():
        line = line.strip()
        if line == "RESULTS_START":
            in_block = True
            continue
        if line == "RESULTS_END":
            in_block = False
            continue
        if not in_block:
            continue

        # Parse: name: X | bgg_id: N | status: S | notes: N
        m = re.match(
            r"name:\s*(.+?)\s*\|\s*bgg_id:\s*(\d+)\s*\|\s*status:\s*(\w+)\s*\|\s*notes:\s*(.*)",
            line,
        )
        if m:
            results.append({
                "name": m.group(1).strip(),
                "bgg_id": int(m.group(2)),
                "status": m.group(3).strip(),
                "notes": m.group(4).strip(),
            })

    return results


def apply_results(results: list[dict], registry: str) -> dict[str, int]:
    """Update registry with parsed results. Returns status counts."""
    counts: dict[str, int] = {}
    for r in results:
        status = r["status"]
        counts[status] = counts.get(status, 0) + 1
        kwargs: dict = {"status": status}
        if r["notes"]:
            kwargs["notes"] = r["notes"]
        try:
            update_game(registry, r["name"], **kwargs)
            print(f"  OK: {r['name']} -> {status}")
        except Exception as e:
            print(f"  ERR: {r['name']}: {e}", file=sys.stderr)
    return counts


def main():
    parser = argparse.ArgumentParser(description="Collect subagent results and update registry")
    parser.add_argument("files", nargs="*", help="Result files to parse (default: stdin)")
    parser.add_argument("--registry", default="games.yaml", help="Path to games.yaml")
    args = parser.parse_args()

    # Read input
    if args.files:
        text = ""
        for path in args.files:
            with open(path) as f:
                text += f.read() + "\n"
    else:
        text = sys.stdin.read()

    results = parse_results(text)
    if not results:
        print("No RESULTS_START/RESULTS_END blocks found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(results)} results")
    counts = apply_results(results, args.registry)

    print(f"\nSummary:")
    for status, count in sorted(counts.items()):
        print(f"  {status}: {count}")
    print(f"  total: {len(results)}")


if __name__ == "__main__":
    main()
