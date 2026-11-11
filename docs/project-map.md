# Project map

Updated at the end of every step. Last update: end of Step 2b (2026-11-11).

## 1. Architecture: what the system is

Each box is a block (one module). Green = built, grey dashed = planned.

```mermaid
flowchart LR
    feeds[("RSS feeds<br/>11 outlets")]
    config[/"config.toml<br/>feeds · settings"/]
    sources["sources<br/>fetch · 24h filter · clean"]
    storage[("storage<br/>SQLite")]
    curation["curation<br/>group · rank · summarise"]
    ai["ai<br/>free LLM tier"]
    web[("web search")]
    messenger["messenger<br/>Telegram"]
    elaboration["elaboration<br/>tell me more"]
    scheduler["scheduler<br/>hourly fetch · 08:00 digest"]
    you(("you"))

    config --> sources
    feeds --> sources
    scheduler -. every hour .-> sources
    sources --> storage
    scheduler -. 08:00 .-> curation
    storage --> curation
    curation <--> ai
    curation --> messenger
    messenger --> you
    you -- reply to a story --> messenger
    messenger --> elaboration
    elaboration <--> ai
    elaboration --> web
    elaboration <--> storage
    elaboration --> messenger

    classDef done fill:#c8e6c9,stroke:#2e7d32,color:#000
    classDef planned fill:#f5f5f5,stroke:#9e9e9e,stroke-dasharray:4 3,color:#000
    class config,sources done
    class storage,curation,ai,web,messenger,elaboration,scheduler planned
```

Runs on: my PC for now → a free cloud server in Step 7.

## 2. Journey: how it got built

✅ built or decided · 🔀 change of plan · ⚠️ setback · 📋 moved to backlog

```mermaid
timeline
    title morning-news, how it got built
    section 2026-11-10 · Planning
        Idea : News scraper → digest at 08.00 → reply to dig deeper
        ⚠️ Setback : Tried to build everything at once → switched to step by step
        ✅ Decisions : RSS instead of scraping : Telegram : AI ranks with explicit criteria : Group the same story across outlets
        🔀 Change : Claude Pro can't power a bot → API route
        🔀 Change : Goal of $0 → free AI tier and swappable blocks
    section Step 0 · Setup
        ⚠️ Setback : Python 3.12 installed by mistake → removed
        ✅ Decision : Python 3.14, not 3.15 (library support)
        ⚠️ Setback : Windows blocked the venv script → execution policy
    section Step 1 · First feed
        ✅ Built : Read Observador, 51 articles
    section 2026-11-11 · Step 2 · All feeds
        ✅ Built : 11 feeds from config.toml : 24h filter : HTML cleaning of titles
        ⚠️ Setback : Telegraph blocks programs, WSJ feed dead → The Economist
        ⚠️ Setback : Economist International is an archive → latest feed
        ⚠️ Setback : Feeds are truncated (Público ≈ 1.5 h) → fetch hourly and store
        📋 Backlog : Reuters (no official feed) : Expresso
        ✅ Built : Project map (Mermaid) : Backlog and learning log
    section Step 2b · git and GitHub
        ✅ Built : git repository, first commit : Public repo with README
        ✅ Decision : Commits credit Claude as co-author : Learning log is public
```
