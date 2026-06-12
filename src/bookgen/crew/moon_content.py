"""Chapter plan and research data for the Moon Race production book.

Figures, Hebrew summaries, and section prose live in dedicated modules
(``moon_figures``, ``moon_prose``) and are re-exported here so existing
imports keep working while every content file stays under the 150-line limit.
"""

from __future__ import annotations

from bookgen.crew.moon_figures import CHAPTER_FIGURES, HEBREW_SUMMARIES
from bookgen.crew.moon_prose import section_citations, section_paragraphs

CHAPTERS: list[tuple[str, list[str]]] = [
    (
        "Cold War Context and the Space Race Begins",
        ["Superpower rivalry after 1945", "Rockets, missiles, and prestige"],
    ),
    (
        "Soviet Early Lead: Sputnik and Vostok",
        ["Sputnik and the shock in America", "First human in space: Yuri Gagarin"],
    ),
    (
        "American Response: Mercury, Gemini, Apollo",
        ["NASA and the crash program", "From Earth orbit to the lunar landing goal"],
    ),
    (
        "Key Missions and Turning Points",
        ["Robotic Luna, Ranger, and Surveyor", "Apollo 11 and lunar samples"],
    ),
    (
        "Propaganda, Politics, and Public Opinion",
        ["Media and ideological messaging", "Cost, risk, and congressional support"],
    ),
    (
        "Legacy: Who Won and What Remains",
        ["End of Apollo and later cooperation", "Lessons for science and exploration"],
    ),
]

# All bibliography keys cited from chapter prose (appendix adds team2026 and
# crewai2026); used for fallbacks and validation that each source is cited.
CITATIONS = [
    "siddiqi2010",
    "logsdon2010",
    "nasa2019",
    "harford1997",
    "cadbury2006",
    "mcdougall1985",
    "chaikin1994",
    "nasaimages",
]

FINDINGS: list[tuple[str, str, str]] = [
    (
        "The Moon Race grew out of Cold War military rocketry",
        "Intercontinental missiles made orbital flight technically feasible",
        "external",
    ),
    (
        "The USSR scored the first satellite and first human orbit",
        "Sputnik and Gagarin demonstrated early Soviet momentum",
        "external",
    ),
    (
        "Kennedy's 1961 pledge reframed US goals toward the Moon",
        "Apollo became a concentrated national engineering project",
        "external",
    ),
    (
        "Robotic precursors reduced risk before crewed landings",
        "Luna, Ranger, and Surveyor mapped hazards and surfaces",
        "external",
    ),
    (
        "Apollo 11 fulfilled the US lunar landing before a Soviet equivalent",
        "Armstrong and Aldrin walked the Moon in July 1969",
        "external",
    ),
    (
        "Both sides used space achievements for propaganda",
        "Success was sold as proof of system superiority",
        "external",
    ),
    (
        "Crash programs demanded unprecedented coordination and budget",
        "Thousands of contractors and civil servants worked under deadlines",
        "team_analysis",
    ),
    (
        "The race ended in cooperation as much as competition",
        "Apollo-Soyuz and later ISS linked former rivals",
        "external",
    ),
]

THESIS = (
    "The Moon Race was a Cold War contest of engineering, propaganda, and national will "
    "in which the Soviet Union led early milestones while the United States achieved "
    "the decisive lunar landing."
)

OPEN_QUESTIONS = [
    "Could the USSR have landed cosmonauts if funding priorities had differed?",
    "How much of Apollo's success depended on political deadline pressure?",
]

__all__ = [
    "CHAPTERS",
    "CHAPTER_FIGURES",
    "CITATIONS",
    "FINDINGS",
    "HEBREW_SUMMARIES",
    "OPEN_QUESTIONS",
    "THESIS",
    "section_citations",
    "section_paragraphs",
]
