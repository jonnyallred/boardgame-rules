---
name: rules-lookup
description: Use when the user asks a boardgame rules question via /rules command, or asks about rules for a game that exists in the rules/ directory. Answers using a tiered lookup (summary file, extracted rulebook, BGG forums, intuition) and auto-creates a PR to update the rules summary when new information is found.
---

# Rules Lookup Skill

Answer boardgame rules questions using a tiered lookup strategy. When new information is found beyond what's in the summary, automatically update the summary and create a PR.

## Input Format

The user provides: `<game name>: <question>`

Example: `Catan: can you steal from a player who has no resource cards?`

## Step 1: Identify the Game

Parse the game name from the input. Find the matching files:

1. Use Glob to find `rules/<game>*.md` (try lowercase, slugified name)
2. Use Glob to find `extracted/<game>*.txt`
3. If no files found, check `games.yaml` for the game name
4. If the game doesn't exist in the database at all, tell the user and suggest adding it with `python -m scripts.find_rulebook "<game>"`

## Step 2: Tiered Lookup

Work through tiers in order. **Stop at the first tier that provides a clear answer.**

### Tier 1 — Summary File

Read `rules/<game>.md`. Search for the answer to the user's question.

- Use Grep to search for keywords from the question
- Read the relevant sections
- If the answer is clearly stated, **answer and stop** (no update needed)

### Tier 2 — Extracted Rulebook Text

Read `extracted/<game>*.txt`. Search the raw extracted text for details not captured in the summary.

- Use Grep to search for keywords
- Read surrounding context (±20 lines) around matches
- If the answer is found here, **answer and proceed to Step 3** (update needed)

### Tier 3 — BGG Web Search

Search BoardGameGeek forums for the answer.

- Use WebSearch: `site:boardgamegeek.com "<game name>" <key question terms>`
- Look for official rulings, designer clarifications, or strong community consensus
- If found, **answer with the source URL and proceed to Step 3** (update needed)

### Tier 4 — Intuition

If no authoritative source answers the question:

- Reason from the game's mechanics as described in the summary and rulebook
- Consider common boardgame conventions
- **Clearly label the answer as "Unverified — based on game conventions, not official rules"**
- Provide your reasoning
- **Proceed to Step 3** (update needed, marked as unverified)

## Answer Format

Always format your answer as:

```
## Answer

[The answer to the question]

**Source:** [Summary | Extracted Rulebook | BGG Forum (URL) | Intuition (unverified)]
**Confidence:** [High | Medium | Low]
**Section:** [Which section of the rules this falls under, if applicable]
```

## Step 3: Auto-Update Rules Summary

**Only proceed here if the answer came from Tier 2, 3, or 4** (i.e., the summary was missing this information).

**If the game has no summary file (`rules/<game>.md`):** Skip this step. Tell the user the game needs to be added to the database first.

### Create Branch and Update

1. **Create a branch:**
   ```bash
   git checkout -b rules-update/<game>-<short-question-slug>
   ```
   Use a short slug from the question (e.g., `catan-robber-no-cards`).

2. **Edit the summary file** (`rules/<game>.md`):
   - Add the new information to the most appropriate existing section
   - For Tier 3 (BGG) answers, add a brief note: `<!-- Source: BGG forum <URL> -->`
   - For Tier 4 (intuition) answers, add: `<!-- UNVERIFIED: Based on game conventions, not official rules -->`
   - Keep the existing style and level of detail

3. **Commit:**
   ```bash
   git add rules/<game>.md
   git commit -m "rules(<game>): add <brief description of what was added>"
   ```

4. **Push and create PR:**
   ```bash
   git push -u origin rules-update/<game>-<short-question-slug>
   gh pr create --title "rules(<game>): <brief description>" --body "$(cat <<'EOF'
   ## Rules Update

   **Game:** <game>
   **Question:** <user's original question>
   **Answer:** <brief answer>
   **Source:** <tier and source details>

   ### Changes
   - Added <what was added> to the <section> section

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

5. **Switch back to main:**
   ```bash
   git checkout main
   ```

6. **Report the PR URL** to the user.

## Common Mistakes

- **Don't skip tiers.** Always start with Tier 1, even if you think the answer won't be there.
- **Don't update if Tier 1 answered it.** The summary already has the info.
- **Don't forget to switch back to main** after creating the PR.
- **Don't create a PR for a game with no summary file.** Just answer the question.
- **Always cite the source tier.** The user needs to know where the answer came from.
