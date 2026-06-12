"""Curated prose for chapters 4-6 of the Moon Race book (sections 7-12).

Split from ``moon_prose`` so each content module stays under the 150-line cap.
"""

from __future__ import annotations

# (section_title, paragraphs, citation_keys)
SECTIONS_LATE: list[tuple[str, list[str], list[str]]] = [
    (
        "Robotic Luna, Ranger, and Surveyor",
        [
            "Before any crew could land, both nations sent robotic scouts to study the Moon. The Soviet Luna program achieved a string of firsts, including the first impact on the lunar surface and the first images of its far side, expanding humanity's map of a world no one had yet touched.",
            "American robotic missions followed a deliberate progression. Ranger probes returned close-up images as they crashed into the surface, while the Surveyor landers demonstrated soft landing and showed that the lunar soil could bear the weight of a spacecraft, easing fears that a lander might simply sink.",
            "The robotic race had its own rhythm of failure and recovery. Early Rangers missed the Moon entirely or returned no pictures, and Luna probes fell silent in transit, yet each loss taught navigation, communication, and reliability lessons that the next attempt absorbed. By the mid-1960s both programs could hit a target a quarter of a million miles away with growing confidence.",
            "Lunar Orbiter spacecraft then photographed the Moon systematically from orbit, producing the maps from which Apollo's landing sites were chosen. The candidate plains had to be smooth enough for a lander, well lit at the planned arrival time, and reachable with the fuel available, and only orbital photography could certify all three.",
            "The Soviet robotic line continued even after the crewed race was lost. Luna 16 returned a soil sample by automated drill in 1970, and the Lunokhod rovers drove kilometers across the surface under remote control, achievements the Soviet press presented as proof that machines could do cheaply what Apollo did with risk. The argument was self-serving, but the engineering behind it was real.",
            "Together these missions reduced risk. They mapped hazards, measured surface properties, and validated the navigation and landing techniques that crews would later depend on, turning the Moon from an unknown into a surveyed destination.",
        ],
        ["siddiqi2010", "nasa2019"],
    ),
    (
        "Apollo 11 and lunar samples",
        [
            "On 20 July 1969 Apollo 11's lunar module Eagle touched down in the Sea of Tranquility, and Neil Armstrong and Buzz Aldrin became the first humans to walk on another world. Hundreds of millions watched or listened as a goal set eight years earlier was fulfilled with months to spare.",
            "The landing itself was a test of nerve as much as engineering. Program alarms from an overloaded guidance computer interrupted the descent, and Armstrong took semi-manual control to fly past a boulder field, setting down with roughly thirty seconds of fuel margin. The calm voice loop between Houston and the crew became one of the defining recordings of the century.",
            "The crew did more than plant a flag. They deployed scientific instruments and collected about twenty-two kilograms of rock and soil, the first material ever returned from the Moon, which scientists would study for decades to understand the Moon's age and origin.",
            "The samples rewrote lunar science. Laboratory analysis dated the basalts at more than three billion years old, revealed a chemistry consistent with a violent shared origin with Earth, and turned speculative questions about the Moon's birth into measurable ones. Five further landings would extend the collection to hundreds of kilograms from six distinct sites.",
            "Getting there had taken a machine of unprecedented scale. The Saturn V stood taller than the Statue of Liberty, burned thirteen tons of propellant every second at liftoff, and flew thirteen times without a single launch failure, a reliability record that still astonishes engineers. Its development consumed years of test stands, failures, and redesigns that the public mostly never saw.",
            "The flight was also a triumph of navigation and computing. The onboard guidance computer, built from early integrated circuits and woven core-rope memory, held less storage than a modern greeting card yet steered three men across a quarter of a million miles and back. Its priority-scheduling software, which kept the landing alive through those program alarms, became a foundational case study in real-time computing.",
            "Apollo 11 marked the decisive moment of the race. The United States had achieved the most visible objective first, and while exploration continued, the central question of who would reach the Moon had been answered.",
        ],
        ["nasa2019", "chaikin1994", "logsdon2010"],
    ),
    (
        "Media and ideological messaging",
        [
            "Spaceflight was always partly a performance. Both superpowers presented their achievements as evidence that their political and economic systems were superior, and each launch was packaged for domestic audiences and the wider world as proof of progress.",
            "Their strategies differed sharply. The Soviet Union tended to announce successes only after they were secure, keeping failures hidden, while the United States increasingly broadcast its missions live, accepting the risk of public failure in exchange for the credibility of openness.",
            "Television transformed the contest in the American case. The Apollo 11 moonwalk reached an estimated six hundred million viewers, the largest live audience in history to that point, and the decision to carry a camera to the surface, once contested inside NASA as dead weight, proved to be among the program's most consequential choices.",
            "Archives such as the NASA Image and Video Library preserve this visual legacy and show how deliberately it was constructed: mission photography was planned shot by shot, astronauts trained with cameras, and the resulting pictures were cleared and distributed as instruments of national storytelling.",
            "Propaganda also traveled in person. Exhibitions of spacecraft toured world fairs, cosmonauts and astronauts were dispatched on goodwill tours through newly independent states, and both powers courted the same audiences with model rockets and film reels. In the competition for the loyalties of the decolonizing world, a capsule on a pedestal was diplomacy by other means.",
            "The imagery endured. Photographs such as Earthrise, taken from lunar orbit, transcended propaganda and reshaped how people everywhere saw their own planet, showing that the race produced cultural touchstones as well as political points.",
        ],
        ["cadbury2006", "mcdougall1985", "nasaimages"],
    ),
    (
        "Cost, risk, and congressional support",
        [
            "Ambition came at a steep price. At its peak the Apollo program consumed a significant share of the federal budget and employed hundreds of thousands of people, and sustaining that investment required continual political justification.",
            "Risk was equally real. The 1967 Apollo 1 fire, which killed three astronauts during a ground test, forced a sweeping reassessment of design and safety and reminded everyone that the race was conducted at the edge of what was survivable.",
            "The Soviet program paid its own price in the same years. Korolev died during surgery in 1966, his successor inherited an underfunded lunar rocket, and cosmonaut Vladimir Komarov was killed in 1967 when Soyuz 1's parachute failed. Both nations learned that deadline pressure and new machines were a lethal combination.",
            "Congressional support was never automatic. NASA's budget peaked in 1966 and declined every year afterward, even before the first landing, as legislators weighed the program against war spending and domestic priorities. The political coalition that funded Apollo proved as carefully engineered, and as perishable, as the hardware itself.",
            "Critics asked openly whether the Moon was worth the money. Civil rights leaders marched at Cape Kennedy on the eve of Apollo 11 to contrast rockets with poverty, and senators demanded to know what the program returned beyond prestige. Defenders answered with jobs, technology, and the Cold War scoreboard, but the debate itself showed that national consensus behind Apollo was narrower than the television audiences suggested.",
            "Public and congressional support proved finite. As early goals were met and costs mounted, enthusiasm cooled, and the same political forces that had launched the program began to question how long it could continue at such expense.",
        ],
        ["logsdon2010", "harford1997", "mcdougall1985"],
    ),
    (
        "End of Apollo and later cooperation",
        [
            "After Apollo 11, the United States flew several more lunar missions before ending the program in 1972, as budgets tightened and priorities shifted. The Soviet crewed lunar effort, hampered by the failures of its giant N1 rocket and the death of Korolev, never reached the Moon at all.",
            "The N1 told the Soviet half of the ending. Four launches between 1969 and 1972 ended in four failures, including an explosion that destroyed its pad, and the program was cancelled in secrecy so complete that Moscow denied for years that a crewed lunar effort had existed. The cover story held until the archives opened decades later.",
            "Competition gradually gave way to contact. In 1975 the Apollo-Soyuz Test Project docked American and Soviet spacecraft in orbit, a symbolic handshake that signaled the race's most intense phase was over.",
            "The handshake required real engineering diplomacy. The two nations designed a shared docking adapter, reconciled incompatible atmospheres and procedures, and trained crews in each other's languages and simulators. The techniques of working together, negotiated by the same establishments that had raced each other, outlasted the mission.",
            "Both programs redirected their remaining hardware toward orbital stations. The Soviet Union flew the Salyut series and learned long-duration spaceflight the hard way, while the United States converted a Saturn stage into Skylab and kept three crews aloft for months. The race's leftover machines, built to reach the Moon, ended up teaching both nations how to live in orbit instead.",
            "The last three planned Apollo missions were cancelled with their Saturn rockets already built, and the giant vehicles became museum pieces in Houston, Huntsville, and Florida. Ending the program while the hardware still worked struck many engineers as a waste; to the budget committees it was simply what victory looked like once the race had been won.",
            "That thaw set a precedent. The cooperation rehearsed in the 1970s would later mature into joint programs, culminating in the International Space Station, where former rivals share a single laboratory in orbit.",
        ],
        ["nasa2019", "siddiqi2010", "cadbury2006"],
    ),
    (
        "Lessons for science and exploration",
        [
            "The Moon race left a deep scientific legacy. The returned samples, instruments, and data transformed lunar science, while the technologies developed for spaceflight found uses far beyond it, from materials and computing to global communications.",
            "It also offered organizational lessons. Achieving the landing required disciplined systems engineering, relentless testing, and clear goals shared across enormous teams, a model later studied by engineers and managers in many fields.",
            "Historians draw a further lesson about evidence and memory. Because the race was fought in public, its photographs, telemetry, and documents form one of the best-preserved records of any modern engineering effort, and open archives now let researchers test the era's official stories against what the participants actually recorded.",
            "The race also set the template for how nations signal ambition in technology. Later contests over computing, genomics, and artificial intelligence borrowed Apollo's grammar of moonshots, deadlines, and flagship demonstrations, evidence that the deepest legacy of the 1960s was a way of organizing national effort, not any single machine.",
            "Some of the era's instruments are still running. Retroreflectors left on the surface return laser pulses that measure the Moon's slow retreat from Earth, the sample archive continues to yield discoveries with instruments that did not exist in 1969, and engineering data from Apollo informed every lander that followed. Few crash programs can claim working hardware and open questions half a century on.",
            "Who won, then, depends on the clock. Stop it in 1961 and the Soviet Union leads on every first that mattered; stop it in 1969 and the American flag stands on the Sea of Tranquility; let it run to the present and the clearest victors are the scientific archive and the habit of cooperation that the race, against its own intentions, eventually produced.",
            "Perhaps the most durable lesson is about motivation and its limits. A single dramatic goal can mobilize extraordinary effort, but sustaining exploration over the long term depends on broader purposes, an insight that still informs how nations plan their journeys beyond Earth.",
        ],
        ["siddiqi2010", "logsdon2010", "chaikin1994", "nasaimages"],
    ),
]
