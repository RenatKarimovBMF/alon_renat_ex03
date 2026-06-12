# Mechanism PRD — CrewAI Orchestrator

**Component:** Crew builder + task pipeline  
**Module:** `bookgen.crew`  
**Version:** 0.10  
**Authors:** Renat Karimov, Alon Engel  
**Last updated:** 2026-06-09

---

## 1. Summary

Define the **five-agent sequential Crew** that transforms a topic into structured JSON artifacts and triggers LaTeX assembly. This is the core of Exercise 03.

---

## 2. Agents

| Key | Class name | CrewAI role |
|-----|------------|-------------|
| `research_director` | ResearchDirector | Chief Researcher |
| `outline_architect` | OutlineArchitect | Publishing Strategist |
| `chapter_writer` | ChapterWriter | Technical Author |
| `latex_editor` | LatexEditor | LaTeX Copy Editor |
| `build_engineer` | BuildEngineer | Build & Release Engineer |

Prompt text lives in `config/prompts/<key>.yaml` — not hardcoded in Python.

---

## 3. Tasks (sequential)

| Order | Task ID | Agent | Output schema | Artifact path |
|-------|---------|-------|---------------|---------------|
| 1 | `research_brief` | Research Director | `ResearchBrief` | `data/sessions/<id>/01_research.json` |
| 2 | `book_outline` | Outline Architect | `BookOutline` | `data/sessions/<id>/02_outline.json` |
| 3 | `write_sections` | Chapter Writer | `SectionDraft[]` | `data/sessions/<id>/03_sections.json` |
| 4 | `assemble_latex` | LaTeX Editor | `.tex` files + `ReviewReport` | `latex/chapters/*.tex` |
| 5 | `review_pages` | LaTeX Editor | `ReviewReport` | `data/sessions/<id>/05_review.json` |
| 6 | `compile_pdf` | Build Engineer | `BuildReport` | `latex/build/main.pdf` |

**Process:** `Process.sequential`  
**Context chaining:** each task receives prior task outputs via CrewAI `context=[...]`.

---

## 4. Chapter Writer loop

The Chapter Writer task is **one CrewAI task** whose Python callback loops over `BookOutline.chapters` and appends `SectionDraft` entries. Do not spawn extra CrewAI agents per chapter (ADR-003).

---

## 5. Validation rules

- Every agent response parsed with Pydantic before next task starts.
- On validation failure: retry same task once with error feedback; then fail session.
- Demo mode (`book.demo_mode.enabled`): cap at 2 chapters × 2 sections.

---

## 6. Tools

| Tool | Used by | Purpose |
|------|---------|---------|
| `write_session_artifact` | all | Persist JSON under session dir |
| `write_tex_file` | LaTeX Editor | Write guarded paths under `latex/` |
| `latex_compile` | Build Engineer | Run latexmk |
| `estimate_pages` | LaTeX Editor | Word-count → page heuristic |

---

## 7. Acceptance criteria

- [ ] `uv run python -m bookgen.main` runs crew in demo mode without manual steps
- [ ] Session JSONL log lists agent, task, tokens, timestamp
- [ ] All five agents visible in CrewAI verbose output
- [ ] Gatekeeper invoked before every LLM call

---

## 8. Out of scope

- Hierarchical manager agent (stretch / ADR optional)
- Real-time human approval gates

---

## 9. Implemented updates (v1.1)

- **Length contract:** the writer task demands exactly 5 paragraphs of 80–95
  words per section with a recount-before-returning step, and a total ~15%
  above target (LLMs systematically undershoot ranges — see `PROMPTS.md` §7).
- **Citations:** the task embeds the real `references.bib` keys
  (`latex/bib.py`); every key must be cited; tags like `team_analysis` are
  forbidden as citations.
- **Hebrew:** the outline task requires a 1–2 sentence `hebrew_summary` per
  chapter, rendered as the RTL block (digits kept LTR via `\beginL` islands).
- **Agent-driven media (live):** the outline agent specifies every chapter's
  web image (search query + caption) and chooses which chapter carries the
  data table, display equation, and chart data; Python fetches images from
  the public web (Wikimedia/NASA, keyless) and renders everything
  deterministically (ADR-007).
- **LLM-backed gap-fill (subject-generic):** if a spec is missing, one extra
  call to the same LLM API regenerates it (validated + budgeted); failed
  image fetches get one LLM-suggested alternative query each, then the
  configured minimum image pool, then "no image for this chapter"
  (`crew/media_gapfill.py`).
- **Dynamic topic:** `--topic` overrides the subject per run; the research
  agent supplies the bibliography (`sources[]` → generated `references.bib`,
  citations filtered), and the off-topic gate (`plan_is_topical`) blocks
  subject-bound pool fallbacks so no Moon media can leak into another topic.
- **Live isolation:** live runs execute in `examples/<topic>-<stamp>/`
  workspaces (ADR-006).
