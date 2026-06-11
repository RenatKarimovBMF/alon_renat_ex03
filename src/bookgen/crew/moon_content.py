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

# NASA image URLs (public domain). Each chapter tries URLs in order, then assets/chapter-figures/.
# Captions are verified against NASA metadata (images-api.nasa.gov).
CHAPTER_FIGURES: list[tuple[str, list[str], str]] = [
    (
        "ch01_cold_war.jpg",
        [
            "https://images-assets.nasa.gov/image/6900846/6900846~orig.jpg",
            "https://images-assets.nasa.gov/image/624109main_1969-05-20-2_full/624109main_1969-05-20-2_full~orig.jpg",
            "https://images-assets.nasa.gov/image/6900560/6900560~orig.jpg",
        ],
        "Apollo 11 Saturn V on Launch Pad 39A before the Moon landing mission.",
    ),
    (
        "ch02_sputnik.jpg",
        [
            "https://images-assets.nasa.gov/image/9248168/9248168~orig.jpg",
        ],
        "Sputnik era — the Soviet Union launched the first artificial satellite in 1957.",
    ),
    (
        "ch03_apollo.jpg",
        [
            "https://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~orig.jpg",
        ],
        "Buzz Aldrin on the Moon during Apollo 11.",
    ),
    (
        "ch04_lunar_surface.jpg",
        [
            "https://images-assets.nasa.gov/image/as11-40-5927/as11-40-5927~orig.jpg",
            "https://images-assets.nasa.gov/image/as11-44-6551/as11-44-6551~orig.jpg",
        ],
        "Apollo 11 Lunar Module Eagle on the Moon surface.",
    ),
    (
        "ch05_earthrise.jpg",
        [
            "https://images-assets.nasa.gov/image/as08-14-2383/as08-14-2383~orig.jpg",
        ],
        "Earthrise from Apollo 8 — icon of public opinion and the space race.",
    ),
    (
        "ch06_iss.jpg",
        [
            "https://images-assets.nasa.gov/image/s75-29432/s75-29432~orig.jpg",
            "https://images-assets.nasa.gov/image/ast-05-263/ast-05-263~orig.jpg",
        ],
        "Apollo–Soyuz handshake in space — beginning of post-race cooperation.",
    ),
]

# Hebrew summaries — each chapter ends in its own RTL block (no mixed lines).
HEBREW_SUMMARIES: list[str] = [
    (
        "פרק זה מציג את רקע המלחמה הקרה ואת תחילת מרוץ החלל. "
        "שני העל-יוצקים הפכו טילים בליסטיים להישגים שמיועדים לתעמולה ולפרסטיז'."
    ),
    (
        "פרק זה עוסק ביתרון הסובייטי המוקדם עם השקת לוויין ראשון "
        "והטסת האדם הראשון לחלל. הישגים אלו הזעזעו את ארצות הברית והאיצו את תגובתה."
    ),
    (
        "פרק זה מתאר את תוכניות החלל האמריקאיות לכיבוש מסלול סביב כדור הארץ "
        "ולנחיתה על הירח. ארצות הברית ריכזה משאבים לאומיים כדי להגיע ליעד לפני היריבה."
    ),
    (
        "פרק זה סוקר משימות מפתח: גשושיות, מיפוי ונחיתה ראשונה של בני אדם על הירח. "
        "משימות אלו הפחיתו סיכון והביאו לדגימות מהירח."
    ),
    (
        "פרק זה בוחן תעמולה, פוליטיקה ודעת קהל. "
        "שני הצדדים הציגו הצלחות חלל כהוכחה לעליונות מערכתית."
    ),
    (
        "פרק זה מסכם את המורשת: סיום תוכניות הנחיתה ושיתוף פעולה בינלאומי. "
        "המרוץ הסתיים בייצור ידע ובשיתוף מדעי לאחר שנים של תחרות."
    ),
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
