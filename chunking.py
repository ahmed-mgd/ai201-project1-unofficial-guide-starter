"""Milestone 3 — Chunking.

Implements the structure-aware strategy from planning.md:

- Split each document on blank-line boundaries into "blocks".
  * For Reddit docs, a block is the original post or a single comment,
    so each opinion becomes its own chunk (no blending of conflicting
    advice into one vector). Blocks are kept whole; an over-long block
    is sub-split into overlapping windows.
  * For official docs, consecutive small blocks (headings, short list
    items, paragraphs) are greedily PACKED together up to the size cap,
    so a heading stays attached to the content beneath it instead of
    becoming a useless fragment chunk. A single block bigger than the
    cap is sub-split into overlapping windows.

Size cap = 800 characters (~200 tokens), chosen to stay inside the
256-token limit of all-MiniLM-L6-v2. Overlap = 150 characters, applied
only when a long block is sub-split (relevant mainly to the longer
official pages).
"""

from __future__ import annotations

import re

MAX_CHARS = 800
OVERLAP_CHARS = 150
MIN_CHARS = 20  # drop fragments shorter than this
SHORT_LEAD_CHARS = 80  # a leading Reddit block this short is just the title line


def _split_blocks(text: str) -> list[str]:
    """Split on blank lines into paragraph/comment-sized blocks."""
    blocks = re.split(r"\n\s*\n", text)
    return [b.strip() for b in blocks if b.strip()]


def _split_long_block(block: str) -> list[str]:
    """Sub-split an over-long block into <=MAX_CHARS windows with overlap.

    Breaks at the nearest whitespace before the cap to avoid cutting words.
    """
    pieces: list[str] = []
    start = 0
    n = len(block)
    while start < n:
        end = min(start + MAX_CHARS, n)
        if end < n:
            # back up to the last whitespace so we don't split mid-word
            cut = block.rfind(" ", start, end)
            if cut > start:
                end = cut
        pieces.append(block[start:end].strip())
        if end >= n:
            break
        start = max(end - OVERLAP_CHARS, start + 1)
    return [p for p in pieces if p]


def _pack_blocks(blocks: list[str]) -> list[str]:
    """Greedily combine consecutive blocks up to MAX_CHARS (official docs).

    Keeps headings attached to the content that follows them. A block that
    is itself larger than the cap is flushed and sub-split on its own.
    """
    pieces: list[str] = []
    buffer = ""
    for block in blocks:
        if len(block) > MAX_CHARS:
            if buffer:
                pieces.append(buffer)
                buffer = ""
            pieces.extend(_split_long_block(block))
            continue
        candidate = f"{buffer}\n\n{block}" if buffer else block
        if len(candidate) <= MAX_CHARS:
            buffer = candidate
        else:
            pieces.append(buffer)
            buffer = block
    if buffer:
        pieces.append(buffer)
    return pieces


def _text_to_pieces(doc: dict) -> list[str]:
    """Apply the per-source chunking strategy and return raw text pieces."""
    blocks = _split_blocks(doc["text"])
    if doc["source_type"] == "reddit":
        # The first block is the thread title; if the original post put a blank
        # line right after it (e.g. "Title\nHey guys,\n\n...") the title lands in
        # its own tiny fragment. Merge that short leading block into the next so
        # the original post stays whole. Comments are left untouched.
        if len(blocks) >= 2 and len(blocks[0]) < SHORT_LEAD_CHARS:
            blocks = [f"{blocks[0]}\n\n{blocks[1]}", *blocks[2:]]
        # One comment/post per chunk; only sub-split if a block is too long.
        pieces: list[str] = []
        for block in blocks:
            pieces.extend([block] if len(block) <= MAX_CHARS
                          else _split_long_block(block))
        return pieces
    # Official docs: pack small blocks together so headings keep their context.
    return _pack_blocks(blocks)


def chunk_document(doc: dict) -> list[dict]:
    """Turn one cleaned document into a list of chunk dicts."""
    chunks: list[dict] = []
    for piece in _text_to_pieces(doc):
        piece = piece.strip()
        if len(piece) >= MIN_CHARS:
            chunks.append(
                {
                    "text": piece,
                    "source": doc["title"],
                    "source_type": doc["source_type"],
                    "url": doc["url"],
                    "filename": doc["filename"],
                    "char_len": len(piece),
                }
            )
    return chunks


def chunk_documents(docs: list[dict]) -> list[dict]:
    """Chunk every document, assigning a stable global id to each chunk."""
    all_chunks: list[dict] = []
    for doc in docs:
        for i, chunk in enumerate(chunk_document(doc)):
            chunk["chunk_id"] = f"{doc['filename']}::{i}"
            all_chunks.append(chunk)
    return all_chunks
