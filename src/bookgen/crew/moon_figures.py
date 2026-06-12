"""Chapter figures and Hebrew summaries for the Moon Race book.

Kept separate from the chapter/research data so each content module stays
well under the 150-line limit and has a single responsibility.
"""

from __future__ import annotations

# NASA image URLs (public domain). Each chapter tries the bundled copy in
# assets/chapter-figures/ first (offline, deterministic) and only falls back
# to these URLs when a bundled image is missing.
CHAPTER_FIGURES: list[tuple[str, list[str], str]] = [
    (
        "ch01_cold_war.jpg",
        [
            "https://images-assets.nasa.gov/image/6900846/6900846~orig.jpg",
            "https://images-assets.nasa.gov/image/6900560/6900560~orig.jpg",
        ],
        "Apollo 11 Saturn V on Launch Pad 39A before the Moon landing mission.",
    ),
    (
        "ch02_sputnik.jpg",
        ["https://images-assets.nasa.gov/image/9248168/9248168~orig.jpg"],
        "Sputnik era - the Soviet Union launched the first artificial satellite in 1957.",
    ),
    (
        "ch03_apollo.jpg",
        ["https://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~orig.jpg"],
        "Buzz Aldrin on the Moon during Apollo 11.",
    ),
    (
        "ch04_lunar_surface.jpg",
        ["https://images-assets.nasa.gov/image/as11-40-5927/as11-40-5927~orig.jpg"],
        "Apollo 11 Lunar Module Eagle on the Moon surface.",
    ),
    (
        "ch05_earthrise.jpg",
        ["https://images-assets.nasa.gov/image/as08-14-2383/as08-14-2383~orig.jpg"],
        "Earthrise from Apollo 8 - icon of public opinion and the space race.",
    ),
    (
        "ch06_iss.jpg",
        ["https://images-assets.nasa.gov/image/s75-29432/s75-29432~orig.jpg"],
        "Apollo-Soyuz handshake in space - beginning of post-race cooperation.",
    ),
]

# Hebrew summaries - one isolated RTL block per chapter (no mixed-direction lines).
HEBREW_SUMMARIES: list[str] = [
    (
        "פרק זה מציג את רקע המלחמה הקרה ואת ראשית מרוץ החלל. "
        "שתי מעצמות-העל הפכו טילים בליסטיים להישג יוקרתי שנועד לתעמולה ולהוכחת עליונות טכנולוגית."
    ),
    (
        "פרק זה עוסק ביתרון הסובייטי המוקדם: שיגור הלוויין הראשון והטסת האדם הראשון לחלל. "
        "הישגים אלו זעזעו את ארצות הברית והאיצו את תגובתה."
    ),
    (
        "פרק זה מתאר את תוכניות החלל האמריקאיות - מרקורי, ג'מיני ואפולו - "
        "שריכזו משאבים לאומיים כדי להשיג נחיתה על הירח לפני ברית המועצות."
    ),
    (
        "פרק זה סוקר משימות מפתח: גשושיות רובוטיות שמיפו את הירח, "
        "ולאחריהן נחיתת אפולו 11 שהביאה דגימות ראשונות מפני הירח."
    ),
    (
        "פרק זה בוחן תעמולה, פוליטיקה ודעת קהל. "
        "שני הצדדים הציגו את הישגי החלל כראיה לעליונות שיטתם, תחת לחצי תקציב וסיכון."
    ),
    (
        "פרק זה מסכם את המורשת: סיום עידן אפולו והמעבר מתחרות לשיתוף פעולה בין-לאומי - "
        "מאפולו-סויוז ועד תחנת החלל הבין-לאומית."
    ),
]
