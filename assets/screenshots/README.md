# Screenshots (submission evidence)

Embedded in the root `README.md`:

1. `toc.png` — table-of-contents page of `latex/build/book.pdf`
2. `sample-page.png` — chapter page: prose, linked citations, a table, RTL Hebrew summary
3. `pipeline.png` — terminal output of `uv run python -m bookgen.main` (offline production run)

`toc.png`/`sample-page.png` are rendered from the compiled `book.pdf`; `pipeline.png`
is captured from a real run. Optional for `--live` runs: `crew-log.png` — a snippet of
`logs/crew_run_*.jsonl`.
