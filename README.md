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

**Domain:** NYC college student survival knowledge — practical, peer-sourced information about
navigating New York City as a student (transit, housing, food, money, health, safety, academics,
and international student resources).

**Why this knowledge is valuable and hard to find through official channels:**
Official university websites cover tuition, enrollment, and campus maps. They do not tell you
that a $1.50 pizza slice near campus keeps you full for $3, that the L train is brutal during
rush hour, that your security deposit must be returned within 14 days under NYC law, or that
NYC Well offers free 24/7 mental health support. This information lives in Reddit threads, student
blogs, and word-of-mouth. This RAG system aggregates it in one queryable place.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/nyc, r/AskNYC, MTA rider guides | Reddit + MTA       | data/nyc_subway_guide.txt                |
| 2 | r/FoodNYC, r/NYCbargains, Yelp student reviews | Reddit + Yelp | data/nyc_cheap_eats.txt          |
| 3 | r/NYCapartments, r/AskNYC, NYU/Columbia housing forums | Reddit | data/nyc_housing_guide.txt      |
| 4 | r/personalfinance, r/povertyfinance, Columbia/NYU finance blogs | Reddit | data/nyc_student_budget.txt |
| 5 | r/nyc, TimeOut New York, r/AskNYC | Reddit + TimeOut   | data/nyc_free_activities.txt            |
| 6 | NYU Student Health guides, Columbia Health, r/AskNYC | University sites | data/nyc_health_wellness.txt |
| 7 | r/nyc, NYPD community safety, NYU campus safety | Reddit + NYPD | data/nyc_safety_navigation.txt     |
| 8 | r/college, r/GradSchool, CUNY/NYU/Fordham student blogs | Reddit + blogs | data/nyc_academic_campus_life.txt |
| 9 | r/nyc, r/bikecommuting, MTA bus guides | Reddit + MTA     | data/nyc_transportation_guide.txt       |
| 10 | r/f1visa, r/internationalstudents, NAFSA, NYU ISSO | Reddit + NAFSA | data/nyc_international_students.txt   |



---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 800 characters

**Overlap:** 150 characters

**Why these choices fit the documents:**
Our documents are medium-length informational guides (4,000–7,000 characters each)
written in multi-sentence paragraphs rather than single-fact bullet lists. An
800-character window (~120–140 words) captures a complete idea — typically one full
paragraph or a cohesive list of related facts — without pulling in irrelevant material
from the next topic. Initial testing with 300-character chunks showed frequent
mid-sentence splits that produced decontextualized fragments and hurt retrieval quality.

A 150-character overlap (~25 words) ensures that content at a chunk boundary appears
fully in at least one neighboring chunk. This is especially important for list-structured
content like neighborhood rent tables and multi-step visa rules, where a shorter overlap
would split individual entries across chunks and make retrieval miss the full context.

**Preprocessing:** Documents are plain `.txt` files with no HTML or navigation text to
strip. Each file was `.strip()`-ed on load to remove leading/trailing whitespace.

**Final chunk count:** ~85–90 chunks across 10 documents (varies slightly with
whitespace normalization). Run `python build_database.py` to see the exact count.

**Sample chunks** (excerpts — each actual chunk is ~800 characters; these show representative content from within chunks):

**Chunk A** — `nyc_subway_guide.txt`
> "As of 2024, the MTA is transitioning from MetroCards to OMNY (the tap-to-pay system). OMNY accepts contactless credit/debit cards and Apple Pay/Google Pay. You get a free transfer within 2 hours of your first tap."

**Chunk B** — `nyc_subway_guide.txt`
> "Students should note: the reduced fare MetroCard gives half-price rides to eligible students. You must apply through your school. The current reduced fare is $1.45 per ride (half of the $2.90 base fare as of 2024)."

**Chunk C** — `nyc_housing_guide.txt`
> "Your security deposit must be returned within 14 days of move-out with itemized deductions, or the landlord may owe you the full amount. NYC has strong tenant protections — free legal advice is available through NYC's housing courts."

**Chunk D** — `nyc_international_students.txt`
> "On-campus work: you may work up to 20 hours/week on campus while school is in session; no limit during official school breaks. Off-campus work: generally not allowed without specific authorization (CPT for internships, OPT after graduation)."

**Chunk E** — `nyc_health_wellness.txt`
> "NYC Well (nyc.gov/nycwell): free 24/7 mental health helpline, text, and chat; can connect you with ongoing free or low-cost therapy in NYC. Open Path Collective: therapy sessions at $30–80/session for students and low-income individuals."


---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `sentence-transformers/all-MiniLM-L6-v2`

**Why chosen:** Runs completely locally with no API key or cost. Produces 384-dimensional
semantic embeddings. Well-suited to English informational text. Small footprint (~80 MB)
with fast inference — ideal for a student project.

**Production tradeoff reflection:**
For a real production deployment, I would weigh several factors when choosing a different model:

- **Context length:** all-MiniLM-L6-v2 has a 256-token max input, which means long chunks get
  silently truncated. A production system serving diverse documents would benefit from a model
  with a 512+ token window (e.g., `all-mpnet-base-v2` or `text-embedding-3-small` from OpenAI).
- **Accuracy on domain-specific text:** General-purpose models may underperform on technical
  or domain-specific vocabulary. A domain-adapted model fine-tuned on legal, medical, or
  multilingual text would improve retrieval quality for specialized corpora.
- **Multilingual support:** If serving international students who query in their first language,
  a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` or OpenAI's `text-embedding-3-large`
  would be essential.
- **Latency and hosting:** Local models (sentence-transformers) have zero network latency after
  the initial load but add ~200-500ms per batch on CPU. API-hosted models (OpenAI, Cohere)
  reduce local compute requirements but add network round-trip and per-token cost.
- **Cost:** At scale, API embedding costs accumulate. For a corpus of 10,000+ documents,
  a one-time local embedding with a high-quality model beats recurring API costs.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

```
You are a helpful assistant for The Unofficial NYC Student Guide.
Answer ONLY using the information in the CONTEXT sections provided below.
Do NOT use any outside knowledge, even if you know the answer.
If the answer is not contained in the context, respond with EXACTLY:
  "I don't have enough information in the documents to answer that."
Always cite the source filenames at the end of your answer using this format:
  Sources: [filename1.txt, filename2.txt]
```

**How grounding is enforced in the pipeline:**

1. **System prompt instruction:** The LLM is explicitly told to use ONLY the provided context
   and to refuse gracefully if the answer isn't there.
2. **Context injection:** Retrieved chunks are formatted as labeled `[Context N — Source: filename]`
   blocks in the user message. The model receives no other factual content.
3. **Low temperature (0.2):** Reduces creative deviation and keeps the model closer to what
   the context actually says.
4. **Mandatory refusal phrase:** The exact refusal phrase is specified in the prompt, making
   it easy to detect programmatically if needed.

**How source attribution is surfaced:**

The system prompt requires the model to append `Sources: [filename1.txt, ...]` at the end of
every answer. The Streamlit UI also displays the source filenames in a separate caption below
each answer, populated from the retrieved chunk metadata (independent of the LLM's own citation).
Users can expand the "View retrieved chunks" section to see exactly which passages were used.

**Example response with source attribution:**

*Query:* "What is OMNY and how does the weekly bonus cap work?"

*Response:*
> OMNY is the MTA's tap-to-pay system that is replacing the MetroCard. It accepts
> contactless credit/debit cards and mobile payment services like Apple Pay and
> Google Pay. A free transfer is included within 2 hours of your first tap.
>
> The weekly bonus cap works as follows: if you take 12 rides in a 7-day period,
> rides 13 through the end of that week are free. This replaces the old 7-day
> unlimited MetroCard.
>
> Sources: [nyc_subway_guide.txt]

**Example response with source attribution (two sources):**

*Query:* "What free mental health resources are available to students in NYC?"

*Response:*
> Several free mental health resources are available to NYC students:
> - **Campus counseling centers**: free, confidential therapy for enrolled students
> - **NYC Well**: free 24/7 mental health helpline (call, text, or chat) at nyc.gov/nycwell
> - **Crisis Text Line**: text HOME to 741741 for free 24/7 crisis counseling
> - **Open Path Collective**: sessions at $30–80 for students and low-income individuals
> - **Therapy Aid Coalition**: free and reduced-cost sessions for those in financial need
>
> Sources: [nyc_health_wellness.txt, nyc_student_budget.txt]

**Example out-of-scope query (refusal):**

*Query:* "Is the moon made of cheese?"

*Response:*
> I don't have enough information in the documents to answer that.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How do I get a reduced-fare MetroCard and how much does it cost? | Apply through your school; costs $1.45/ride (half of $2.90) | Correctly stated students must apply through school; cost is $1.45/ride | Relevant | Accurate |
| 2 | What is OMNY and how does the weekly bonus cap work? | OMNY is tap-to-pay; rides 13+ in a 7-day window are free after 12 paid rides | Correctly explained OMNY as the MetroCard replacement and described the 12-ride cap | Relevant | Accurate |
| 3 | What free or low-cost mental health resources are available to NYC students? | Campus counseling, NYC Well, Crisis Text Line (741741), Open Path Collective | Listed all major resources with correct contact info | Relevant | Accurate |
| 4 | What are tenant rights for security deposits in NYC? | Must be returned within 14 days with itemized deductions | Correctly stated 14-day return rule; mentioned landlord owes full amount if violated | Relevant | Accurate |
| 5 | How many hours/week can an F-1 international student work on campus? | 20 hours/week during semester; no limit during school breaks | Correctly answered 20 hours/week with no-limit caveat for breaks | Relevant | Accurate |

**Retrieval quality:** Relevant 
**Response accuracy:** Accurate 

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed (partially):**
"What grocery stores should I shop at to save money?"

**What the system returned:**
The system retrieved chunks from `nyc_cheap_eats.txt` and correctly mentioned Trader Joe's and Key Food, but omitted the Costco recommendation and the greenmarket details because the relevant content was split across a chunk boundary — one chunk ended with "For bulk staples: Costco" and the next began with "(requires membership, but splitting with roommates...)", so the retrieval step returned the second chunk without the first in its top-4 results.

**Root cause (tied to a specific pipeline stage):**
**Chunking stage.** An 800-character chunk ended mid-list at the phrase "For bulk staples: Costco" and the next chunk started with the continuation about membership splitting. When the query was semantically matched, the second chunk ranked lower in similarity to "grocery stores to save money" than other chunks, so it fell outside the top-5 retrieved. The LLM received only the tail of the list — missing the Costco entry entirely.

**What I would change to fix it:**
Implement sentence-boundary-aware chunking using spaCy's sentence tokenizer so that list items are never split mid-entry. Alternatively, increase k from 5 to 7 to retrieve more chunks and reduce the chance of a relevant chunk falling outside the window. A third option is to increase overlap from 150 to 200 characters for documents that contain dense lists.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped during implementation:**
Defining the grounding prompt in the spec before writing `generate.py` meant the critical
system prompt instruction was locked in before touching any code. This prevented me from
accidentally writing a generic chat assistant prompt and having to reverse-engineer grounding
later. The spec's requirement to "show the actual instruction" pushed me to write the complete
system prompt in `planning.md` first, which I then copy-pasted directly into `generate.py`.

**One way the implementation diverged from the spec, and why:**
The spec called for a chunk size of 300 characters with 50-character overlap. During
implementation, testing showed that 300-character chunks frequently cut paragraphs mid-sentence,
producing decontextualized fragments that retrieved poorly. The final implementation uses
800-character chunks with 150-character overlap after observing that this better matched the
natural paragraph boundaries in the source documents and produced more coherent retrieval results.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1: Generating boilerplate for `embed.py`**

- *What I gave the AI:* The Embedding Model section from `planning.md`, the ChromaDB documentation
  for PersistentClient, and the sentence-transformers `.encode()` API signature. I asked Claude
  to implement `embed_and_store()` using batched insertion.
- *What it produced:* A working function that encoded all chunks in one `model.encode(texts)` call
  and inserted them in a single `collection.add()` call.
- *What I changed or overrode:* I changed the implementation to process in batches (added the
  `batch_size` parameter and the `for batch_start in range(0, total, batch_size)` loop) because
  the initial version would fail on machines with limited RAM when processing large corpora.
  I also added the `{"hnsw:space": "cosine"}` metadata to the collection creation call, which
  the AI had omitted, because without it ChromaDB defaults to L2 distance and the similarity
  scores in `retrieve.py` would be incorrect.

**Instance 2: Writing the grounding system prompt**

- *What I gave the AI:* The Grounded Generation requirements from the assignment spec and the
  requirement that the refusal phrase be exact and detectable programmatically.
- *What it produced:* A system prompt that instructed the model to use context and cite sources,
  but used vague phrasing ("try to answer only from context").
- *What I changed or overrode:* I revised the instruction to be categorical ("Answer ONLY using...")
  and added the exact refusal phrase as a quoted string in the prompt so the model would reproduce
  it verbatim. I also added the explicit temperature=0.2 setting to `generate.py` after observing
  that the default temperature produced more hallucinated "guesses" when the context was sparse.


---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- A free Groq API key from https://console.groq.com

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd unofficial-guide

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set GROQ_API_KEY=your_key_here

# 5. Build the vector database (first time only)
python build_database.py

# 6. Start the Streamlit interface
streamlit run app.py
# Open http://localhost:8501 in your browser
```
