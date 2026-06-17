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

**Ingestion process.** Reddit and Columbus.gov block automated scraping, so the raw sources were collected once in the browser (archived under `documents/raw/`) and converted to a consistent plain-text format with a small `title / url / source_type` header: Reddit threads from their `.json` (one comment per blank-line block; deleted/removed/AutoModerator comments and one-liners dropped), the CampusParc pages from their main content area, and the Columbus FAQ extracted from its PDF. The resulting files live in `documents/`. `ingest.py` then loads every file, parses its header, and cleans the body — decoding HTML entities, stripping non-breaking spaces, and removing Reddit UI noise (Reply/Share/vote counts/timestamps) — before handing the text to `chunk.py`. Run the whole pipeline with `python build_chunks.py`, which writes `chunks.jsonl` and prints the chunk count and sample chunks.

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

**Why these choices fit your documents:** The 800-char cap keeps every chunk inside the 256-token input limit of `all-MiniLM-L6-v2` (longer text is silently truncated). The corpus has two shapes, so chunking is structure-aware: Reddit threads are split one-comment-per-chunk so conflicting opinions never blend into one vector, while official pages have their short blocks (headings, list items, paragraphs) greedily packed up to the cap so a heading stays attached to the content beneath it. Preprocessing strips HTML entities, non-breaking spaces, and Reddit UI noise (Reply/Share/vote counts/timestamps) before chunking. See `ingest.py` and `chunk.py`.

**Final chunk count:** 109 chunks across 11 documents (8 Reddit threads + 3 official pages/PDF). Sizes range 20–799 characters (avg ~308); none exceed the 800-character cap.

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

**Model used:**

**Production tradeoff reflection:**

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:**

Top returned chunks:
-
-
-

Relevance explanation:

---

**Query 2:**

Top returned chunks:
-
-
-

Relevance explanation:

---

**Query 3:**

Top returned chunks:
-
-
-

Relevance explanation:

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

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
