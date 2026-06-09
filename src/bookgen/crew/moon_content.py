"""Chapter plan and prose templates for the Moon Race production book."""

from __future__ import annotations

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

CITATIONS = ["siddiqi2010", "logsdon2010", "nasa2019", "harford1997", "cadbury2006"]

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


def paragraph_templates(chapter_title: str, section_title: str) -> list[str]:
    """Return rotating Moon Race paragraphs for a section."""
    return [
        (
            f"In {chapter_title}, {section_title} shows how the superpowers turned "
            "ballistic missile research into a public contest for orbital and lunar "
            "firsts. Leaders on both sides treated each launch as proof of industrial "
            "capacity, scientific maturity, and ideological confidence."
        ),
        (
            f"The section {section_title} highlights engineers such as Sergei Korolev "
            "and Wernher von Braun, whose teams adapted military rockets for exploration. "
            "Reliability, telemetry, and life-support constraints turned each mission "
            "into a chain of irreversible decisions under extreme time pressure."
        ),
        (
            f"For {section_title}, historians compare Soviet secrecy with NASA's televised "
            "milestones. Public audiences learned mission jargon, followed countdowns, and "
            "debated whether moonshots justified their cost while terrestrial crises continued."
        ),
        (
            f"Additional detail on {section_title}: archives now reveal how failures "
            "were hidden, retried, or reframed. The Moon Race was never a smooth arc; "
            "it was a sequence of gambles where a single explosion could shift budgets "
            "and national narratives overnight."
        ),
    ]
