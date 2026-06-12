"""Read citation keys from a BibTeX file (so prompts only offer real keys)."""

from __future__ import annotations

import re
from pathlib import Path

_ENTRY = re.compile(r"@\w+\{([^,\s]+)\s*,")

# Meta sources about the pipeline itself; cited from the appendix, not prose.
META_KEYS = frozenset({"team2026", "crewai2026"})


def read_bib_keys(path: Path, *, include_meta: bool = False) -> list[str]:
    """Return the citation keys defined in ``references.bib`` (file order)."""
    if not path.exists():
        return []
    keys = _ENTRY.findall(path.read_text(encoding="utf-8"))
    if include_meta:
        return keys
    return [key for key in keys if key not in META_KEYS]
