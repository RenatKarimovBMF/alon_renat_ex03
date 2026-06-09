![The Moon Race: USSR vs US](assets/moon-race-hero.png)

# CrewAI LaTeX Book Generator

**Intelligent Agents — Exercise 03** · Haifa University  
**Renat Karimov** & **Alon Engel** · Group code `anrbj666`

CrewAI multi-agent pipeline that produces a **~15-page LaTeX book** for Exercise 03.

**Book topic:** *The Moon Race: USSR vs US* — from Sputnik and Gagarin through Apollo 11 to the legacy of superpower competition in space.

---

## What this project does

1. **CrewAI agents** (research → outline → chapters → review → build) produce structured JSON artifacts.
2. Python **assembles LaTeX** chapter files deterministically (no hallucinated `.tex`).
3. **MiKTeX / TeX Live** compiles `latex/build/main.pdf` (~15 pages).

The default run uses **offline production fixtures** ($0, no API keys). Use `--live` when you want the crew to write a custom topic via LLM.

---

## Status

| Stage | Description | Status |
|-------|-------------|--------|
| 0–4 | Planning, scaffold, CrewAI crew, full PDF pipeline | Done |
| 5 | Quality gate + Moodle submission | Next |

---

## Prerequisites

| Tool | Purpose |
|------|---------|
| **Python 3.11–3.13** | CrewAI does not support 3.14 |
| **MiKTeX or TeX Live** | Compile LaTeX to PDF |
| **`.venv`** (already in repo) | Project dependencies |
| **API keys** (optional) | Only for `--live` mode |

---

## Quick start (Windows PowerShell)

```powershell
cd "C:\Users\Ренат\Desktop\Haifa Un\6 is Final\Ai\crewai-latex-book-ex03"

# MiKTeX on PATH for this session (needed to compile PDF)
$env:Path = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;" + $env:Path

# Validate config
.\.venv\Scripts\python.exe -m bookgen.main --dry-run

# Generate the full Moon Race book + compile PDF
.\.venv\Scripts\python.exe -m bookgen.main

# Open result
start latex\build\main.pdf
```

If you use [uv](https://github.com/astral-sh/uv):

```bash
uv sync --extra dev
uv run python -m bookgen.main
```

---

## Run modes

| Command | Purpose | API cost |
|---------|---------|----------|
| `.\.venv\Scripts\python.exe -m bookgen.main --demo` | 2-chapter smoke test | $0 |
| `.\.venv\Scripts\python.exe -m bookgen.main` | **Full ~15-page Moon Race book** | $0 |
| `.\.venv\Scripts\python.exe -m bookgen.main --live` | Live CrewAI crew (3 LLM tasks) | Paid |
| `.\.venv\Scripts\python.exe -m bookgen.main --compile-only` | Recompile existing `latex/` | $0 |

**Output PDF:** `latex/build/main.pdf`  
**Session artifacts:** `data/sessions/<id>/` · **Cost log:** `docs/COST.md`

### LaTeX compile notes

- First compile may take several minutes while MiKTeX downloads packages.
- If `latexmk` asks for **Perl**, install the `perl` package in MiKTeX Console, or compile manually with `pdflatex` + `bibtex`.

---

## Table of contents (production run)

1. Cold War Context and the Space Race Begins  
2. Soviet Early Lead: Sputnik and Vostok  
3. American Response: Mercury, Gemini, Apollo  
4. Key Missions and Turning Points  
5. Propaganda, Politics, and Public Opinion  
6. Legacy: Who Won and What Remains  

Each chapter has two sections with citations from `latex/references.bib`.

---

## API usage & cost

See [docs/COST.md](docs/COST.md) (auto-updated after each run).

| Run mode | Typical cost |
|----------|--------------|
| `--demo` | $0.00 |
| default production | $0.00 (~6750 words, Moon Race fixtures) |
| `--live` | Depends on model; logged in `logs/crew_run_*.jsonl` |

---

## Screenshots

Add PNGs under `assets/screenshots/` for submission evidence:

- Table of contents (`toc.png`)
- Sample content page (`sample-page.png`)
- Terminal pipeline output (`pipeline.png`)

See [assets/screenshots/README.md](assets/screenshots/README.md).

---

## Repository layout

```
crewai-latex-book-ex03/
├── assets/             # Hero image + README screenshots
├── config/prompts/     # CrewAI agent YAML prompts
├── docs/               # PRD, PLAN, TODO, COST.md
├── latex/              # LaTeX sources + build/main.pdf
├── src/bookgen/        # Python package (crew, sdk, reporting)
├── data/sessions/      # JSON artifacts per run (gitignored)
├── logs/               # crew_run_*.jsonl (gitignored)
└── tests/
```

Git repository root is **`crewai-latex-book-ex03/`** (not `docs/`).

---

## CrewAI architecture

Five agents · sequential crew (3 LLM tasks in live mode):

`Research Director → Outline Architect → Chapter Writer → [assemble] → Review → Compile`

Gatekeeper wraps every LLM call. Prompts live in `config/prompts/`.

---

## Documentation

- [PRD](docs/PRD.md)
- [PLAN](docs/PLAN.md)
- [TODO](docs/TODO.md)
- [COST](docs/COST.md)

---

## Submission checklist

- [ ] GitHub shared with `rmisegal@gmail.com`
- [ ] `latex/` folder committed
- [ ] `docs/PRD.md`, `PLAN.md`, `TODO.md`, root `README.md`
- [ ] Moodle PDF: `anrbj666-ex03.pdf` from Word template
- [ ] Self-grade on Moodle
