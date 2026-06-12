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
| S4-04 | PDF screenshots + TOC in README | Alon | [x] (toc/sample-page from PDF, pipeline run) |
| S4-05 | User commit + push Stage 4 | Both | [ ] |

---

## Stage 5 — Quality gate & submission

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S5-01 | Coverage ≥85%, Ruff clean | Both | [x] (90%, ruff clean) |
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
| S6-07 | Delete stale chapter `.tex` files (only the 6 used remain) | Both | [x] |
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
| S6-19 | Capture screenshots into `assets/screenshots/` | Both | [x] |
| S6-20 | One `--live` run for a real cost table (gemini free tier, $0.00) | Both | [x] |
| S6-21 | Wire up gatekeeper retry/back-off on transient 429/5xx (was unused) | Both | [x] |

---

## Stage 7 — Hard 15-page subject rule, examples, generic subjects

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S7-01 | Subject chapters alone ≥15 pages (hard rule): expand curated prose to ~4,000 words → 16 subject / 20 total | Both | [x] |
| S7-02 | Broaden bibliography (McDougall, Chaikin, NASA image credits, CrewAI docs) and cite every source | Both | [x] |
| S7-03 | Live prompts: per-section word floor, real bib keys only, Hebrew summaries from outline | Both | [x] |
| S7-04 | Generic-subject seam: config `extras` block (figures/Hebrew/table/equation/plot), Moon defaults | Both | [x] |
| S7-05 | Isolated `examples/<topic>-<stamp>/` workspace per live run (canonical latex/ untouched) | Both | [x] |
| S7-06 | Config-driven HTTP timeout + retry on timeouts; Anthropic max_tokens configurable | Both | [x] |
| S7-07 | Anthropic pricing table + prefix matching for dated model ids | Both | [x] |
| S7-08 | Live Opus 4.8 run meeting the rule (20 sheets, 16 subject pages, $0.5019) | Both | [x] |
| S7-09 | Rotate the API keys pasted in chat (Gemini + Anthropic) | Alon | [ ] |
| S7-10 | Fix RTL BiDi: digits/Latin runs in Hebrew rendered reversed (1961→1691); wrap in `\beginL…\endL` | Both | [x] |
| S7-11 | `GatekeeperLLM.supports_function_calling` for CrewAI converter fallback | Both | [x] |
| S7-12 | Strict per-paragraph word contract in writer prompt (5×80–95) after two undershoots | Both | [x] |
| S7-13 | Delete broken example folders; keep verified Opus examples (curated-injection + agent-media) | Both | [x] |

---

## Stage 8 — Agent-created media (live runs)

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S8-01 | Media schemas with safety validators (figure/table/equation/chart) on ChapterPlan | Both | [x] |
| S8-02 | Keyless web image search (Wikimedia Commons → NASA Images) with injectable client | Both | [x] |
| S8-03 | Generic renderers: booktabs table, sanitized display equation, matplotlib chart from agent data | Both | [x] |
| S8-04 | Outline agent decides media content AND placement; per-element safety-net fallback | Both | [x] |
| S8-05 | Fix figure-cache purge deleting fetched web images (`_sync_manifest` scoped to bundled names) | Both | [x] |
| S8-06 | Live Opus run with agent media: 22 sheets, 18 subject pages, table→ch2 eq→ch4 chart→ch6, $0.6508 | Both | [x] |
| S8-07 | Keep both examples in `examples/`: agent-media run + curated-injection run | Both | [x] |
| S8-08 | LLM-backed gap-fill: missing table/equation/chart regenerated via the same LLM API; failed image queries retried with LLM-suggested alternatives, then pool, then none | Both | [x] |
| S8-09 | `--topic` CLI flag: fully dynamic per-run subject (config stays default) | Both | [x] |
| S8-10 | Agent-researched bibliography: ResearchBrief.sources → generated references.bib + citation filtering | Both | [x] |
| S8-11 | Off-topic leak gate (`plan_is_topical`): no subject-bound pool media under `--topic`; dynamic cover/header via `\BookTitle` | Both | [x] |
| S8-12 | End-to-end WW2 proof run: 20 sheets / 16 subject pages, 8 real WW2 sources all cited, $0.5690 | Both | [x] |
