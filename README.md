# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

The domain for this project is parking at the Ohio State University. Parking at OSU is run by a private company called CampusParc, and it seems to be focused more on profits than student convenience. Information is scattered throughout the company's site, which makes it hard to take advantage of perks such as off-peak parking and refunds for unused semesters. In addition, there are alternative options such as street parking and city permits, but they do not show up readily in search results. This agent corroborates between official and unofficial sources to dig out the best solutions to OSU's parking problems.

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

**Final chunk count:** 108 chunks across all documents.

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

Query: *Can I get a refund if I cancel or return my parking permit?*

Response: "According to the official CampusParc documents, refunds are available under certain conditions. - For annual permits purchased in full, a prorated refund is available, excluding the current and prior months. - For digital day passes, temporary monthly permits, and single-exit garage validations, refunds are available if returned within specific time frames (e.g., prior to the effective date or within 60 days of purchase). - However, refunds for current or prior months are not available for other permit types. It's recommended to review the specific refund policies for your permit type and to contact the CampusParc Customer Care Center or fill out the Return Request Form to initiate the return process."

Source attribution: CampusParc — Returns, Refunds & Exchanges (official) — https://osu.campusparc.com/get-a-permit/returns-refunds-exchanges/

---

**Grounded response 2**

Query: *I want to work out at Jesse Owens South in the evenings. What are the cheapest parking options?*

Response: "According to the context documents, there are a few options to consider for cheap parking near Jesse Owens South. One option is to park on King Avenue, which has 'big stretches of free street parking' about half a mile from Jesse Owens, according to a student on Reddit [1]. However, please note that this is a student's opinion and may not reflect official policy. Another option is to use metered parking spaces, which have a progressive pricing rate structure... as stated in the official City of Columbus — University District Parking FAQ [4]. It's also worth considering parking on west campus, as one student mentions that 'there is always parking available on west campus' [5], although this may be farther from Jesse Owens South."

Source attribution: South Campus Parking (reddit); Public Parking Help (reddit); City of Columbus — University District Parking FAQ (official); Parking help please!!!!! (reddit)

---

**Out-of-scope query**

Query: *What are the best dining halls at Ohio State?*

System response (refusal): "I don't have enough information on that." (no sources listed — the corpus is parking-only, so the system declined rather than answering from general knowledge.)

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:** A single **"Your question"** text box, an **Ask** button, and Enter-to-submit. Built with Gradio (`app.py`), launched via `python app.py` at http://localhost:7860.

**Output format:** Two read-only boxes — an **"Answer"** box (the grounded response) and a **"Retrieved from"** box listing the deduplicated source documents (title, type, and URL) the chunks came from. When the system declines, the "Retrieved from" box shows "(no sources — not enough information in the documents)".

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** Can I get a refund if I cancel or return my parking permit?

> **System (Answer):** According to the official CampusParc documents, refunds are available under certain conditions. For annual permits purchased in full, a prorated refund is available, excluding the current and prior months. For digital day passes, temporary monthly permits, and single-exit garage validations, refunds are available if returned within specific time frames. However, refunds for current or prior months are not available. It's recommended to contact the CampusParc Customer Care Center or fill out the Return Request Form to initiate the return.

> **System (Retrieved from):** • CampusParc — Returns, Refunds & Exchanges (official) — https://osu.campusparc.com/get-a-permit/returns-refunds-exchanges/

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Cheapest parking for Jesse Owens South in the evenings? | Off-peak permit (#9) plus cheap/free south-campus street spots near JOS (#3) | Cited free street parking on King Ave ~½ mile from JOS (Reddit), metered progressive pricing (City FAQ), and west-campus availability; flagged Reddit as opinion. Would have been a plus if it surfaced off-peak parking. | Relevant | Accurate |
| 2 | Best options for summer parking on north campus? | Partial — summer relaxed rules (#9) + general tips (#8); flagged as a likely failure case | "I don't have enough information on that." (declined, no sources) | Off-target | Inaccurate (failure case) |
| 3 | Can I appeal a citation if I misread a parking sign? | Appeal is possible, but "I misread the sign" is usually not accepted; acknowledge both (#7) | Said there's no official policy in context; per students, appealing is "worth a shot" and some won by admitting a mistake. Cited the appeal thread. | Relevant | Partially accurate |
| 4 | General tips to save money on parking at OSU? | Synthesis: off-peak (#9), city/UD permits (#6/#11), street parking (#5), south-campus spots (#3) | Suggested a list of three tips, including permit and street passes. Mentioned that the user should be "prepared to walk some miles to find parking" as one of the tips with no context. | Partially relevant | Partially accurate |
| 5 | Can I get a refund if I cancel/return my permit? | Per #10: prorated refund excluding current/prior months, with conditions | Accurately summarized refund policy (prorated for paid-in-full; day passes/temp within 60 days; no current/prior-month refunds; use Return Request Form). Cited the official refunds page. | Relevant | Accurate |

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

**Question that failed:** "What are the best options for summer parking on north campus?" (Q2) — a question scoped to a specific season *and* a specific part of campus.

**What the system returned:** "I don't have enough information on that." — a full refusal, with no sources listed.

**Root cause (tied to a specific pipeline stage): a corpus-coverage gap that retrieval then could not paper over.** No document in the corpus addresses "summer parking on north campus" specifically. The summer-related content that does exist is off-topic for this query. The off-peak page (#9) only mentions a summer permit-purchase clause, and the "summer tips" thread (#8) is about someone starting a job, not north-campus parking. Because nothing matches all three constraints (summer + north campus + parking options), the embedding model fell back on general term overlap ("parking," "campus") and the top 5 chunks were all generic neighborhood/south-campus/west-campus discussion (best distance 0.239) — none mentioning summer at all. The scattered summer chunks (#8, #9) never even reached the top 5. With no summer-north-campus facts in the retrieved context, the grounding prompt correctly forced a refusal rather than letting the model invent an answer. So the failure isn't hallucination or a bad embedding — it's that the question asks for something the documents don't cover, and low retrieval distances (0.239) masked that gap because the topic (parking) matched even though the specifics (summer, north campus) did not.

**What you would change to fix it:** (1) Close the coverage gap directly — collect a summer-parking / north-campus source so the facts actually exist; (2) add a **relevance gate** that checks whether retrieved chunks contain the query's key terms (e.g., "summer"), not just a low average distance, before trusting them; (3) surface partial coverage to the user ("I found general parking info but nothing specific to summer on north campus") instead of a flat refusal; (4) at minimum, log when the best distance is low but no chunk contains a key query term — that mismatch is the signature of this failure.

*(A second, different failure — Q4 "general tips to save money on parking" — also refused, but for a distinct reason: **retrieval ranking**. The query matched Reddit thread titles/original posts that literally say "parking tips," so the top chunks were question posts rather than the answer comments that hold the actual tips, leaving the model nothing concrete to cite.)*

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing the Chunking Strategy and Retrieval Approach sections *before* coding meant the implementation was a direct translation of decisions I'd already justified, not guesses made mid-code. The spec tied the 800-character chunk cap to the 256-token input limit of `all-MiniLM-L6-v2`, so when I built the chunker I had a concrete, defensible number instead of an arbitrary one. Similarly, the "store `source_type` in metadata" idea from the Anticipated Challenges section directly shaped how I built source attribution — I knew before writing `query.py` that citations had to come from chunk metadata, not the LLM.

**One way your implementation diverged from the spec, and why:** The spec said official pages would be split "by section/heading/paragraph," but when I inspected the real chunk output that produced useless heading-only fragments like "Off-Peak Hours are defined as:" with the hours stranded in a separate chunk. So I added **greedy packing** — combining small adjacent blocks up to the cap so a heading stays attached to its content. A related divergence: a Reddit post split into a tiny "title + 'Hey guys,'" fragment because the poster left a blank line after the greeting, so I added a rule to merge a short leading block into the next. Neither refinement was in the original spec; both came from looking at actual output during Milestones 3–4. The corpus also shrank from the planned 12 sources to 11 (two Columbus pages were replaced by one University District FAQ PDF), settling at 108 chunks.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1 — implementing the chunking pipeline from my spec**

- *What I gave the AI:* My planning.md Chunking Strategy section (800-char cap, 150-char overlap, structure-aware, "keep each Reddit comment as its own chunk") and asked it to implement the loader and chunker.
- *What it produced:* `ingest.py` (load + clean) and `chunking.py` (block splitting with the size cap and overlap).
- *What I changed or overrode:* The first version split official pages strictly on blank lines, which produced fragment chunks like "Off-Peak Hours are defined as:" divorced from the actual hours. I directed it to combine small official blocks up to the cap instead. Later, reviewing retrieval results, I caught a Reddit post that had been split into a near-empty "Worth it to Appeal Parking Citation? Hey guys," chunk and directed that "Hey guys," be combined with the next block so the original post stays whole.

**Instance 2 — wiring up generation + the Gradio interface**

- *What I gave the AI:* My grounding requirement (answer only from retrieved context, cite sources, decline when uncovered) and the instruction to use Gradio (the recommended interface), plus the existing retrieval function.
- *What it produced:* `query.py` (Groq `llama-3.3-70b-versatile` call with a strict grounding system prompt and programmatic source attribution) and `app.py` (Gradio UI).
- *What I changed or overrode:* Installing Gradio broke the environment two ways, and I directed the fixes: (1) Gradio forced `huggingface-hub` to 1.x, which conflicted with `transformers`. I had it upgrade `transformers`/`sentence-transformers` to compatible versions instead of downgrading Gradio below the required version; (2) importing Gradio failed because my `chunk.py` shadowed Python's standard-library `chunk` module (Gradio's `pydub` dependency does `from chunk import Chunk`), so I had it rename the module to `chunking.py`.
