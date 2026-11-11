# morning-news

A Telegram bot that sends a news digest every morning at 08:00 (Europe/Lisbon),
curated by an AI model. Replying to a story starts a "tell me more" conversation.

## Hard constraint
- **Must cost $0.** Free tiers only (AI, web search, cloud). If a feature can't be free, flag it before building it.

## Decisions (2026-11-10)
- **Sources:** RSS feeds, in a config file. Areas: Portugal, World, Tech/AI.
  - Portugal: Observador, Público, RTP, ECO. World: BBC, Guardian, Al Jazeera + one centre-right outlet (to find).
  - Tech/AI: MIT Technology Review, Ars Technica, Hacker News.
- **Topics (configurable):** Portugal: politics and economy first, big court cases/scandals; football only if huge;
  skip celebrities and public figures.
- **Stories per section** set in config (start around Portugal 6, World 6, Tech/AI 4).
- **Duplicates are grouped, not dropped:** one summary per story listing every outlet that covered it;
  "tell me more" compares how each outlet framed it. Never hard-code political labels as fact.
- **App:** Telegram bot.
- **AI:** called through an API (not the Claude Pro subscription), behind a swappable provider layer
  (`rank_news()`, `elaborate()`). Start on a free tier (Gemini, to be confirmed in Step 3).
- **"Tell me more"** may search the web and must cite its sources.
- **Ranking v1:** the model picks using explicit criteria (impact, scale, novelty, relevance to me)
  and gives a one-line reason per pick.
- **Deferred ideas** live in `BACKLOG.md` (what, why not now, what's needed). Add to it whenever we decide
  "not now"; don't duplicate them here.

## Architecture: swappable blocks
Each block is one module with a small, fixed interface. Blocks talk only through shared data shapes
(`NewsItem` = one headline from a feed, `Story` = a grouped, summarised story), so replacing a block
(for example Gemini → Claude, or Telegram → Slack) means rewriting that block only.

| Block | Job | v1 choice |
|---|---|---|
| sources | fetch headlines → `list[NewsItem]` | RSS (feedparser) |
| ai | send a prompt, get text/JSON back (optionally with web search) | Gemini free tier (TBC) |
| curation | group duplicates, rank, summarise → `list[Story]` | AI with explicit criteria |
| elaboration | answer a question about a story | AI + web search |
| messenger | send the digest, receive replies | Telegram |
| storage | remember stories and conversations | SQLite |
| scheduler | trigger the digest at 08:00 | python-telegram-bot job queue |
| deployment | where it runs (not code) | local now, free cloud in Step 7 |

Rules: config and secrets come from `config.yaml` / environment variables, never hard-coded, so the code
runs the same on any machine or cloud. Draw clear boundaries, but don't build alternative implementations
of a block until one is actually needed.

## Known issues
- **Feeds are truncated, not paginated.** A feed holds only the publisher's last N items. Measured 2026-11-11:
  Público ~11 items ≈ 1.5 h, Observador 51 ≈ 4.5 h, RTP 50 ≈ 7 h. A single fetch at 08:00 would miss most of
  the previous day. Fix (to decide): fetch during the day and store items (storage block), digest reads from
  storage. Needs something running all day → ties to Step 7 (cloud).
  **Interval reasoning:** the fastest-moving feed sets the interval. Público covers ~1.5 h, so fetch about
  **every hour** (a margin below 1.5 h). Re-measure feed windows before fixing the value, and put the interval
  in `config.toml` with this reasoning as a comment.
- The Economist `/international/` feed is a section archive (items back to 2024, ~1 new/day) whose recent items
  also appear in `/latest/rss.xml` (~15 items/day), so config uses `/latest/` only.
## Git
- One repo for this project (`projects/morning-news/`), default branch `main`. I run the git commands myself.
- Commit messages: short summary of what changed (e.g. "Step 2: ..."), then the trailer
  `Co-Authored-By: Claude <noreply@anthropic.com>` to be open about AI help.
- Update the project map, learning log and CLAUDE.md before the end-of-step commit.

## Environment
- Python 3.14 (chosen over 3.15 for library compatibility), VS Code with the Python extension.

## Roadmap (one step at a time; Claude writes and explains the code)
0. Setup: Python, VS Code, folder, virtual environment  ✓ done
1. Read one RSS feed and print headlines  ✓ done
2. All feeds, date filter, config file, HTML cleaning of titles  ✓ done
   → then create `docs/project-map.md` (Mermaid: architecture map + project journey); update it at the end of every step  ✓ done
2b. git + GitHub: version history, private→public repo for CV, cloud sessions  ← current
3. AI ranks, groups and summarises (compare two free models)
4. Send the digest to Telegram
5. Daily 08:00 schedule
6. Reply → "tell me more" with web search and conversation memory (SQLite)
7. Run it on a free cloud server
