# Sample run (committed evidence)

This folder is one real production run, kept in version control so graders can
see the pipeline's artifacts without running it (`.gitignore` keeps only this
`sample/` session; other runs under `data/sessions/` are ignored).

| File | Produced by |
|------|-------------|
| `01_research.json` | Research stage (`ResearchBrief`) |
| `02_outline.json` | Outline stage (`BookOutline`) |
| `03_sections.json` | Chapter Writer stage (`SectionDraftBundle`) |
| `05_review.json` | Review stage (`ReviewReport`, `approved=true`, ~15 pages) |
| `06_build.json` | Compile stage (`BuildReport`, `success=true`) |
| `COST.md` | Token/cost summary (offline fixtures run → $0) |

A `--live` run additionally writes `logs/crew_run_<id>.jsonl` with per-call token
counts; in offline fixtures mode there are no LLM calls, so the cost table is $0.
