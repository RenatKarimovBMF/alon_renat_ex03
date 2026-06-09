# CrewAI LaTeX Book Generator

**Intelligent Agents — Exercise 03** · Haifa University  
**Renat Karimov** & **Alon Engel** · Group code `anrbj666`

CrewAI multi-agent pipeline that produces a **~15-page LaTeX article** for Exercise 03.

## Status

| Stage | Description | Status |
|-------|-------------|--------|
| 0–3 | Planning, scaffold, core libs, CrewAI crew | Done |
| 4 | Full PDF pipeline, cost report, README evidence | Done |
| 5 | Quality gate + Moodle submission | Next |

## Quick start

```bash
cd crewai-latex-book-ex03
uv sync --extra dev
uv run python -m bookgen.main --dry-run
```

Use **Python 3.11–3.13** (`requires-python <3.14`).

## Run modes

| Command | Purpose | API cost |
|---------|---------|----------|
| `uv run python -m bookgen.main --demo` | 2-chapter smoke test | $0 |
| `uv run python -m bookgen.main` | **Full ~15-page book** (production fixtures) | $0 |
| `uv run python -m bookgen.main --live` | Live CrewAI crew (3 LLM tasks) | Paid |
| `uv run python -m bookgen.main --compile-only` | Recompile existing `latex/` | $0 |

### Recommended for submission PDF

```bash
uv run python -m bookgen.main
# Output: latex/build/main.pdf
```

Artifacts land in `data/sessions/<id>/` plus `docs/COST.md`.

## Book table of contents (production run)

**Topic:** *The Moon Race: USSR vs US*

1. Cold War Context and the Space Race Begins  
2. Soviet Early Lead: Sputnik and Vostok  
3. American Response: Mercury, Gemini, Apollo  
4. Key Missions and Turning Points  
5. Propaganda, Politics, and Public Opinion  
6. Legacy: Who Won and What Remains  

Each chapter has two sections with citations from `latex/references.bib`.

## API usage & cost

See [docs/COST.md](docs/COST.md) (auto-updated after each run).

| Run mode | Typical cost |
|----------|--------------|
| `--demo` | $0.00 (fixtures) |
| default production | $0.00 (fixtures, ~6750 words) |
| `--live` | Depends on model; logged per agent in `logs/crew_run_*.jsonl` |

Example live-run table format:

| Agent | Model | Calls | Input | Output | Est. USD |
|-------|-------|------:|------:|-------:|---------:|
| research_director | gpt-4o-mini | 1 | … | … | … |
| outline_architect | gpt-4o-mini | 1 | … | … | … |
| chapter_writer | gpt-4o-mini | 1 | … | … | … |

## Screenshots

Add PNGs under `assets/screenshots/` after generating the PDF:

- Table of contents (`toc.png`)
- Sample content page (`sample-page.png`)
- Terminal pipeline output (`pipeline.png`)

See [assets/screenshots/README.md](assets/screenshots/README.md).

## Repository layout

```
├── config/prompts/     # CrewAI agent YAML prompts
├── docs/               # PRD, PLAN, TODO, COST.md
├── latex/              # LaTeX sources + build/main.pdf
├── src/bookgen/        # Python package (crew, sdk, reporting)
├── data/sessions/      # JSON artifacts per run
├── logs/               # crew_run_*.jsonl
└── tests/
```

## CrewAI architecture (summary)

Five agents · sequential crew (3 LLM tasks in live mode):

`Research Director → Outline Architect → Chapter Writer → [assemble] → Review → Compile`

Gatekeeper wraps every LLM call. Prompts live in `config/prompts/`.

## Documentation

- [PRD](docs/PRD.md)
- [PLAN](docs/PLAN.md)
- [TODO](docs/TODO.md)
- [COST](docs/COST.md)

## Submission checklist

- [ ] GitHub shared with `rmisegal@gmail.com`
- [ ] `latex/` folder committed
- [ ] `docs/PRD.md`, `PLAN.md`, `TODO.md`, root `README.md`
- [ ] Moodle PDF: `anrbj666-ex03.pdf` from Word template
- [ ] Self-grade on Moodle
