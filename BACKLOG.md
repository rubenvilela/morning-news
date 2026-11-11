# Backlog: ideas for after v1

Things we chose not to do yet, and why. Each one has what's needed to pick it up later.

## Sources
- **Reuters** (added 2026-11-11). A wire service: factual, fairly neutral, a good baseline for comparing framing.
  - No official RSS any more (`feeds.reuters.com` no longer exists).
  - Only free route found: a Google News search feed,
    `https://news.google.com/rss/search?q=site:reuters.com+when:1d&hl=en-US&gl=US&ceid=US:en` (~100 items/day).
  - Downsides: links are Google redirect URLs (hard to fetch the full article in "tell me more"), unofficial use
    of Google News (can break), titles end in " - Reuters". Add as an *experimental* source.
- **Expresso** (Portuguese weekly, centre). Working feed: `https://feeds.feedburner.com/expresso-geral`.

## Ranking
- **Coverage count**: group the same story across outlets with text embeddings + clustering, and use
  "how many outlets covered it" as an importance signal next to the AI's judgment (approach C).
- **👍/👎 feedback** on each story, so the ranking learns what *I* find important.
