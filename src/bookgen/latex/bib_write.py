"""Generate references.bib from agent-researched sources (live runs).

The research agent supplies real published sources; this module renders them
as BibTeX entries (values sanitized against TeX injection) and appends the two
meta entries the static appendix cites. Citations that reference unknown keys
are filtered out so the compiled book never contains a broken ``\\cite``.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from bookgen.models import SectionDraftBundle, SourceRef

logger = logging.getLogger("bookgen.latex.bib")

_UNSAFE = re.compile(r"[{}\\%~#&$^_]")

# Cited from the static appendix (How This Book Was Made); always present.
_META_ENTRIES = """@article{team2026,
  title  = {CrewAI Publishing Pipeline for Exercise 03},
  author = {Karimov, Renat and Engel, Alon},
  year   = {2026},
  note   = {Team analysis of agent-generated book production}
}

@misc{crewai2026,
  title  = {CrewAI Documentation: Agents, Tasks, Crews, and Processes},
  author = {{CrewAI Inc.}},
  year   = {2026},
  howpublished = {docs.crewai.com}
}
"""

META_KEYS = frozenset({"team2026", "crewai2026"})


def _clean(value: str) -> str:
    return _UNSAFE.sub("", value).strip()


def _entry(source: SourceRef) -> str:
    publisher = f"  publisher = {{{_clean(source.publisher)}}},\n" if source.publisher else ""
    return (
        f"@book{{{source.key},\n"
        f"  title  = {{{_clean(source.title)}}},\n"
        f"  author = {{{_clean(source.author)}}},\n"
        f"{publisher}"
        f"  year   = {{{source.year}}}\n"
        f"}}\n"
    )


def write_bibliography(sources: list[SourceRef], path: Path) -> set[str]:
    """Write references.bib from agent sources; return the valid citation keys."""
    unique: dict[str, SourceRef] = {source.key: source for source in sources}
    body = "\n".join(_entry(source) for source in unique.values())
    path.write_text(f"{body}\n{_META_ENTRIES}", encoding="utf-8")
    return set(unique) | META_KEYS


def filter_citations(bundle: SectionDraftBundle, valid_keys: set[str]) -> int:
    """Drop citation keys that are not in the bibliography; return drop count."""
    dropped = 0
    for section in bundle.sections:
        kept = [key for key in section.citations if key in valid_keys]
        dropped += len(section.citations) - len(kept)
        section.citations = kept
    if dropped:
        logger.warning(
            "dropped unknown citation keys",
            extra={"extra_data": {"count": dropped}},
        )
    return dropped
