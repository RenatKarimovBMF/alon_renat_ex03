# Project TODO — CrewAI LaTeX Book Generator

**Authors:** Renat Karimov, Alon Engel  
**Version:** 0.10 (planning draft)  
**Last updated:** 2026-06-09

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
| S2-01 | Pydantic models (`ResearchBrief`, `BookOutline`, …) | Alon | [ ] |
| S2-02 | Port Gatekeeper from Ex02 | Renat | [ ] |
| S2-03 | LLM SDK facade | Alon | [ ] |
| S2-04 | LaTeX writer + escaping tests | Renat | [ ] |
| S2-05 | LaTeX compiler wrapper + log parser | Alon | [ ] |

---

## Stage 3 — CrewAI crew

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S3-01 | Prompt YAML files in `config/prompts/` | Both | [ ] |
| S3-02 | Agent definitions (`crew/agents.py`) | Alon | [ ] |
| S3-03 | Task definitions + sequential Crew | Renat | [ ] |
| S3-04 | CrewAI tools (write_tex, latex_compile, …) | Both | [ ] |
| S3-05 | `--dry-run` / `--demo` CLI modes | Renat | [ ] |

---

## Stage 4 — Full pipeline & PDF

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S4-01 | End-to-end demo run (2 chapters) | Both | [ ] |
| S4-02 | Full 15-page production run | Both | [ ] |
| S4-03 | Cost log + README cost table | Renat | [ ] |
| S4-04 | PDF screenshots + TOC in README | Alon | [ ] |

---

## Stage 5 — Quality gate & submission

| ID | Task | Owner | Status |
|----|------|-------|--------|
| S5-01 | Coverage ≥85%, Ruff clean | Both | [ ] |
| S5-02 | All source files ≤150 lines | Both | [ ] |
| S5-03 | Moodle `anrbj666-ex03.pdf` | Both | [ ] |
| S5-04 | GitHub shared with `rmisegal@gmail.com` | Both | [ ] |
| S5-05 | Self-grade submitted | Both | [ ] |
