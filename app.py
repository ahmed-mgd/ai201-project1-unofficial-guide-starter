"""Milestone 5 — Gradio query interface for The Unofficial Guide.

Run:
    python app.py
then open http://localhost:7860
"""

import gradio as gr

from query import ask


def handle_query(question: str):
    if not question or not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    if not sources:
        sources = "(no sources — not enough information in the documents)"
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide — OSU Parking") as demo:
    gr.Markdown(
        "# The Unofficial Guide — OSU Parking\n"
        "Ask anything about parking at Ohio State. Answers are grounded **only** in "
        "collected r/OSU threads and official CampusParc / City of Columbus parking "
        "documents — if the documents don't cover it, the system says so."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. Can I get a refund on my parking permit?",
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
