"""Distinct, human-readable prose for each Moon Race section.

Every section has its own paragraphs and citation keys, so the assembled book
reads as continuous narrative instead of a rotating template. Citation keys are
spread across all bibliography entries so each source is actually referenced.
"""

from __future__ import annotations

# (section_title, paragraphs, citation_keys)
_SECTION_CONTENT: list[tuple[str, list[str], list[str]]] = [
    (
        "Superpower rivalry after 1945",
        [
            "After the Second World War, the United States and the Soviet Union emerged as rival superpowers whose competition shaped global politics for decades. Their contest was ideological, military, and economic, but it was also deeply symbolic: each side sought visible proof that its system could out-build and out-think the other. Space, still an untouched frontier, offered exactly that kind of stage.",
            "The rivalry hardened quickly. Berlin, Korea, and the nuclear arms race left little room for trust, and reliable intelligence on the other side was scarce and prized. In that climate, technological milestones doubled as strategic signals: a successful launch told allies and adversaries alike that a nation could deliver a warhead across continents, so the line between civilian achievement and military deterrence was deliberately blurred.",
            "Prestige, then, was never a side effect of the space race; it was a central goal. Governments invested enormous resources because being first carried weight in capitals, newspapers, and living rooms around the world. The Moon eventually became the ultimate prize precisely because it was difficult, expensive, and visible to everyone who looked up at night.",
        ],
        ["siddiqi2010", "cadbury2006"],
    ),
    (
        "Rockets, missiles, and prestige",
        [
            "The rockets that carried satellites and cosmonauts were direct descendants of wartime weapons. Germany's V-2, the first large liquid-fueled ballistic missile, proved that controlled rocket flight at the edge of space was possible, and at the war's end both superpowers raced to recruit its engineers and seize its hardware. The expertise gathered in 1945 became the seed of two parallel national programs.",
            "Through the 1950s, missile development and space ambition advanced together. The same boosters designed to deliver nuclear warheads could, with modest changes, loft scientific payloads, so investment in one capability quietly strengthened the other. This dual use meant that every rocket test was watched closely abroad, and that failures were as politically costly as they were technically instructive.",
            "Prestige tied the whole enterprise together. A reliable, powerful rocket signaled industrial maturity, scientific depth, and military credibility in a single stroke. Because these signals were read by allies, adversaries, and domestic audiences at once, governments were willing to fund ambitious programs whose payoff was measured as much in influence as in engineering.",
        ],
        ["harford1997", "logsdon2010"],
    ),
    (
        "Sputnik and the shock in America",
        [
            "On 4 October 1957 the Soviet Union launched Sputnik 1, the first artificial satellite, and its simple radio beep, audible to amateur listeners worldwide, announced that the space age had begun. The achievement was modest in mass but enormous in meaning: a Soviet object was now passing over American territory several times a day, beyond any power to stop it.",
            "In the United States the reaction was swift and anxious. Commentators spoke of a Sputnik crisis, questioning whether American science and education had fallen behind. The launch reframed space as a domain of national security and pride, and the political pressure it generated would soon reshape budgets and institutions.",
            "The most lasting response was structural. Within a year the United States created NASA to lead civilian spaceflight and expanded federal support for science and engineering education. Sputnik thus did more than orbit the Earth; it set in motion the institutional machinery that would eventually carry Americans to the Moon.",
        ],
        ["cadbury2006", "nasa2019"],
    ),
    (
        "First human in space: Yuri Gagarin",
        [
            "On 12 April 1961 Yuri Gagarin orbited the Earth aboard Vostok 1, becoming the first human in space and handing the Soviet Union another decisive first. The single orbit lasted under two hours, but its symbolic weight was immense: a human being had left the planet and returned, and a Soviet citizen had done it first.",
            "The flight was the product of careful, secretive engineering led by Sergei Korolev, whose identity the Soviet state concealed for security reasons. Vostok's automated systems, life support, and reentry capsule represented years of incremental, high-risk testing, much of it hidden from the public until success could be announced.",
            "Gagarin's flight intensified the contest. Coming only weeks before the first American suborbital flight, it underscored how far ahead the Soviet program appeared and pushed Washington to seek a goal dramatic enough to change the narrative. That goal would soon be named: the Moon.",
        ],
        ["siddiqi2010", "harford1997"],
    ),
    (
        "NASA and the crash program",
        [
            "Faced with repeated Soviet firsts, the United States organized an unprecedented peacetime mobilization of engineering talent. NASA grew rapidly, contracting with universities and thousands of companies to build launch vehicles, spacecraft, tracking networks, and test facilities almost simultaneously. The result was a crash program whose scale rivaled the largest industrial efforts in the nation's history.",
            "Project Mercury came first, proving that Americans could survive launch, orbit, and reentry. Its successes were hard-won and public, and they restored a measure of confidence even as they revealed how much remained unknown about living and working in space.",
            "Managing such a program demanded new methods. Systems engineering, rigorous testing schedules, and tight configuration control became as important as any single rocket, because coordinating so many contractors under deadline pressure was itself a formidable technical challenge.",
        ],
        ["logsdon2010", "nasa2019"],
    ),
    (
        "From Earth orbit to the lunar landing goal",
        [
            "In May 1961 President Kennedy committed the United States to landing a man on the Moon and returning him safely before the decade's end. The pledge was audacious: the country had barely fifteen minutes of human spaceflight experience, yet it now had a deadline and a destination that the whole world could understand.",
            "Choosing the Moon was a strategic decision as much as a scientific one. It was far enough ahead that the Soviet lead in early milestones would not decide the outcome, and dramatic enough that success would be unmistakable. The goal concentrated national effort on a single, measurable objective.",
            "Project Gemini bridged the gap between ambition and capability. Its flights practiced the rendezvous, docking, long-duration flight, and spacewalking that a lunar mission would require, turning Kennedy's promise into a sequence of solvable engineering problems.",
        ],
        ["logsdon2010", "cadbury2006"],
    ),
    (
        "Robotic Luna, Ranger, and Surveyor",
        [
            "Before any crew could land, both nations sent robotic scouts to study the Moon. The Soviet Luna program achieved a string of firsts, including the first impact on the lunar surface and the first images of its far side, expanding humanity's map of a world no one had yet touched.",
            "American robotic missions followed a deliberate progression. Ranger probes returned close-up images as they crashed into the surface, while the Surveyor landers demonstrated soft landing and showed that the lunar soil could bear the weight of a spacecraft, easing fears that a lander might simply sink.",
            "Together these missions reduced risk. They mapped hazards, measured surface properties, and validated the navigation and landing techniques that crews would later depend on, turning the Moon from an unknown into a surveyed destination.",
        ],
        ["siddiqi2010", "nasa2019"],
    ),
    (
        "Apollo 11 and lunar samples",
        [
            "On 20 July 1969 Apollo 11's lunar module Eagle touched down in the Sea of Tranquility, and Neil Armstrong and Buzz Aldrin became the first humans to walk on another world. Hundreds of millions watched or listened as a goal set eight years earlier was fulfilled with months to spare.",
            "The crew did more than plant a flag. They deployed scientific instruments and collected about twenty-two kilograms of rock and soil, the first material ever returned from the Moon, which scientists would study for decades to understand the Moon's age and origin.",
            "Apollo 11 marked the decisive moment of the race. The United States had achieved the most visible objective first, and while exploration continued, the central question of who would reach the Moon had been answered.",
        ],
        ["nasa2019", "logsdon2010"],
    ),
    (
        "Media and ideological messaging",
        [
            "Spaceflight was always partly a performance. Both superpowers presented their achievements as evidence that their political and economic systems were superior, and each launch was packaged for domestic audiences and the wider world as proof of progress.",
            "Their strategies differed sharply. The Soviet Union tended to announce successes only after they were secure, keeping failures hidden, while the United States increasingly broadcast its missions live, accepting the risk of public failure in exchange for the credibility of openness.",
            "The imagery endured. Photographs such as Earthrise, taken from lunar orbit, transcended propaganda and reshaped how people everywhere saw their own planet, showing that the race produced cultural touchstones as well as political points.",
        ],
        ["cadbury2006", "siddiqi2010"],
    ),
    (
        "Cost, risk, and congressional support",
        [
            "Ambition came at a steep price. At its peak the Apollo program consumed a significant share of the federal budget and employed hundreds of thousands of people, and sustaining that investment required continual political justification.",
            "Risk was equally real. The 1967 Apollo 1 fire, which killed three astronauts during a ground test, forced a sweeping reassessment of design and safety and reminded everyone that the race was conducted at the edge of what was survivable.",
            "Public and congressional support proved finite. As early goals were met and costs mounted, enthusiasm cooled, and the same political forces that had launched the program began to question how long it could continue at such expense.",
        ],
        ["logsdon2010", "harford1997"],
    ),
    (
        "End of Apollo and later cooperation",
        [
            "After Apollo 11, the United States flew several more lunar missions before ending the program in 1972, as budgets tightened and priorities shifted. The Soviet crewed lunar effort, hampered by the failures of its giant N1 rocket and the death of Korolev, never reached the Moon at all.",
            "Competition gradually gave way to contact. In 1975 the Apollo-Soyuz Test Project docked American and Soviet spacecraft in orbit, a symbolic handshake that signaled the race's most intense phase was over.",
            "That thaw set a precedent. The cooperation rehearsed in the 1970s would later mature into joint programs, culminating in the International Space Station, where former rivals share a single laboratory in orbit.",
        ],
        ["nasa2019", "cadbury2006"],
    ),
    (
        "Lessons for science and exploration",
        [
            "The Moon race left a deep scientific legacy. The returned samples, instruments, and data transformed lunar science, while the technologies developed for spaceflight found uses far beyond it, from materials and computing to global communications.",
            "It also offered organizational lessons. Achieving the landing required disciplined systems engineering, relentless testing, and clear goals shared across enormous teams, a model later studied by engineers and managers in many fields.",
            "Perhaps the most durable lesson is about motivation and its limits. A single dramatic goal can mobilize extraordinary effort, but sustaining exploration over the long term depends on broader purposes, an insight that still informs how nations plan their journeys beyond Earth.",
        ],
        ["siddiqi2010", "logsdon2010"],
    ),
]

_PARAGRAPHS: dict[str, list[str]] = {title: paras for title, paras, _ in _SECTION_CONTENT}
_CITATIONS: dict[str, list[str]] = {title: cites for title, _, cites in _SECTION_CONTENT}


def section_paragraphs(chapter_title: str, section_title: str) -> list[str]:
    """Return distinct paragraphs for a section, with a safe generic fallback."""
    paragraphs = _PARAGRAPHS.get(section_title)
    if paragraphs:
        return list(paragraphs)
    return [
        f"This section of {chapter_title} examines {section_title.lower()} and its "
        "place in the wider Moon Race narrative.",
    ]


def section_citations(section_title: str) -> list[str]:
    """Return the bibliography keys assigned to a section."""
    return list(_CITATIONS.get(section_title, ["siddiqi2010"]))
