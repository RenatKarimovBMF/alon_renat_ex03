# Prompt Engineering Log

**Project:** Exercise 03 — CrewAI LaTeX Book Generator
**Version:** 1.00
**Authors:** Renat Karimov, Alon Engel

This is the *development* prompt log required by Guidelines V3 §8.3 — the
significant prompts we gave AI coding assistants while building the project,
with context, results, and what we changed afterwards. (The agent prompts that
run *inside* the pipeline live separately in `config/prompts/*.yaml`.)

---

## 1. Architecture scaffold

**Goal:** turn the assignment into a guideline-compliant repo skeleton.

**Prompt (summary):**
> "Design a Python package for a CrewAI pipeline that writes a ~15-page LaTeX
> book. Use an SDK layer as the single entry point, a central API gatekeeper for
> all LLM calls, Pydantic models for every agent hand-off, config in JSON with a
> version key, and keep every file under 150 lines. Give me the module tree."

**Result / lesson:** the first tree mixed business logic into the CLI. We
re-prompted to force *all* logic behind `BookGenSdk`, which is what shipped.

---

## 2. JSON-only agent hand-offs

**Goal:** stop the writer agent from emitting raw LaTeX that breaks compilation.

**Prompt (summary):**
> "Each CrewAI task must return JSON validated by a Pydantic schema
> (ResearchBrief, BookOutline, SectionDraftBundle, ReviewReport, BuildReport).
> Python — not the LLM — should generate `.tex`. Show the schemas and the
> assembly function."

**Lesson:** keeping the LLM out of `.tex` generation removed almost all compile
errors. Documented as ADR-002.

---

## 3. Hebrew / BiDi and "fancy" formulas

**Goal:** satisfy the BiDi requirement and avoid plain-text math.

**Prompts (summary):**
> "Add a right-to-left Hebrew summary block per chapter using `babel` +
> `otherlanguage`, isolated so no line mixes Hebrew and English."
> "Render the Tsiolkovsky rocket equation as a proper `equation` environment
> (fancy formula), not inline text."

**Lesson:** the summary first appeared *after* a `\clearpage`, so it looked like
it belonged to the next chapter. We changed the layout to a trailing page break
**after** each chapter instead (see `latex/writer.py`).

---

## 4. Killing repeated content (the big one)

**Goal:** the fixtures generator rotated four template paragraphs until a word
target was hit, so every section repeated the same text and citations.

**Prompt (summary):**
> "Replace the word-target paragraph loop with curated, distinct prose per
> section. Each of the 12 sections gets its own paragraphs and its own citation
> keys so all bibliography entries are used and nothing repeats. Citations should
> appear once per section, not after every paragraph."

**Lesson:** distinct prose dropped the book from 22 → 16 pages and made it read
like a real book. Length is now controlled by content, not a padding loop.

---

## 5. Offline, deterministic tests

**Goal:** a unit test downloaded NASA images and failed without network.

**Prompt (summary):**
> "Make image resolution bundled-first (committed copies before any network),
> make the fetch function injectable, and add an `ensure_figures_fn` hook to the
> assembler so unit tests run fully offline. Cover HTTP providers with
> `httpx.MockTransport`."

**Lesson:** this both fixed the flaky test and lifted coverage past 85%.

---

## 6. "How This Book Was Made" appendix

**Goal:** add the TikZ block diagram the lecturer asked for and realize the
Team-Analysis section promised in PLAN §13.

**Prompt (summary):**
> "Write a LaTeX appendix that draws the agent pipeline with TikZ (vertical
> stages, gatekeeper as a side node) and compares the earlier IPC orchestration
> with the CrewAI crew. Cite the team source."

**Lesson:** vertical layout avoided page-width overflow; a horizontal six-box row
needed `\resizebox`, which we dropped in favor of the cleaner vertical diagram.

---

## 7. Making the live writer hit a hard length floor

**Goal:** the live book must fill ≥15 subject pages, but Opus undershot every
soft instruction.

**Iterations:**
> v1 "3-5 paragraphs, 320-400 words per section" → ~280 words/section (13 pages).
> v2 "360-440 words; sections under 360 are rejected" → ~339 words/section (14 pages).
> v3 "exactly 5 paragraphs of 80-95 words EACH; recount every section before
> returning and expand any under 400" → 405-443 words/section (16 pages ✓).

**Lesson:** models negotiate ranges but follow *per-paragraph contracts with a
self-check step*. Asking ~15% above the real target also offsets systematic
undershoot. (Each failed attempt cost ~$0.5-0.8 — see `COST_live.md`.)

---

## 8. Hebrew BiDi: years rendered reversed (1961 → 1691)

**Goal:** digits and Latin runs (N1, NASA) inside the RTL Hebrew summaries
printed backwards.

**Prompts (summary):**
> "Wrap digit runs in `\foreignlanguage{english}{...}`" — fixed the digits but
> scrambled the surrounding Hebrew word order (verified by rendering the page
> to PNG and reading it).
> "Use the TeX--XeT primitives instead: wrap each Latin/digit run in
> `{\beginL ... \endL}`."

**Lesson:** for babel-hebrew on pdfTeX, an LTR *island* (`\beginL/\endL`) is
the correct primitive; a language *switch* re-segments the line. Visual
verification (render → read) caught what text extraction could not.

---

## 9. Agent-created media: content and placement by the crew

**Goal:** images, the table, the equation, and the chart must be *created/chosen
by the agents and taken from the web*, not pre-baked by the team — including
where each lands in the book.

**Prompt (summary):**
> "Extend BookOutline: every chapter gets figure {image_query, caption}
> (a public-web image search); exactly one chapter of your choice gets table
> {caption, columns, rows}, one gets equation {intro, latex, explanation}
> (display-math body only), one gets chart {title, y_label, points} with real
> numeric data. You decide content AND placement."

**Engineering around it:** pydantic validators reject ragged tables, unsafe
TeX (`\input`, `\write`, …), and `$`-wrapped math so CrewAI's converter
retries; Python fetches images from Wikimedia Commons/NASA (keyless),
renders the chart with matplotlib, and keeps the configured plan as a
per-element safety net for failed fetches.

**Result / lesson:** the agent placed table→ch2, equation→ch4, chart→ch6 (the
fixtures plan used 1/3/4 — proof the placement is genuinely the agent's).
4 of 6 web images fetched on the first try; first-hit image relevance is the
remaining weak spot (a "Sputnik 1" query can return a museum fragment), which
the caption still describes correctly.

**Follow-up — LLM-backed gap-fill:** to stay subject-generic, the *fallback*
is also the LLM: a missing table/equation/chart spec triggers one extra call
("Pick the best-fitting chapter and return real, factual content as JSON:
{schema}"), and failed image queries trigger one call asking for "ONE simpler,
more generic query likely to match stock/archive photos" per failed chapter.
Both degrade gracefully (warn + proceed) so a bad reply never breaks the run.

---

## 10. Calibrating words-per-page

**Goal:** the review heuristic assumed 450 words/page, but a figure-rich book is
much sparser.

**Prompt (summary):**
> "Measure prose words vs compiled PDF pages across runs and fit pages ≈
> overhead + words/density. Put the experiment in a notebook and use the result
> to set `words_per_page` so the review estimate matches reality."

**Lesson:** the effective density is ~110 words/page here because figures, the
table, the equation, the plot, the TikZ appendix, and per-chapter page breaks
dominate. See `notebooks/words_per_page_calibration.ipynb`.
