"""Milestone 3 — Document ingestion and cleaning.

Loads every source file from documents/, parses its small header
(title / url / source_type), and cleans the body text so it is ready
for chunking. Implements the "load raw -> clean -> hand off to chunking"
step from planning.md.

Each document file looks like:

    title: r/OSU — "South campus parking"
    url: https://www.reddit.com/...
    source_type: reddit
    ---
    <the pasted post + comments / page text>

A file is SKIPPED (with a printed reason) if it is empty or still
contains the "<<< PASTE" placeholder sentinel, so unfilled templates
never pollute the vector store.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

DOCUMENTS_DIR = Path(__file__).parent / "documents"
PLACEHOLDER_SENTINEL = "<<<"  # matches "<<< PASTE" / "<<< NOT FILLED YET" markers

# Reddit UI boilerplate that adds no meaning. Matched per-line, case-insensitive.
REDDIT_UI_PATTERNS = [
    r"^\s*(reply|share|report|save|award|follow|give award|crosspost)\s*$",
    r"^\s*\d+\s*(points?|upvotes?|comments?|awards?)\s*$",
    r"^\s*[-+]?\d+\s*$",                       # bare vote counts
    r"^\s*(edit|edited)\b.*$",                 # "Edited 2y ago" lines
    r"^\s*level\s*\d+\s*$",                    # old-reddit comment nesting markers
    r"^\s*·.*ago\s*$",                         # "· 3 yr. ago" timestamp lines
    r"^\s*(vote|upvote|downvote)\s*$",
    r"^\s*continue this thread\s*$",
    r"^\s*more repl(y|ies).*$",
]
REDDIT_UI_RE = re.compile("|".join(REDDIT_UI_PATTERNS), re.IGNORECASE)


def _parse_header(raw: str) -> tuple[dict, str]:
    """Split the `key: value` header (before the `---`) from the body."""
    meta: dict = {}
    if "---" in raw:
        header, _, body = raw.partition("---")
        for line in header.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip().lower()] = value.strip()
        return meta, body
    # No header -> treat the whole file as body.
    return meta, raw


def _clean_common(text: str) -> str:
    """Cleaning applied to every document regardless of source."""
    text = html.unescape(text)                    # &amp; -> &, &nbsp; -> space
    text = text.replace(" ", " ")            # stray non-breaking spaces
    text = re.sub(r"[ \t]+", " ", text)           # collapse runs of spaces/tabs
    # Drop our own instruction comment lines (lines starting with '#').
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]
    text = "\n".join(lines)
    # Normalise blank lines: never more than one in a row.
    text = re.sub(r"\n[ \t]*\n[ \t]*(\n[ \t]*)+", "\n\n", text)
    return text.strip()


def _clean_reddit(text: str) -> str:
    """Reddit-specific cleaning: remove UI noise lines."""
    kept = [ln for ln in text.splitlines() if not REDDIT_UI_RE.match(ln)]
    text = "\n".join(kept)
    return _clean_common(text)


def load_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[dict]:
    """Return a list of cleaned document dicts ready for chunking.

    Each dict: {filename, title, url, source_type, text}
    """
    docs: list[dict] = []
    skipped: list[tuple[str, str]] = []

    for path in sorted(documents_dir.glob("*.txt")) + sorted(documents_dir.glob("*.md")):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        meta, body = _parse_header(raw)

        if PLACEHOLDER_SENTINEL in body:
            skipped.append((path.name, "still a placeholder (not filled in yet)"))
            continue

        source_type = meta.get("source_type", "reddit" if "reddit" in path.name else "official")
        text = _clean_reddit(body) if source_type == "reddit" else _clean_common(body)

        if len(text.strip()) < 20:
            skipped.append((path.name, "empty after cleaning"))
            continue

        docs.append(
            {
                "filename": path.name,
                "title": meta.get("title", path.stem),
                "url": meta.get("url", ""),
                "source_type": source_type,
                "text": text,
            }
        )

    if skipped:
        print(f"Skipped {len(skipped)} file(s):")
        for name, reason in skipped:
            print(f"  - {name}: {reason}")
    print(f"Loaded {len(docs)} document(s) from {documents_dir}/\n")
    return docs


if __name__ == "__main__":
    # Quick manual check: load and print the first cleaned document in full.
    documents = load_documents()
    if documents:
        first = documents[0]
        print("=" * 70)
        print(f"FIRST DOCUMENT: {first['title']}  ({first['source_type']})")
        print("=" * 70)
        print(first["text"])
