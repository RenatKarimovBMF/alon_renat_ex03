# Product Requirements Document — CrewAI LaTeX Book Generator

**Project:** Exercise 03 — Intelligent Agents (Haifa University)  
**Course instructor:** Dr. Yoram Segal  
**Version:** 1.00  
**Authors:** Renat Karimov, Alon Engel  
**Group code:** `anrbj666`  
**Last updated:** 2026-06-12

---

## 1. Overview

Build a **CrewAI multi-agent publishing pipeline** in Python that collaboratively produces a **~15-page LaTeX document** (article or short book), compiles it to PDF, and ships a professional GitHub repository that satisfies **Software Submission Guidelines V3**.

**Default deliverable topic:**  
*The Moon Race: USSR vs US*

The team chose this topic for the ~15-page LaTeX book produced by the CrewAI publishing crew.

| Layer | Technology | Role |
|-------|------------|------|
| Agent orchestration | **CrewAI** | Role-based crew (research → outline → write → review → compile) |
| Document output | **LaTeX** | Structured `.tex` sources + BibTeX |
| Runtime | Python 3.11+ / **uv** | SDK entry, gatekeeper, tests, CLI |
| Graded artifact | **PDF (~15 pages)** | Primary grading focus per `ex03.txt` |

---

## 2. Goals

1. Satisfy Exercise 03 requirements: CrewAI + LaTeX, ~15 pages, modular agent design, GitHub with `PRD` / `PLAN` / `TODO` / `README`, plus the LaTeX project folder.
2. Meet Guidelines V3: SDK layer, Gatekeeper, TDD, ≥85% coverage, Ruff clean, ≤150 lines/file, cost logging, version keys in config.
3. Demonstrate **agent instruction design** — each role has explicit goals, constraints, output schema, and handoff rules.
4. Produce a PDF that reads like a coherent academic/technical article, not a dump of raw LLM text.

### 2.1 Success criteria (acceptance)

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC-01 | Final PDF is **13–17 pages** (target 15) | `pdfinfo` / page count in README |
| AC-02 | PDF built from committed LaTeX under `latex/` | `uv run python -m bookgen.main --compile-only` |
| AC-03 | CrewAI crew runs end-to-end without manual copy-paste between agents | CLI log + `logs/crew_run_<id>.jsonl` |
| AC-04 | GitHub contains `docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md`, root `README.md` | Repo inspection |
| AC-05 | All LLM calls pass through **Gatekeeper** | Unit tests + runtime logs |
| AC-06 | **Cost breakdown** documented (tokens in/out, model, estimated USD) | `docs/COST.md` or README § |
| AC-07 | Moodle submission: `anrbj666-ex03.pdf` from Word template | Manual |

---

## 3. User stories

| ID | As a… | I want… | So that… |
|----|-------|---------|----------|
| US-01 | Grader | Open the PDF first and see a structured 15-page article | The main deliverable is clear |
| US-02 | Grader | Read PRD / PLAN / TODO before code | I can assess agent architecture design |
| US-03 | Grader | See distinct CrewAI roles with explicit instructions | Modular agent design is evident |
| US-04 | Student | Run one CLI command to generate the book | The pipeline is reproducible |
| US-05 | Student | Re-run only failed stages (e.g. re-compile) | Development is efficient |
| US-06 | Student | Cap API spend via gatekeeper + demo config | I stay within budget |
| US-07 | Grader | Inspect LaTeX sources in `latex/` | Output is not a black-box PDF |
| US-08 | Grader | See agent handoffs (outline → sections → review) | Crew workflow is auditable |
| US-09 | Student | Use a cheap demo mode (shorter outline, 2 sections) | I can test without full 15-page run |
| US-10 | Grader | See original interpretation beyond slide summaries | Excellence criteria are met |

---

## 4. Functional requirements

### 4.1 CrewAI crew

- **FR-01:** Exactly **one Crew** with **five primary agents** (see `PLAN.md` §5): Research Director, Outline Architect, Chapter Writer, LaTeX Editor, Build Engineer.
- **FR-02:** Tasks execute in a **defined order** with explicit `context` dependencies (CrewAI sequential/hierarchical process — default: **sequential** for auditability).
- **FR-03:** Each agent output must conform to a **Pydantic schema** (JSON), not free-form prose, before the next task consumes it.
- **FR-04:** Chapter Writer may spawn **section sub-tasks** internally (loop over outline sections) without adding undeclared agents.
- **FR-05:** LaTeX Editor validates: no markdown leakage, required `\section{}` structure, BibTeX keys resolved, estimated page budget per chapter.

### 4.2 LaTeX / PDF pipeline

- **FR-06:** LaTeX project lives in `latex/` with at minimum: `main.tex`, `preamble.tex`, `chapters/*.tex`, `references.bib`, `figures/` (optional).
- **FR-07:** Build Engineer (agent + tool) writes/updates `.tex` files deterministically from approved JSON payloads.
- **FR-08:** Compilation uses `latexmk` or `pdflatex` + `bibtex` via a sandboxed tool; logs saved to `logs/latex/`.
- **FR-09:** Target length enforced: **~4,000–5,500 words** or **~15 pages** at 11pt A4 (configurable in `config/book.json`).

### 4.3 SDK, Gatekeeper, observability

- **FR-10:** All external LLM access goes through `sdk.llm_client` → `shared.gatekeeper.ApiGatekeeper`.
- **FR-11:** Structured logs: `logs/crew_run_<session>.jsonl`, token counts per agent/task.
- **FR-12:** Version key `"version": "1.00"` in `config/setup.json`, `config/rate_limits.json`, and `config/book.json`.

### 4.4 CLI

- **FR-13:** Entry point: `python -m bookgen.main` (via `uv run`).
- **FR-14:** Flags: `--topic`, `--config`, `--demo`, `--compile-only`, `--dry-run`, `--session-id`.
- **FR-15:** `--dry-run` validates configs and schemas without LLM calls.

---

## 5. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | Source files ≤ **150 lines** (excluding docstrings blank lines per Guidelines) |
| NFR-02 | Test coverage ≥ **85%** on `src/` |
| NFR-03 | `ruff check` passes with project config |
| NFR-04 | Windows primary dev; portable to Linux/macOS |
| NFR-05 | No secrets in Git; `.env-example` only |
| NFR-06 | Reproducible install: `uv sync` + `uv run` |

---

## 6. Out of scope (v1.0)

- GUI (CLI only unless time permits)
- Real-time human-in-the-loop approval gates (optional stretch)
- Multi-language PDF (English primary; Hebrew abstract optional stretch)
- Autonomous web browsing without citation metadata

---

## 7. Mechanism PRDs (child documents)

| Document | Scope |
|----------|--------|
| `docs/PRD_crew_orchestrator.md` | CrewAI agents, tasks, schemas, process type |
| `docs/PRD_latex_pipeline.md` | `.tex` layout, compilation tool, page budget |
| `docs/PRD_gatekeeper.md` | Rate limits, queue, retry (reuse Ex02 pattern) |
| `docs/PRD_llm_sdk.md` | Provider facade (Claude / Gemini / OpenAI) |

---

## 8. Risks & mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| PDF ≠ 15 pages | Grade hit | Page budget in config; Reviewer agent checks word/page estimate |
| LaTeX compile errors | No PDF | Build Engineer + automated compile loop with error feedback |
| Agent outputs invalid JSON | Pipeline stall | Pydantic validation + retry task (max 2) |
| API cost overrun | Budget | Gatekeeper + `--demo` profile |
| Generic slide summary content | Low originality | Research Director must cite course PDFs + add team analysis section |

---

## 9. Definition of done (project)

- [ ] PDF submitted on Moodle as `anrbj666-ex03.pdf`
- [ ] GitHub public or shared with `rmisegal@gmail.com`
- [ ] `latex/` + compiled PDF artifact (or build instructions) in repo
- [ ] PRD / PLAN / TODO complete and consistent with code
- [ ] Tests green, coverage ≥85%, Ruff clean
- [ ] README: install, usage, screenshots of PDF TOC, cost table, self-grade
