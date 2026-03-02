# Rules Lookup Skill — Design

## Purpose

A Claude Code skill that answers boardgame rules questions using a tiered lookup strategy, then automatically updates the rules summary and creates a PR when new information is found.

## Invocation

Slash command: `/rules Catan: can you steal from someone with no cards?`

Format: `/rules <game name>: <question>`

## File Structure

```
boardgame-rules/
  .claude/
    commands/
      rules.md              # slash command entry point
    skills/
      rules-lookup/
        SKILL.md             # main skill logic
```

## Tiered Lookup Workflow

**Tier 1 — Summary file:** Read `rules/<game>.md`. If the answer is there, cite the section.

**Tier 2 — Extracted text:** Read `extracted/<game>*.txt`. Search raw rulebook for details not in summary. Flag that summary needs updating.

**Tier 3 — BGG web search:** WebSearch `site:boardgamegeek.com "<game>" <keywords>`. Look for consensus from forum discussions. Include source URL.

**Tier 4 — Intuition:** Best-guess based on game mechanics and conventions. Clearly labeled "unverified."

Stop at first tier that yields an answer. Always state which tier the answer came from.

## Answer Format

Each answer includes:
- The answer itself
- Source tier (summary / extracted rulebook / BGG forum / intuition)
- Confidence level (high / medium / low)
- Relevant section or URL citation

## Auto-Update & PR Flow

After answering, if new information was found (Tiers 2-4):

1. Create branch: `rules-update/<game>-<short-slug>`
2. Edit `rules/<game>.md` — add info to appropriate section with source annotation
3. Commit with descriptive message
4. Push and `gh pr create`
5. Return PR URL to user

For intuition-sourced updates: PR description marks the addition as "unverified."

If the game has no summary file: skip update, suggest adding the game to the database.

## Approach

Single-file skill (SKILL.md) with no helper scripts. Claude uses its built-in tools: Read, Grep, Edit, WebSearch, Bash (for git/gh).

## Decisions

- **Project-scoped skill**: Lives in repo's `.claude/` — only active when working in this project
- **Slash command**: Explicit `/rules` invocation, not auto-detect
- **Always update on new info**: Including intuition (clearly marked in PR)
- **PR not direct commit**: Allows review before merging, especially for intuition-sourced additions
