"""Sources block: reads news headlines from RSS feeds."""

import html
import re
from datetime import datetime, timedelta, timezone

import feedparser

from .config import load_config  # the "." means: from this same package


def clean_text(text: str) -> str:
    """Remove HTML tags and codes from a piece of text, and tidy the spaces."""
    text = re.sub(r"<[^>]+>", "", text)  # 1. drop tags such as <em> and </em>
    text = html.unescape(text)           # 2. turn codes such as &amp; into &
    return " ".join(text.split())        # 3. collapse repeated spaces and line breaks


def parse_date(entry) -> datetime | None:
    """Return the article's publication date as a UTC datetime, or None if it has none."""
    # feedparser has already turned the date text into numbers (year, month, day, hour, ...),
    # always converted to UTC. Some feeds only give an "updated" date, so we try both.
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed is None:
        return None
    # parsed[:6] is (year, month, day, hour, minute, second); the * spreads them out as arguments.
    return datetime(*parsed[:6], tzinfo=timezone.utc)


def fetch_headlines(url: str) -> list[dict]:
    """Download one RSS feed and return its articles as a list of dictionaries."""
    feed = feedparser.parse(url)

    headlines = []
    for entry in feed.entries:
        headlines.append({
            "title": clean_text(entry.get("title", "")),
            "link": entry.get("link", ""),
            "published": parse_date(entry),  # a datetime, or None
        })
    return headlines


def fetch_all_feeds() -> list[dict]:
    """Read every feed in config.toml and return the recent headlines in one list."""
    config = load_config()

    # The oldest moment we still accept: now minus N hours.
    cutoff = datetime.now(timezone.utc) - timedelta(hours=config["lookback_hours"])
    print(f"Keeping articles published after {cutoff:%Y-%m-%d %H:%M} UTC\n")

    all_headlines = []
    for feed in config["feeds"]:
        headlines = fetch_headlines(feed["url"])
        if not headlines:
            print(f"WARNING: no articles from {feed['name']} ({feed['url']})")

        # Keep articles newer than the cutoff. Articles with no date are kept too,
        # so we never lose news silently; we count them to see how often it happens.
        recent = [h for h in headlines if h["published"] is None or h["published"] >= cutoff]
        no_date = sum(1 for h in recent if h["published"] is None)

        # Remember where each headline came from: we need it to compare outlets later.
        for h in recent:
            h["source"] = feed["name"]
            h["area"] = feed["area"]

        line = f"{feed['name']:<22} {len(headlines):>3} found, {len(recent):>3} recent"
        if no_date:
            line += f" ({no_date} without a date)"
        print(line)
        all_headlines.extend(recent)
    return all_headlines


# This block only runs when you start this file directly,
# not when another file imports from it.
if __name__ == "__main__":
    headlines = fetch_all_feeds()
    print(f"\nTotal: {len(headlines)} recent articles\n")

    # Sample: the first 2 headlines of each source, to check the data looks right.
    shown_per_source = {}  # e.g. {"Observador": 2, "Público": 1}
    for h in headlines:
        count = shown_per_source.get(h["source"], 0)
        if count < 2:
            print(f"- [{h['source']}] {h['title']}")
            print(f"    published: {h['published']}")
            shown_per_source[h["source"]] = count + 1
