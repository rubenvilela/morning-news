# Learning log: morning-news

## Step 0–1: Setup and first feed

### RSS (Really Simple Syndication)
- **What:** a standard shared by many websites. For news outlets, it's a file (in XML format) the site
  publishes for programs to read, instead of the web page made for people.
- **Why:** every site uses the same structure (title, link, date, summary), so one code snippet works for all of them.
- **Gotcha:** not every site has a feed, and feed URLs break (`publico.pt/rss` gave a 404, the feedburner one worked).
  Also, not everything in a feed is an article (radio bulletins, `/programas/`), and dates arrive as text, in UTC.

### Virtual environment
- **What:** a closed box with all the libraries my code needs, at the specific versions it needs.
  It still runs on the Python installed on the computer.
- **Why:** two projects can have different library versions without affecting one another.
- **How:** `python -m venv .venv` creates it, `.venv\Scripts\Activate.ps1` activates it,
  and `(.venv)` at the start of the prompt means it's active.
- **Gotcha:** on Windows, activation is blocked by the script execution policy. Fix it once with
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- `.venv` is never uploaded (it's in `.gitignore`); it gets rebuilt from `requirements.txt`.

### `python -m`
- **What:** a Python flag (not PowerShell; it works in any terminal) that runs a module by its import name
  instead of its file path, so `package.module` instead of `folder\project\module.py`.
- **Why:** when I run `python -m morning_news.sources`, Python knows `sources` belongs to the
  `morning_news` package. So if `sources` needs another module from the same package
  (`from .config import ...`, where the `.` means "my own package"), Python looks for it there.
  When I run the file by its path (`python morning_news\sources.py`), Python treats it as a standalone
  script with no package, so `.config` has nowhere to look and fails.
- **Gotcha:** running by file path works until a module imports another one from its own package; then it fails with
  `ImportError: attempted relative import with no known parent package`.
  Tip: read a traceback from the last line up (the last line says *what*, the lines above say *where*).

## Step 2: All feeds, config file, date filter

### TOML (Tom's Obvious, Minimal Language)
- **What:** a format for config files. `#` starts a comment, `key = value` is a setting, and `[[x]]` adds one more
  item to a list called `x`. Each item becomes a dictionary (named fields, like a table row), not a tuple.
  Similar to JSON, but JSON is mostly for programs exchanging data and doesn't allow comments; TOML is made
  for people to read and edit.
- **Why:** to change settings (lookback hours, feeds) without touching the code. Cleaner and easier to read.
- **Gotcha:** plain settings must come before the first `[[x]]`, otherwise TOML treats them as part of the last item.
  And `[x]` (one group) is not `[[x]]` (one more item in a list).

### Docstring
- **What:** text in triple quotes (`"""`). It works like a comment, but Python keeps it: in VS Code, hovering over
  a module or function shows it as a description (and `help(...)` in the REPL prints it).
- **Gotcha:** it has to be the first line of the module or function, otherwise it's just an ignored string.

### File modes and encoding (`"r"` vs `"rb"`)
- **What:** files on disk are always bytes. `"rb"` (read binary) gives the raw bytes; `"r"` also decodes them
  into text using an encoding (the rule that maps bytes to characters).
- **Why:** `tomllib` needs `"rb"` so it decodes the bytes itself, always as UTF-8. With `"r"` it raises
  `TypeError: File must be opened in binary mode`.
- **Gotcha:** on Windows, `"r"` has traditionally decoded with cp1252 instead of UTF-8, which can garble accents
  ("Público" → "PÃºblico"). When opening text files myself, write `open(path, "r", encoding="utf-8")`.

### Truncated feeds
- **What:** RSS feeds only hold the publisher's last N articles, not every article ever, and there's no "page 2".
- **Why it matters:** a digest of the last 24 h can't fetch once a day; the parser has to run several times a day
  and store what it collects. The fastest feed sets the interval (Público ≈ 1.5 h → about every hour).
- **Gotcha:** you can spot truncation when found = recent (e.g. "51 found, 51 recent").

### Aware vs naive dates
- **What:** dates with a time zone (aware) or without one (naive).
- **Why it matters:** a naive "08:00" is ambiguous (Lisbon? UTC? New York?), so near the 24 h cutoff an article
  can be wrongly kept or dropped.
- **Gotcha:** comparing a naive date with an aware one raises a `TypeError`; that's why the code adds `tzinfo=timezone.utc`.

### Regex (regular expressions)
- **What:** a pattern that describes text. `re.sub(pattern, replacement, text)` means: in `text`, replace everything
  matching `pattern` with `replacement` (like Excel's SUBSTITUTE, but with a pattern).
- **Example:** `<[^>]+>` matches any HTML tag. Write patterns as raw strings: `r"..."`.

### REPL
- **What:** the interactive Python prompt (`>>>`) you get by typing `python` with no file. Every line is treated as Python
  and its result is shown immediately, until `exit()`.
- **Why:** to explore code and data piece by piece, e.g. `from morning_news.config import load_config`.

### List comprehensions
- **What:** a loop written in one line that creates a new list: `[expression for n in numbers if condition]`.
  The expression comes first and is what goes into the new list for each item (it can be transformed, e.g. `n * 2`);
  then the loop logic (`for n in numbers`, so all the `n`s); and, if there's an `if`, the condition that decides
  which items are kept.
- **Example:** `recent = [h for h in headlines if h["published"] >= cutoff]` is our date filter.
- **Gotcha:** keep them simple; when the logic gets complicated, a normal loop is easier to read.
