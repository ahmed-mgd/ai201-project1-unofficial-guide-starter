"""Milestone 4 — Retrieval smoke test.

Runs the evaluation-plan questions through retrieve() and prints the top-k
chunks with their cosine distances, so you can eyeball whether retrieval is
returning on-topic chunks before wiring up generation.

    python test_retrieval.py
"""

from __future__ import annotations

from vectorstore import retrieve

# The 5 questions from planning.md's Evaluation Plan.
QUERIES = [
    "I want to work out at Jesse Owens South in the evenings. What are the cheapest parking options?",
    "What are the best options for summer parking on north campus?",
    "Can I appeal a citation if I misread a parking sign?",
    "What are some general tips to save money on parking at OSU?",
    "Can I get a refund if I cancel or return my parking permit?",
]

K = 5
SNIPPET = 180


def main() -> None:
    for i, query in enumerate(QUERIES, 1):
        print("=" * 80)
        print(f"Q{i}: {query}")
        print("=" * 80)
        hits = retrieve(query, k=K)
        best = hits[0]["distance"] if hits else None
        for rank, hit in enumerate(hits, 1):
            text = " ".join(hit["text"].split())  # flatten newlines for display
            print(f"  {rank}. [dist {hit['distance']:.3f}] "
                  f"{hit['source']} ({hit['source_type']})")
            print(f"     {text[:SNIPPET]}{'...' if len(text) > SNIPPET else ''}")
        flag = "" if best is None or best < 0.5 else "   <-- best > 0.5, weak match"
        print(f"  best distance: {best:.3f}{flag}\n" if best is not None else "")


if __name__ == "__main__":
    main()
