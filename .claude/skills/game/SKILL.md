---
name: game
description: Use when the user invokes /game <name> to load a game's rules summary into context for conversational Q&A. Do not use for specific rules questions that need deep lookup — use rules-lookup for that.
---

# Game Loader

Load a game's rules summary into context so the user can ask questions conversationally.

## Input

The user provides: `<game name>`

Example: `/game catan`

## Steps

1. **Parse the game name** from the arguments. Slugify it (lowercase, hyphens for spaces).

2. **Find the summary file:**
   - Glob for `rules/<slug>*.md`
   - If not found, check `games.yaml` for a matching game name
   - If the game doesn't exist in the database, tell the user and suggest: `python -m scripts.find_rulebook "<game>"`

3. **Read the full summary file** using the Read tool.

4. **Respond with:**
   - A short confirmation: "Loaded **<Game Title>** rules. Ask me anything."
   - Key stats from frontmatter: player count, play time, designer
   - Do NOT summarize the rules — the user will ask what they need

## When You Can't Answer

If the user asks a question and the loaded summary doesn't cover it, say:

> I don't see that in the summary. For a deeper lookup (extracted rulebook, BGG forums), try:
> `/rules <game>: <question>`

## Important

- Do NOT create branches, PRs, or edit files. This skill is read-only.
- The summary is now in context — answer follow-up questions directly from it without re-reading the file.
- Keep answers concise and cite the relevant section when possible.
