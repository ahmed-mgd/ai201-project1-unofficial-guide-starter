"""Milestone 5 — Grounded answer generation.

Retrieves context with vectorstore.retrieve(), then asks Groq's
llama-3.3-70b-versatile to answer using ONLY that context. The system
prompt enforces grounding (no outside knowledge; decline when the context
is insufficient), and source attribution is built programmatically from
the retrieved chunks — it is never left to the model to invent.

    from query import ask
    ask("Can I get a refund on my parking permit?")
    # -> {"answer": "...", "sources": ["CampusParc — Returns... (official) — https://..."]}

CLI:
    python query.py "your question here"
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from groq import Groq

from vectorstore import retrieve

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
TOP_K = 5
DECLINE = "I don't have enough information on that."

SYSTEM_PROMPT = (
    "You are The Unofficial Guide, an assistant that answers questions about "
    "parking at The Ohio State University. Answer the user's question using ONLY "
    "the information in the provided context documents. Follow these rules strictly:\n"
    "- Use only facts found in the context. Never use outside or prior knowledge.\n"
    f'- If the context does not contain enough information to answer the question, '
    f'reply with exactly: "{DECLINE}" and nothing else.\n'
    "- When the sources disagree, say so instead of silently picking one.\n"
    "- Note when a claim is student opinion (Reddit) versus official policy.\n"
    "Be concise and specific."
)

_client: Groq | None = None


def _groq() -> Groq:
    """Create the Groq client once, with a clear error if the key is missing."""
    global _client
    if _client is None:
        key = os.environ.get("GROQ_API_KEY")
        if not key or key == "your_key_here":
            raise RuntimeError(
                "GROQ_API_KEY is not set. Copy .env.example to .env and add your "
                "Groq API key (free at https://console.groq.com)."
            )
        _client = Groq(api_key=key)
    return _client


def _format_context(hits: list[dict]) -> str:
    """Number each retrieved chunk and label it with its source for the prompt."""
    return "\n\n".join(
        f"[{i}] (source: {h['source']} — {h['source_type']})\n{h['text']}"
        for i, h in enumerate(hits, 1)
    )


def _format_sources(hits: list[dict]) -> list[str]:
    """Deduplicate retrieved sources (first-seen order) for attribution."""
    seen: set[str] = set()
    sources: list[str] = []
    for h in hits:
        if h["source"] in seen:
            continue
        seen.add(h["source"])
        label = f"{h['source']} ({h['source_type']})"
        if h.get("url"):
            label += f" — {h['url']}"
        sources.append(label)
    return sources


def _is_decline(answer: str) -> bool:
    return "i don't have enough information" in answer.lower()


def ask(question: str, k: int = TOP_K) -> dict:
    """Answer a question grounded only in the retrieved chunks.

    Returns {"answer": str, "sources": list[str]}. Sources are attached only
    when the model actually answered (an "I don't have enough information"
    decline returns no sources).
    """
    hits = retrieve(question, k=k)
    response = _groq().chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Context documents:\n\n{_format_context(hits)}\n\n"
                           f"Question: {question}",
            },
        ],
    )
    answer = response.choices[0].message.content.strip()
    sources = [] if _is_decline(answer) else _format_sources(hits)
    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    import sys

    q = " ".join(sys.argv[1:]) or "Can I get a refund if I return my parking permit?"
    result = ask(q)
    print("Q:", q)
    print("\nANSWER:\n" + result["answer"])
    print("\nSOURCES:")
    for s in result["sources"]:
        print("  •", s)
    if not result["sources"]:
        print("  (none)")
