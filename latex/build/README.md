# Compiled book PDF

After you run the pipeline, the **only** book PDF is:

```
latex/build/book.pdf
```

There is no `main.pdf` in this project. If you see `main.pdf` elsewhere (for example under `latex/`), it is a stale manual compile — delete it and open `book.pdf` here instead.

Generate or refresh:

```powershell
$env:PYTHONPATH = "src"
$env:MPLBACKEND = "Agg"
.\.venv\Scripts\python.exe -m bookgen.main --compile-only
```

**Submit to GitHub:** this file (`book.pdf`) is tracked in git so graders can open it without running the pipeline.
