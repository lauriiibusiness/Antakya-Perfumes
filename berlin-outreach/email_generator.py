"""
email_generator.py — Generate personalized German cold emails.
4 template variations per scenario to avoid mass-mail patterns.
"""

import random

SENDER_NAME = "Ioana Laura Mocanu"

CATEGORY_PHRASES = {
    "Restaurant": "Restaurants",
    "Café": "Cafés",
    "Friseursalon": "Friseursalons",
    "Barbershop": "Barbershops",
    "Boutique": "Boutiquen",
    "Fitnessstudio": "Fitnessstudios",
    "Personal Trainer": "Personal Trainern",
    "Nagelstudio": "Nagelstudios",
    "Tattoostudio": "Tattoostudios",
    "Einzelhandel": "lokalen Geschäften",
}

# ── No website ──────────────────────────────────────────────────────────────

_NO_WEBSITE = [
    """\
Hallo {name}-Team,

beim Stöbern nach {cat} in Berlin bin ich auf euch gestoßen – klingt wirklich toll, was ihr macht!

Ich habe allerdings keine Website gefunden. Gerade in Berlin suchen die meisten Kunden zuerst online – ohne Website gehen viele einfach weiter.

Ich gestalte moderne Landing Pages für Berliner Unternehmen ab €350 – fertig in wenigen Tagen, ohne technischen Aufwand für euch.

Habt ihr 15 Minuten für ein kurzes Gespräch? Antwortet einfach auf diese Mail!

Herzliche Grüße aus Berlin,
{sender}""",

    """\
Guten Tag,

mein Name ist Ioana – ich bin Webdesignerin und helfe kleinen Berliner Unternehmen, online sichtbarer zu werden.

Ich bin auf {name} gestoßen, aber leider ohne Website. Das ist schade, denn viele potenzielle Kunden googeln, bevor sie irgendwo hingehen.

Ich erstelle professionelle Landing Pages ab €350 – mobilfreundlich, schnell und für Berlin optimiert.

Wäre ein kurzes 15-minütiges Gespräch möglich? Einfach auf diese E-Mail antworten.

Mit freundlichen Grüßen,
{sender}""",

    """\
Hey {name}-Team!

Ich wollte kurz melden – bin bei meiner Suche nach {cat} in Berlin auf euch aufmerksam geworden. Cooles Konzept!

Nur aufgefallen: Ich konnte keine Website finden. In einer Stadt wie Berlin verliert man dadurch wirklich viele Kunden.

Ich baue schnelle, moderne Landing Pages für lokale Berliner Unternehmen – ab €350, in wenigen Tagen fertig.

Hättet ihr 15 Minuten für ein kurzes Kennenlernen? Meldet euch einfach hier!

Bis bald,
{sender}""",

    """\
Hallo {name},

ich heiße Ioana und arbeite als Webdesignerin in Berlin. Auf der Suche nach {cat} bin ich auf euch gestoßen – aber eine Website habe ich leider nicht gefunden.

Für Berliner Unternehmen ist eine professionelle Online-Präsenz wirklich wichtig – neue Kunden, bessere Sichtbarkeit.

Ich erstelle Landing Pages ab €350, komplett fertig und ohne Stress für euch.

Kurzes Gespräch gefällig? 15 Minuten reichen – einfach hier antworten.

Viele Grüße,
{sender}""",
]

# ── Has website (offer redesign) ────────────────────────────────────────────

_HAS_WEBSITE = [
    """\
Hallo {name}-Team,

ich bin zufällig auf eure Website gestoßen – tolles Unternehmen! Ich denke aber, dass die Seite optisch nicht ganz zeigt, was ihr wirklich bietet.

Eine moderne, frische Website kann entscheiden, ob ein Besucher bleibt oder zur Konkurrenz wechselt.

Ich biete Website-Redesigns für Berliner Unternehmen ab €500 – schnell umgesetzt, professionell und ohne großen Aufwand für euch.

Hättet ihr 15 Minuten für ein kurzes Gespräch? Antwortet einfach auf diese Mail!

Herzliche Grüße,
{sender}""",

    """\
Guten Tag,

mein Name ist Ioana, ich bin Webdesignerin in Berlin. Ich schaue mir regelmäßig Websites lokaler Unternehmen an – und bin dabei auf {name} gestoßen.

Die Website hat Potenzial, aber ein paar moderne Updates könnten wirklich einen Unterschied machen und mehr Kunden bringen.

Ich biete Website-Redesigns ab €500 – für Berliner Unternehmen optimiert, fertig innerhalb von 2 Wochen.

Wäre ein kurzes Kennenlernen möglich? 15 Minuten – einfach auf diese E-Mail antworten!

Herzliche Grüße aus Berlin,
{sender}""",

    """\
Hey {name}-Team!

Ich habe eure Website besucht und finde das Konzept wirklich gut – aber ehrlich gesagt sieht die Seite etwas veraltet aus und zeigt nicht, wie besonders ihr seid.

Als Webdesignerin helfe ich Berliner Unternehmen zu einer modernen Online-Präsenz. Redesigns ab €500, in 2 Wochen fertig.

Hättet ihr 15 Minuten für ein kurzes Gespräch? Würde mich freuen!

Viele Grüße,
{sender}""",

    """\
Hallo {name},

ich heiße Ioana und bin Webdesignerin in Berlin. Ich habe eure Website kurz angeschaut – gute Inhalte, aber das Design könnte frischer sein und mehr Besucher zu Kunden machen.

Für lokale Berliner Unternehmen mache ich professionelle Redesigns ab €500 – schnell, modern und effektiv.

Kurzes Gespräch möglich? 15 Minuten reichen – einfach hier antworten.

Herzliche Grüße,
{sender}""",
]

_SUBJECTS_NO_WEBSITE = [
    "Website für {name}?",
    "Kurze Frage zur Online-Präsenz – {name}",
    "Online in Berlin gefunden – aber keine Website",
    "Schnell gefunden in Berlin – {name}",
]

_SUBJECTS_HAS_WEBSITE = [
    "Kurze Idee für die Website von {name}",
    "Euer Online-Auftritt – {name}",
    "Website-Update für {name}?",
    "Kleiner Vorschlag für {name}",
]


def generate_email(business_name: str, category: str, has_website: bool) -> str:
    cat_phrase = CATEGORY_PHRASES.get(category, category)
    pool = _HAS_WEBSITE if has_website else _NO_WEBSITE
    return random.choice(pool).format(
        name=business_name,
        cat=cat_phrase,
        sender=SENDER_NAME,
    )


def get_subject(business_name: str, has_website: bool) -> str:
    pool = _SUBJECTS_HAS_WEBSITE if has_website else _SUBJECTS_NO_WEBSITE
    return random.choice(pool).format(name=business_name)
