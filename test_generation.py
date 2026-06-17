"""Milestone 5 — End-to-end grounded generation test.

Runs a few in-corpus questions plus one out-of-scope question and prints
the grounded answer and the programmatically attached sources. Use this to
confirm (a) answers are traceable to retrieved chunks and (b) the system
declines on questions the documents don't cover.

    python test_generation.py
"""

from query import ask

IN_CORPUS = [
    "Can I get a refund if I return my parking permit?",
    "Can I appeal a citation if I misread a parking sign?",
    "I want to work out at Jesse Owens South in the evenings. What are the cheapest parking options?",
]
OUT_OF_SCOPE = "What are the best dining halls at Ohio State?"


def show(question: str) -> None:
    result = ask(question)
    print("=" * 80)
    print("Q:", question)
    print("-" * 80)
    print(result["answer"])
    print("\nRetrieved from:")
    for s in result["sources"]:
        print("  •", s)
    if not result["sources"]:
        print("  (none)")
    print()


if __name__ == "__main__":
    for q in IN_CORPUS:
        show(q)
    print("### OUT-OF-SCOPE — system should decline ###\n")
    show(OUT_OF_SCOPE)
