"""Milestone 3 — Build and inspect chunks.

Runs the full ingestion + chunking pipeline, then:
  1. prints the total chunk count and a size sanity-check,
  2. prints 5 representative chunks for manual inspection,
  3. writes all chunks to chunks.jsonl for Milestone 4 (embedding).

Usage:
    python build_chunks.py
"""

from __future__ import annotations

import json
from pathlib import Path

from chunk import MAX_CHARS, chunk_documents
from ingest import load_documents

OUTPUT_PATH = Path(__file__).parent / "chunks.jsonl"


def representative_chunks(chunks: list[dict], n: int = 5) -> list[dict]:
    """Pick up to n chunks from as many different source files as possible."""
    picked: list[dict] = []
    seen_files: set[str] = set()
    # First pass: one chunk per distinct source file (for variety).
    for chunk in chunks:
        if chunk["filename"] not in seen_files:
            picked.append(chunk)
            seen_files.add(chunk["filename"])
        if len(picked) == n:
            return picked
    # Second pass: fill remaining slots with evenly spaced chunks.
    if chunks:
        step = max(1, len(chunks) // n)
        for i in range(0, len(chunks), step):
            if chunks[i] not in picked:
                picked.append(chunks[i])
            if len(picked) == n:
                break
    return picked[:n]


def main() -> None:
    docs = load_documents()
    if not docs:
        print("No filled-in documents found. Paste content into documents/*.txt "
              "(replace the '<<< PASTE' placeholder), then re-run.")
        return

    chunks = chunk_documents(docs)
    total = len(chunks)

    # --- Size sanity check (guidance from the milestone) ---
    sizes = [c["char_len"] for c in chunks]
    print(f"Total chunks: {total}")
    print(f"Chunk size (chars): min={min(sizes)}  max={max(sizes)}  "
          f"avg={sum(sizes) // total}")
    over_cap = sum(1 for s in sizes if s > MAX_CHARS)
    print(f"Chunks over the {MAX_CHARS}-char cap: {over_cap} (should be 0)")
    if total < 50:
        print("WARNING: fewer than 50 chunks — chunks may be too large, or you "
              "still have documents left to fill in.")
    elif total > 2000:
        print("WARNING: more than 2000 chunks — chunks may be too small.")
    print()

    # --- 5 representative chunks for inspection ---
    samples = representative_chunks(chunks, 5)
    print("=" * 70)
    print("5 REPRESENTATIVE CHUNKS (inspect these; copy into README.md)")
    print("=" * 70)
    for i, c in enumerate(samples, 1):
        print(f"\n--- Chunk {i} | source: {c['source']} ({c['source_type']}) "
              f"| {c['char_len']} chars | id: {c['chunk_id']} ---")
        print(c["text"])

    # --- Persist for Milestone 4 ---
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"\nWrote {total} chunks to {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
