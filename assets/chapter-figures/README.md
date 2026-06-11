# Chapter figure fallbacks

NASA public-domain JPEGs used when live download fails during `ensure_figures()`.

Re-populate after URL changes:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -c "from pathlib import Path; from bookgen.latex.figures import ensure_figures; ensure_figures(Path('latex'))"
```

Files are copied to `latex/figures/` during each pipeline run.
