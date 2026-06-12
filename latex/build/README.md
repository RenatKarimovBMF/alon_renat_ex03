# Compiled book PDF

After you run the pipeline, the **only** book PDF is:

```
latex/build/book.pdf
```

There is no `main.pdf` in this project. If you see `main.pdf` elsewhere (for example under `latex/`), it is a stale manual compile — delete it and open `book.pdf` here instead.

Generate or refresh (everything runs through `uv`):

```powershell
uv run python -m bookgen.main --compile-only   # recompile existing .tex
uv run python -m bookgen.main                  # full offline production run
```

Live runs (`--live`) compile into their own `examples/<topic>-<stamp>/latex/build/`
instead, so this canonical PDF is never overwritten by an LLM run.

**Submit to GitHub:** this file (`book.pdf`) is tracked in git so graders can open it without running the pipeline.
