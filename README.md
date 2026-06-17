# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/OSU — "Parking help please" | Reddit | https://www.reddit.com/r/OSU/comments/1q45gjx/parking_help_please/ |
| 2 | r/OSU — "What parking permit should I get?" | Reddit | https://www.reddit.com/r/OSU/comments/1mcrmis/what_parking_permit_should_i_get/ |
| 3 | r/OSU — "South campus parking" | Reddit | https://www.reddit.com/r/OSU/comments/1l8h0ph/south_campus_parking/ |
| 4 | r/OSU — "Parking garage availability" | Reddit | https://www.reddit.com/r/OSU/comments/1rcujuj/parking_garage_availability/ |
| 5 | r/OSU — "Street parking during school year" | Reddit | https://www.reddit.com/r/OSU/comments/1ld1hw1/street_parking_during_school_year/ |
| 6 | r/OSU — "Public parking help" | Reddit | https://www.reddit.com/r/OSU/comments/1fvb7j2/public_parking_help/ |
| 7 | r/OSU — "Worth it to appeal parking citation?" | Reddit | https://www.reddit.com/r/OSU/comments/1lr4cd3/worth_it_to_appeal_parking_citation/ |
| 8 | r/OSU — "Parking tips for someone who doesn't go here" | Reddit | https://www.reddit.com/r/OSU/comments/1ke38zh/parking_tips_for_someone_who_doesnt_go_here/ |
| 9 | CampusParc — Off-Peak Permit Parking | Official | https://osu.campusparc.com/find-parking/off-peak-permit-parking/ |
| 10 | CampusParc — Returns, Refunds & Exchanges | Official | https://osu.campusparc.com/get-a-permit/returns-refunds-exchanges/ |
| 11 | City of Columbus — University District Parking FAQ (PDF) | Official (PDF) | https://www.columbus.gov/files/sharedassets/city/v/1/services/ud-website-faq-_updated-6_10_21.pdf |

**Ingestion process.** Reddit and Columbus.gov block automated scraping, so the raw sources were collected once in the browser (archived under `documents/raw/`) and converted to a consistent plain-text format with a small `title / url / source_type` header: Reddit threads from their `.json` (one comment per blank-line block; deleted/removed/AutoModerator comments and one-liners dropped), the CampusParc pages from their main content area, and the Columbus FAQ extracted from its PDF. The resulting files live in `documents/`. `ingest.py` then loads every file, parses its header, and cleans the body — decoding HTML entities, stripping non-breaking spaces, and removing Reddit UI noise (Reply/Share/vote counts/timestamps) — before handing the text to `chunking.py`. Run the whole pipeline with `python build_chunks.py`, which writes `chunks.jsonl` and prints the chunk count and sample chunks.

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** Max 800 characters (~200 tokens) per chunk.

**Overlap:** 150 characters, applied only when a single block exceeds the cap and must be sub-split. Reddit comments are kept whole and need no overlap.

**Why these choices fit your documents:** The 800-char cap keeps every chunk inside the 256-token input limit of `all-MiniLM-L6-v2` (longer text is silently truncated). The corpus has two shapes, so chunking is structure-aware: Reddit threads are split one-comment-per-chunk so conflicting opinions never blend into one vector, while official pages have their short blocks (headings, list items, paragraphs) greedily packed up to the cap so a heading stays attached to the content beneath it. Preprocessing strips HTML entities, non-breaking spaces, and Reddit UI noise (Reply/Share/vote counts/timestamps) before chunking. See `ingest.py` and `chunking.py`.

**Final chunk count:** 108 chunks across 11 documents (8 Reddit threads + 3 official pages/PDF). Sizes range 20–799 characters (avg ~311); none exceed the 800-character cap.

---

## Sample Chunks

<!-- Paste 5 representative chunks from your document collection after running your ingestion pipeline.
     For each chunk, note which source document it came from.
     These must be actual text — not screenshots. -->

| # | Source document | Chunk text |
|---|----------------|------------|
| 1 | `03_reddit_south_campus.txt` (Reddit answer) | - Neil Ave in front of King Ave Methodist Church (west side only)<br>- W 7th in front of H2O church (north side only)<br>- King Ave between Hunter and Highland (north side only)<br>- E 8th, E 9th, E 11th |
| 2 | `07_reddit_appeal_citation.txt` (Reddit answer) | If it's a legit ticket, they probably won't dismiss it altogether. But if it's your first time, they might reduce it down quite a bit. In that case, submit an appeal and just be polite and honest about what happened. Worst case is they say no, best case you pay a fraction of the fine. |
| 3 | `09_campusparc_offpeak.txt` (Official) | Off-Peak Permit Parking<br><br>When there is less demand for parking on weekday evenings, weekends and holidays, more parking access becomes available for permit holders.<br><br>Off-Peak Hours are defined as:<br><br>Weekday Evenings: 4:00 p.m. - 3:00 a.m. Monday - Thursday<br><br>Weekends: 4:00 p.m. Friday - 3:00 a.m. Monday<br><br>University Holidays: 12:01 a.m. - 3:00 a.m. the following day<br><br>During off-peak hours:<br><br>9th Avenue East, Arps, Neil and Union North garages become available for visitor and keycard use.<br><br>Check out your permits webpage for access details<br><br>WA, WAE, WB, WC, WCO and CX permits are valid in unreserved Central Campus A, B, or C spaces<br><br>Motorcycles are permitted to park in four-wheel vehicle parking spots |
| 4 | `10_campusparc_refunds.txt` (Official) | Refunds for current or prior months are not available; payment remains the permit holder's responsibility. Upon permit return, a temporary multi-day surface lot permit can be provided for use for the remainder of the month upon request. Permits should be returned by the close of business on the last working day of the month to avoid being charged for the following month.<br><br>Purchased in Full: Customers returning an annual permit purchased in full will receive a prorated refund, excluding the current and prior months. |
| 5 | `11_columbus_ud_faq.txt` (Official PDF) | 8. Am I eligible for a guest permit? Residents in permit zone UDA are entitled to 1 guest permit per address (for $25) in addition to 1 residential permit per licensed driver. All other UD zones are not eligible for guest permits. Guest parking in zones UDB and UDC is accommodated through paid parking using the ParkColumbus mobile application.<br><br>9. How much does a permit cost? Residential permit fees follow the structure below. Prices increase to manage demand. Residences are limited to 1 permit for each licensed driver in the household, up to 6 licensed drivers. ● Permits 1-2: $25 each ● Permit 3: $50 ● Permit 4: $100 ● Permit 5: $200 ● Permit 6: $300 |

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` (384-dimensional embeddings, runs locally with no API key or rate limits). Chunks are embedded with normalized vectors and stored in a persistent **ChromaDB** collection (`parking_chunks`) using **cosine** distance, so a retrieval score is `1 - cosine_similarity` (0 = identical meaning; lower is better). Each stored chunk carries metadata for attribution: `source`, `source_type` (reddit/official), `url`, `filename`, and `position`. Retrieval uses **top-k = 5**. See `vectorstore.py`.

**Production tradeoff reflection:** If I were deploying this for real users and cost weren't a constraint:
- **Accuracy on opinion text:** I'd test a stronger model like `all-mpnet-base-v2` (768-dim) or an API model (`text-embedding-3-large`). Short, sarcastic, slangy Reddit opinions are exactly where the small MiniLM model loses nuance.
- **Context length:** MiniLM's 256-token cap forces me to keep chunks small. A long-context embedding model would let me embed whole official sections intact, keeping related rules together.
- **Local vs. API:** local (current) = free, private, no rate limits, but a lower accuracy ceiling and uses my own compute. API = higher accuracy and zero infra, but per-call cost at scale and sends data to a third party.
- **Multilingual:** not needed — this corpus is all English, so I would not pay for a multilingual model here.
- **Latency:** local embedding is fine for a 108-chunk corpus; for thousands of live queries I'd weigh a hosted model or a quantized local one.

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:** *"I want to work out at Jesse Owens South in the evenings. What are the cheapest parking options?"*

Top returned chunks (full text):

1. **[dist 0.370] *South Campus Parking* (reddit):** "King has big stretches of free street parking. Half mile from Jesse Owens, tops"
2. **[dist 0.485] *Public Parking Help* (reddit):** "Public Parking Help Hello, I am a sophomore here at OSU, and I'm looking at bringing a vehicle down here next week to help make travel easier for me and my family. Im curious, is there any parking, such as like roadside parking that is free that I could possibly keep a car at overnight and move every day or two? I'm willing to walk some miles to anything."
3. **[dist 0.487] *South Campus Parking* (reddit):** "South Campus Parking Can anyone explain how parking around south campus would work? My family is visiting for the next couple days, and I wasn't sure what parking would be available to them. I live off campus by JOS, and I was wondering if there's street parking or a safe/cheap garage?"

Relevance explanation: The top hit directly names free street parking a half-mile from Jesse Owens. This is exactly what the query asks for, and it's from the right source (the South Campus thread). The other two are people asking about the same cheap/free parking near JOS and south campus, so they surround the answer with relevant context. Best distance 0.370 (< 0.5).

---

**Query 2:** *"Can I appeal a citation if I misread a parking sign?"*

Top returned chunks (full text):

1. **[dist 0.358] *Worth it to Appeal Parking Citation?* (reddit):** "Worth it to Appeal Parking Citation? Hey guys, I parked outside my research labs parking lot, which I am not supposed to, but I was only going to be there for an hour. Unfortunately campusparc caught me and hit me with a $56 fine. Is it worth appealing, and what would I even say?"
2. **[dist 0.359] *Worth it to Appeal Parking Citation?* (reddit):** "I've appealed both my citations online and it worked. However, in those cases, I got the citations because I reverse parked and my license plate wasn't showing. I wasn't even sure what the problem was until I called them and they clarified it for me. I think it's worth a shot to appeal!"
3. **[dist 0.383] *Worth it to Appeal Parking Citation?* (reddit):** "No. You parked someplace you were not supposed to park. You have no defense. Appealing is for when they messed up and you were not supposed to be ticketed. That's not you, you should have been ticketed and you were. You probably won't do that again… that's the point of a ticket."

Relevance explanation: Every hit comes from the citation-appeal thread and speaks directly to whether an appeal works, which is relevant to the scenario behind "misread a sign." The chunks usefully disagree: one says appeals worked, but only because the citation itself was questionable (plate not showing), while another flatly says there is "no defense" if you genuinely parked where you shouldn't have. That tension is ideal grounding for a nuanced, honest answer. Best distance 0.358.

---

**Query 3:** *"Can I get a refund if I cancel or return my parking permit?"*

Top returned chunks (full text):

1. **[dist 0.348] *CampusParc — Returns, Refunds & Exchanges* (official):** "Refunds for current or prior months are not available; payment remains the permit holder's responsibility. Upon permit return, a temporary multi-day surface lot permit can be provided for use for the remainder of the month upon request. Permits should be returned by the close of business on the last working day of the month to avoid being charged for the following month. Purchased in Full: Customers returning an annual permit purchased in full will receive a prorated refund, excluding the current and prior months."
2. **[dist 0.402] *CampusParc — Returns, Refunds & Exchanges* (official):** "Returns, Refunds & Exchanges We want to ensure that you get the maximum use out of your permit. If for any reason you're unsatisfied with the permit you purchased or wish to explore another permit option, we're happy to accommodate. Returns and Refunds Annual permits may be returned at any time by stopping by the CampusParc Customer Care Center or by filling out the Return Request Form . See below for specific purchase-type policies."
3. **[dist 0.476] *CampusParc — Returns, Refunds & Exchanges* (official):** "Employees utilizing payroll deduction must address the cost difference for the current calendar month at the time of exchange, with deductions for the new permit becoming effective the following calendar month. Depending on the permit type, visitor permits may be eligible for refunds. Digital Day Passes and Temporary Monthly Permits: Any unused digital day passes, inclusive of Offstreet permits, or temporary monthly permits are eligible for refunds prior to the effective date of the permit and within 60 days of purchase. Refunds are no longer available once the permit goes into effect. Partial refunds are not available for partially used visitor permits. To request a return please stop by the CampusParc Customer Care Center or fill out the Return Request Form ."

Relevance explanation: All top hits come from the official Returns/Refunds page and state the actual policy (prorated refund excluding current/prior months, return-by-end-of-month timing, and the special cases for day passes and visitor permits). This is the correct, high-authority grounding for a factual policy question. Best distance 0.348.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** Generation uses Groq's `llama-3.3-70b-versatile` at `temperature=0` (see `query.py`). The retrieved chunks are inserted into the user message as numbered, source-labeled context, and the system prompt *enforces* grounding rather than suggesting it:

> You are The Unofficial Guide, an assistant that answers questions about parking at The Ohio State University. Answer the user's question using ONLY the information in the provided context documents. Follow these rules strictly:
> - Use only facts found in the context. Never use outside or prior knowledge.
> - If the context does not contain enough information to answer the question, reply with exactly: "I don't have enough information on that." and nothing else.
> - When the sources disagree, say so instead of silently picking one.
> - Note when a claim is student opinion (Reddit) versus official policy.
> Be concise and specific.

The "ONLY ... never use outside or prior knowledge" rule plus the mandated exact decline phrase is what prevents the model from answering from its training data on out-of-scope questions.

**How source attribution is surfaced in the response:** Attribution is **programmatic, not model-generated**. After retrieval, `query.py` builds the source list directly from the retrieved chunks' metadata (`source` title, `source_type`, `url`), deduplicated in first-seen order — so the citations can never be hallucinated by the LLM. The Gradio UI shows them in a separate **"Retrieved from"** box. When the model returns the decline message, the source list is deliberately emptied (it answered nothing, so it cites nothing).

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query:

Response:

Source attribution:

---

**Grounded response 2**

Query:

Response:

Source attribution:

---

**Out-of-scope query**

Query:

System response (refusal):

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:**

**Output format:**

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** 

> **System:** 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
