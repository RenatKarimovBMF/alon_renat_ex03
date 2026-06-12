# Mechanism PRD — LaTeX Pipeline

**Component:** LaTeX writer + compiler  
**Module:** `bookgen.latex`  
**Version:** 0.10  
**Authors:** Renat Karimov, Alon Engel  
**Last updated:** 2026-06-09

---

## 1. Summary

Convert validated JSON drafts into a compilable LaTeX project and produce the **~15-page PDF** — the primary graded deliverable.

---

## 2. Directory layout

```
latex/
├── main.tex
├── preamble.tex
├── metadata.tex
├── chapters/chNN_<slug>.tex
├── references.bib
├── figures/          (optional)
└── build/            (gitignored output)
```

---

## 3. Writer responsibilities (`bookgen.latex.writer`)

- Escape TeX special characters: `% $ # _ { } ~ ^ \`
- Emit `\section{}` / `\subsection{}` only (article class)
- Preserve `\cite{key}` markers from `SectionDraft.citations`
- Update `\input{...}` list in `main.tex` deterministically
- Never write outside `latex/` root (path guard)

---

## 4. Compiler responsibilities (`bookgen.latex.compiler`)

- Command: `latexmk -pdf -interaction=nonstopmode -output-directory=latex/build latex/main.tex`
- Max attempts: `book.latex.max_compile_attempts` (default 3)
- Parse `.log` for: undefined citations, missing refs, Unicode errors
- Return `BuildReport(success, pdf_path, attempts, errors[])`

---

## 5. Page budget

| Setting | Default |
|---------|---------|
| `target_pages` | 15 (**subject** pages — hard floor) |
| `page_tolerance` | ±2 |
| `words_per_page` | 280 (measured; see `notebooks/words_per_page_calibration.ipynb`) |

LaTeX Editor `ReviewReport.estimated_pages` must be within tolerance before compile task runs.

---

## 6. Acceptance criteria

- [x] `latex/build/book.pdf` exists after successful run
- [x] Subject chapters alone fill ≥15 pages (appendix start via pypdf − front matter); total ≈19–21
- [x] `references.bib` keys match all `\cite{}` commands (0 unresolved `[?]`)
- [x] Latin/digit runs inside RTL Hebrew render LTR (`\beginL…\endL` islands in `latex/hebrew.py`)
- [x] `--compile-only` flag compiles existing sources without LLM calls
- [x] `--live` compiles into an isolated `examples/<topic>-<stamp>/` workspace (canonical tree untouched)

---

## 7. Failure handling

| Error | Action |
|-------|--------|
| Missing `.bib` key | LaTeX Editor adds stub or removes cite |
| Unicode in body | Replace with LaTeX escapes |
| Overfull hbox only | Warning OK; do not fail |
| Missing `\begin{document}` | Fail fast — writer bug |

---

## 8. Submission requirement

The full `latex/` folder must be committed to GitHub (sources + `references.bib`). PDF in `build/` may be gitignored but must be reproducible via compile step documented in README.
