"""Curated prose for chapters 1-3 of the Moon Race book (sections 1-6).

Split from ``moon_prose`` so each content module stays under the 150-line cap.
Every paragraph is unique across the whole book; citation keys are spread so
all bibliography sources are referenced somewhere in the prose.
"""

from __future__ import annotations

# (section_title, paragraphs, citation_keys)
SECTIONS_EARLY: list[tuple[str, list[str], list[str]]] = [
    (
        "Superpower rivalry after 1945",
        [
            "After the Second World War, the United States and the Soviet Union emerged as rival superpowers whose competition shaped global politics for decades. Their contest was ideological, military, and economic, but it was also deeply symbolic: each side sought visible proof that its system could out-build and out-think the other. Space, still an untouched frontier, offered exactly that kind of stage.",
            "The rivalry hardened quickly. Berlin, Korea, and the nuclear arms race left little room for trust, and reliable intelligence on the other side was scarce and prized. In that climate, technological milestones doubled as strategic signals: a successful launch told allies and adversaries alike that a nation could deliver a warhead across continents, so the line between civilian achievement and military deterrence was deliberately blurred.",
            "Walter McDougall's classic political history argues that the space race forced both governments to become technocratic states: to plan, fund, and direct science on a scale that peacetime democracies and command economies alike had never attempted. Spaceflight was therefore never a private adventure; it was state policy, organized around budgets, five-year plans, and election cycles.",
            "The competition also reshaped daily life far from any launch pad. American classrooms gained new science curricula, Soviet engineering institutes expanded, and both publics learned to read rocket launches as scoreboard entries in a global contest. The vocabulary of the era, from missile gap to space age, captured how thoroughly the rivalry had fused technology with identity.",
            "Orbit offered something practical as well as symbolic: a vantage point no treaty could close. Reconnaissance satellites promised photographs of territory that aircraft could reach only at great risk, which is one reason both governments tolerated each other's early satellites instead of treating an overflight as an act of war. The quiet legal precedent set in those first years, that space belongs to no one, proved as consequential as any single launch.",
            "Neither government ever spent purely for show. Every public milestone rested on a foundation of classified work in guidance, reentry, and tracking whose budgets dwarfed the civilian headlines, and historians still debate where the propaganda program ended and the weapons program began. That ambiguity was the point: a nation that could orbit a satellite on demand had proven things no parade could.",
            "Prestige, then, was never a side effect of the space race; it was a central goal. Governments invested enormous resources because being first carried weight in capitals, newspapers, and living rooms around the world. The Moon eventually became the ultimate prize precisely because it was difficult, expensive, and visible to everyone who looked up at night.",
        ],
        ["siddiqi2010", "mcdougall1985", "cadbury2006"],
    ),
    (
        "Rockets, missiles, and prestige",
        [
            "The rockets that carried satellites and cosmonauts were direct descendants of wartime weapons. Germany's V-2, the first large liquid-fueled ballistic missile, proved that controlled rocket flight at the edge of space was possible, and at the war's end both superpowers raced to recruit its engineers and seize its hardware. The expertise gathered in 1945 became the seed of two parallel national programs.",
            "Through the 1950s, missile development and space ambition advanced together. The same boosters designed to deliver nuclear warheads could, with modest changes, loft scientific payloads, so investment in one capability quietly strengthened the other. This dual use meant that every rocket test was watched closely abroad, and that failures were as politically costly as they were technically instructive.",
            "Behind the hardware stood two very different engineering cultures. The Soviet effort concentrated authority in secret design bureaus led by a chief designer whose word settled disputes, while the American program distributed work across military services, private contractors, and laboratories that competed for funding. Each arrangement produced brilliance and waste in its own way, and each left fingerprints on the vehicles it built.",
            "Propellant chemistry, guidance electronics, and lightweight structures all matured in this decade under military budgets. By the time political leaders demanded spectacular space achievements, the underlying technologies were close enough to ready that engineers could promise results within years rather than decades, a confidence that would have been impossible in 1950.",
            "The first launch vehicles made the lineage explicit. The rocket that carried Sputnik was a lightly modified R-7 intercontinental missile, and America's early satellites rode boosters drawn from the Redstone and Jupiter missile programs. Civilian space agencies would later commission dedicated launchers, but the race began on hardware designed to carry warheads, a fact every government involved understood perfectly well.",
            "Prestige tied the whole enterprise together. A reliable, powerful rocket signaled industrial maturity, scientific depth, and military credibility in a single stroke. Because these signals were read by allies, adversaries, and domestic audiences at once, governments were willing to fund ambitious programs whose payoff was measured as much in influence as in engineering.",
        ],
        ["harford1997", "logsdon2010"],
    ),
    (
        "Sputnik and the shock in America",
        [
            "On 4 October 1957 the Soviet Union launched Sputnik 1, the first artificial satellite, and its simple radio beep, audible to amateur listeners worldwide, announced that the space age had begun. The achievement was modest in mass but enormous in meaning: a Soviet object was now passing over American territory several times a day, beyond any power to stop it.",
            "In the United States the reaction was swift and anxious. Commentators spoke of a Sputnik crisis, questioning whether American science and education had fallen behind. The launch reframed space as a domain of national security and pride, and the political pressure it generated would soon reshape budgets and institutions.",
            "The shock was sharpened by surprise. American intelligence knew a Soviet satellite attempt was coming, but the public did not, and the gap between official calm and popular alarm became a political weapon. Newspapers tallied the weight of Sputnik against the weight of planned American satellites, and the comparison, however crude, fixed the impression of a nation suddenly behind.",
            "A month later Sputnik 2 carried the dog Laika into orbit, proving the Soviets could loft a living creature and a much heavier payload. When the first American answer, Vanguard, exploded on its launch pad in front of television cameras that December, the humiliation completed the narrative the Kremlin wanted the world to absorb.",
            "Congress answered with money and law. The National Defense Education Act poured federal funds into science and language teaching, the Advanced Research Projects Agency was created to prevent another technological surprise, and hearings led by Lyndon Johnson kept the supposed gap between the powers on the front page. A single aluminum sphere had redirected a measurable share of the American budget within eighteen months.",
            "The most lasting response was structural. Within a year the United States created NASA to lead civilian spaceflight and expanded federal support for science and engineering education. Sputnik thus did more than orbit the Earth; it set in motion the institutional machinery that would eventually carry Americans to the Moon.",
        ],
        ["cadbury2006", "nasa2019"],
    ),
    (
        "First human in space: Yuri Gagarin",
        [
            "On 12 April 1961 Yuri Gagarin orbited the Earth aboard Vostok 1, becoming the first human in space and handing the Soviet Union another decisive first. The single orbit lasted under two hours, but its symbolic weight was immense: a human being had left the planet and returned, and a Soviet citizen had done it first.",
            "The flight was the product of careful, secretive engineering led by Sergei Korolev, whose identity the Soviet state concealed for security reasons. Vostok's automated systems, life support, and reentry capsule represented years of incremental, high-risk testing, much of it hidden from the public until success could be announced.",
            "Gagarin himself became the mission's second payload. Young, photogenic, and disciplined, he toured dozens of countries as living proof of Soviet modernity, greeted by crowds that no diplomat could draw. The state that had hidden its chief designer placed its cosmonaut on every front page, a reminder that the race was fought in public opinion as much as in orbit.",
            "Less visible was how narrow the margin had been. Vostok's reentry module separated late, the capsule tumbled, and Gagarin ejected to land by parachute, a detail kept quiet for years because international aviation records required the pilot to land with the craft. The gap between the polished story and the risky flight became a pattern of the Soviet program.",
            "Five more Vostok flights pressed the advantage between 1961 and 1963. Gherman Titov spent a full day in orbit, paired capsules flew within sight of each other, and Valentina Tereshkova became the first woman in space, each mission timed and announced for maximum effect. To outside observers the Soviet program seemed to advance on a confident schedule, even though its margins were thinner than anyone outside the design bureaus knew.",
            "Gagarin's flight intensified the contest. Coming only weeks before the first American suborbital flight, it underscored how far ahead the Soviet program appeared and pushed Washington to seek a goal dramatic enough to change the narrative. That goal would soon be named: the Moon.",
        ],
        ["siddiqi2010", "harford1997"],
    ),
    (
        "NASA and the crash program",
        [
            "Faced with repeated Soviet firsts, the United States organized an unprecedented peacetime mobilization of engineering talent. NASA grew rapidly, contracting with universities and thousands of companies to build launch vehicles, spacecraft, tracking networks, and test facilities almost simultaneously. The result was a crash program whose scale rivaled the largest industrial efforts in the nation's history.",
            "Project Mercury came first, proving that Americans could survive launch, orbit, and reentry. Its successes were hard-won and public, and they restored a measure of confidence even as they revealed how much remained unknown about living and working in space.",
            "The seven Mercury astronauts became a new kind of public figure, equal parts test pilot and national symbol. Andrew Chaikin's interviews with the crews describe how flight assignments, training, and even press conferences were engineered as carefully as the capsules, because the program understood that public confidence was a mission system like any other.",
            "Money followed visibility. NASA's budget multiplied several times over within five years of its founding, new centers rose in Houston, Huntsville, and Cape Canaveral, and entire regional economies reorganized around spaceflight. The agency's administrators spent as much energy managing Congress as managing contractors, and both skills proved indispensable.",
            "The contractor web reached into nearly every state. North American Aviation built the command module, Grumman the lunar lander, Boeing, Douglas, and IBM major pieces of the Saturn stack, while universities ran instruments and tracking stations. Spreading the work built political resilience as deliberately as it built hardware, because a program with jobs in four hundred districts is a program Congress hesitates to cancel.",
            "Managing such a program demanded new methods. Systems engineering, rigorous testing schedules, and tight configuration control became as important as any single rocket, because coordinating so many contractors under deadline pressure was itself a formidable technical challenge.",
        ],
        ["logsdon2010", "chaikin1994", "nasa2019"],
    ),
    (
        "From Earth orbit to the lunar landing goal",
        [
            "In May 1961 President Kennedy committed the United States to landing a man on the Moon and returning him safely before the decade's end. The pledge was audacious: the country had barely fifteen minutes of human spaceflight experience, yet it now had a deadline and a destination that the whole world could understand.",
            "Choosing the Moon was a strategic decision as much as a scientific one. It was far enough ahead that the Soviet lead in early milestones would not decide the outcome, and dramatic enough that success would be unmistakable. The goal concentrated national effort on a single, measurable objective.",
            "John Logsdon's study of the decision shows how deliberately it was made. Kennedy asked his advisers for a contest the United States could win, weighed costs that would eventually exceed twenty billion dollars, and accepted that the deadline itself was the point: an open-ended program could drift, but a decade bounded the effort and forced choices.",
            "The commitment also required a method for getting to the Moon at all. After fierce internal debate, NASA chose lunar-orbit rendezvous, a scheme in which a small lander would separate from a mother ship in lunar orbit. The choice saved weight and time but bet the program on rendezvous techniques no one had yet demonstrated.",
            "Gemini retired that bet one flight at a time. Crews learned that rendezvous required orbital mechanics rather than instinct, that spacewalks demanded handholds and underwater training, and that fuel cells could power a two-week mission. By the program's end in 1966 the United States had logged more hours in orbit than the Soviet Union, the first time the scoreboard had clearly flipped.",
            "The deadline disciplined every decision that followed. Proposals that could not fly before 1970 were set aside however elegant they looked on paper, test programs were run in parallel rather than in sequence, and an all-up testing philosophy launched complete Saturn stacks at once instead of stage by stage. The schedule was a risk multiplier and a focus mechanism at the same time, and Apollo's managers spent the decade balancing the two.",
            "Project Gemini bridged the gap between ambition and capability. Its flights practiced the rendezvous, docking, long-duration flight, and spacewalking that a lunar mission would require, turning Kennedy's promise into a sequence of solvable engineering problems.",
        ],
        ["logsdon2010", "cadbury2006"],
    ),
]
