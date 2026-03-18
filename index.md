---
title: Board Game Rules
layout: home
---

# Board Game Rules

AI-friendly rules summaries for board games. Use these with **Claude**, **ChatGPT**, or any AI assistant to get instant rules answers — including via voice.

## How to Use

### With Claude (voice or text)

Start a conversation with Claude and paste this prompt:

```
You are a board game rules expert. I'll ask you questions about board games.
When I mention a game, fetch its rules from:
https://jonnyallred.github.io/boardgame-rules/rules/{slug}/
where {slug} is the game name in lowercase with hyphens (e.g., "ark-nova", "blood-on-the-clocktower").

The full list of available games is at:
https://jonnyallred.github.io/boardgame-rules/

Answer conversationally. Cite specific rules when relevant.
If a game isn't available, say so and offer general advice.
```

Then just ask questions — "How does trading work in Catan?" or "What happens when you run out of cards in Arcs?"

**For voice:** Paste the prompt into a Claude conversation on the mobile app, then switch to voice mode. Claude will remember the instructions and you can ask rules questions hands-free at the table.

### With ChatGPT, Gemini, or other assistants

The same prompt works — any AI assistant that can fetch web pages will pull the rules on demand.

---

## Available Games

| Game | Players | Time | Designer |
|------|---------|------|----------|
| [7 Wonders](rules/7-wonders/) | 3-7 | 30 min | Antoine Bauza |
| [Architects of the West Kingdom](rules/architects-of-the-west-kingdom/) | 1-5 | 60-80 min | S J Macdonald, Shem Phillips |
| [Arcs](rules/arcs/) | 2-4 | 60-120 min | Cole Wehrle |
| [Ark Nova](rules/ark-nova/) | 1-4 | 90-150 min | Mathias Wigge |
| [Azul](rules/azul/) | 2-4 | 30-45 min | Michael Kiesling |
| [Blood on the Clocktower](rules/blood-on-the-clocktower/) | 5-20 | 30-120 min | Steven Medway |
| [Catan](rules/catan/) | 3-4 | 60-120 min | Klaus Teuber |
| [Chinatown](rules/chinatown/) | 2-5 | 60-90 min | Karsten Hartwig |
| [Concordia](rules/concordia/) | 2-5 | 100 min | Mac Gerdts |
| [Cryptid](rules/cryptid/) | 3-5 | 30-50 min | Hal Duncan, Ruth Veevers |
| [Hansa Teutonica](rules/hansa-teutonica/) | 2-5 | 45-90 min | Andreas Steding |
| [Hey, That's My Fish!](rules/hey-thats-my-fish/) | 2-4 | 20 min | Günter Cornett, Alvydas Jakeliunas |
| [Nemesis](rules/nemesis/) | 1-5 | 90-180 min | Adam Kwapiński |
| [Pandemic](rules/pandemic/) | 2-4 | 45 min | Matt Leacock |
| [Pax Pamir: Second Edition](rules/pax-pamir-second-edition/) | 1-5 | 45-120 min | Cole Wehrle |
| [QE](rules/qe/) | 3-5 | 45-45 min | Gavin Birnbaum |
| [The Quacks of Quedlinburg](rules/quacks-of-quedlinburg/) | 2-4 | 45 min | Wolfgang Warsch |
| ↳ [The Herb Witches](rules/quacks-of-quedlinburg-the-herb-witches/) | 2-5 | 45 min | Wolfgang Warsch |
| ↳ [The Alchemists](rules/quacks-of-quedlinburg-the-alchemists/) | 2-4 | 45 min | Wolfgang Warsch |
| [Ready Set Bet](rules/ready-set-bet/) | 2-9 | 45-60 min | John D. Clair |
| [Rhino Hero](rules/rhino-hero/) | 2-5 | 5-15 min | Scott Frisco, Steven Strumpf |
| [Splendor](rules/splendor/) | 2-4 | 30 min | Marc Andre |
| [Star Wars: The Deckbuilding Game](rules/star-wars-the-deckbuilding-game/) | 2 | 30 min | Caleb Grace |
| [Ticket to Ride](rules/ticket-to-ride/) | 2-5 | 30-60 min | Alan R. Moon |

*{{ site.time | date: "%B %Y" }} · {{ site.pages | where_exp: "p", "p.path contains 'rules/'" | size }} games available*
