# Project TODO — CrewAI LaTeX Book Generator

**Authors:** Renat Karimov, Alon Engel  
**Version:** 1.00  
**Last updated:** 2026-06-12

Status key: `[ ]` pending · `[~]` in progress · `[x]` done · `[-]` cancelled

---

## Stage 0 — Planning (current)

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S0-01 | Draft `docs/PRD.md` | Renat | [x] |
| S0-02 | Draft `docs/PLAN.md` (CrewAI architecture) | Renat | [x] |
| S0-03 | Draft `docs/TODO.md` | Renat | [x] |
| S0-04 | Confirm topic with Lecture 06 / team | Both | [ ] |
| S0-05 | Write `docs/PRD_crew_orchestrator.md` | Alon | [ ] |
| S0-06 | Write `docs/PRD_latex_pipeline.md` | Renat | [ ] |
| S0-07 | Write `docs/PRD_gatekeeper.md` (port from Ex02) | Alon | [ ] |
| S0-08 | Write `docs/PRD_llm_sdk.md` | Alon | [ ] |
| S0-09 | Team review + commit Stage 0 | Both | [ ] |

---

## Stage 1 — Repository scaffold

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S1-01 | `pyproject.toml` + `uv sync` + crewai dependency | Renat | [ ] |
| S1-02 | `config/setup.json`, `rate_limits.json`, `book.json` | Alon | [ ] |
| S1-03 | `latex/` skeleton (`main.tex`, `preamble.tex`, bib) | Renat | [ ] |
| S1-04 | Root `README.md` stub | Alon | [ ] |
| S1-05 | `.env-example`, `.gitignore` | Renat | [ ] |

---

## Stage 2 — Core libraries

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S2-01 | Pydantic models (`ResearchBrief`, `BookOutline`, …) | Alon | [x] |
| S2-02 | Port Gatekeeper from Ex02 | Renat | [x] |
| S2-03 | LLM SDK facade | Alon | [x] |
| S2-04 | LaTeX writer + escaping tests | Renat | [x] |
| S2-05 | LaTeX compiler wrapper + log parser | Alon | [x] |
| S2-06 | User commit + push Stage 2 | Both | [ ] |

---

## Stage 3 — CrewAI crew

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S3-01 | Prompt YAML files in `config/prompts/` | Both | [x] |
| S3-02 | Agent definitions (`crew/agents.py`) | Alon | [x] |
| S3-03 | Task definitions + sequential Crew | Renat | [x] |
| S3-04 | CrewAI tools (write_tex, latex_compile, …) | Both | [x] |
| S3-05 | `--demo` pipeline + live crew kickoff path | Renat | [x] |
| S3-06 | User commit + push Stage 3 | Both | [ ] |

---

## Stage 4 — Full pipeline & PDF

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S4-01 | End-to-end demo run (2 chapters) | Both | [x] |
| S4-02 | Full 15-page production run | Both | [x] |
| S4-03 | Cost log + README cost table | Renat | [x] |
| S4-04 | PDF screenshots + TOC in README | Alon | [ ] (capture real PNGs into `assets/screenshots/`) |
| S4-05 | User commit + push Stage 4 | Both | [ ] |

---

## Stage 5 — Quality gate & submission

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S5-01 | Coverage ≥85%, Ruff clean | Both | [x] (~88%, ruff clean) |
| S5-02 | All source files ≤150 lines | Both | [x] |
| S5-03 | Moodle `anrbj666-ex03.pdf` | Both | [ ] |
| S5-04 | GitHub shared with `rmisegal@gmail.com` | Both | [ ] |
| S5-05 | Self-grade submitted | Both | [ ] |

---

## Stage 6 — Review feedback fixes

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S6-01 | Cover: instructor → Dr. Yoram Segal | Both | [x] |
| S6-02 | Fix Hebrew typos; per-chapter summaries | Both | [x] |
| S6-03 | Distinct per-section prose (no repetition); cite once/section | Both | [x] |
| S6-04 | Diversify citations so all bib entries are used | Both | [x] |
| S6-05 | Chapter-summary page-break layout | Both | [x] |
| S6-06 | TikZ "How This Book Was Made" appendix + Team Analysis | Both | [x] |
| S6-07 | Delete 17 stale chapter `.tex` files | Both | [x] |
| S6-08 | Ruff ruleset (W,N,C4,SIM, ignore E501) + 0 violations | Both | [x] |
| S6-09 | `shared/version.py` + startup version validation; bump to 1.00 | Both | [x] |
| S6-10 | Split `compiler.py` and `moon_content.py` (≤150 lines) | Both | [x] |
| S6-11 | Offline/injectable figures; HTTP providers via MockTransport | Both | [x] |
| S6-12 | Coverage 85%+ (cheap unit tests) | Both | [x] |
| S6-13 | README: uv, mermaid (incl. OOP), generic paths, screenshots | Both | [x] |
| S6-14 | `docs/PROMPTS.md` prompt-engineering log | Both | [x] |
| S6-15 | Gatekeeper rate-limit wait from config + ADR-005 | Both | [x] |
| S6-16 | Topic-aware research prompt + context tool | Both | [x] |
| S6-17 | Words-per-page calibration notebook | Both | [x] |
| S6-18 | Commit run evidence (sample session, COST, PDF) | Both | [x] |
| S6-19 | Capture screenshots into `assets/screenshots/` | Both | [ ] |
| S6-20 | One `--live` run for a real cost table (optional, needs API key) | Both | [ ] |
