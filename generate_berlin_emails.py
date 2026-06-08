#!/usr/bin/env python3
"""
Berlin Business Cold Email CSV Generator
Generates personalized German cold emails for 82 local Berlin businesses.
Replace [DEIN NAME] in the CSV with your actual name before sending.

Format: vertical — each business occupies its own block of rows.
Columns: Field | Value
"""
import csv
import os

SENDER_NAME = "[DEIN NAME]"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "berlin_cold_emails.csv")


# ---------------------------------------------------------------------------
# Template functions — each returns (betreff, email_body)
# All emails are under 150 words, natural German.
# ---------------------------------------------------------------------------

def r1(name, sender):
    betreff = f"Mehr Gäste durch eine modernere Website – {name}"
    body = (
        f"Hallo {name}-Team,\n\n"
        "beim Recherchieren nach schönen Berliner Restaurants bin ich auf Sie aufmerksam geworden – tolles Konzept!\n\n"
        "Als Webdesigner aus Berlin fällt mir auf, dass viele kleine Restaurants Websites haben, "
        "die auf dem Smartphone nicht mehr ganz zeitgemäß wirken. Das kostet täglich potenzielle Gäste.\n\n"
        "Ich helfe Berliner Restaurants mit moderner Webpräsenz: übersichtliche Speisekarte, "
        "einfache Online-Reservierung, mobilfreundliches Design.\n\n"
        "Kosten: ab €500–800 für ein vollständiges Redesign – einmalig, keine Monatsgebühren.\n\n"
        "Hätten Sie Lust auf ein kurzes 15-Minuten-Gespräch? Antworten Sie einfach auf diese E-Mail.\n\n"
        f"Viele Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def r2(name, sender):
    betreff = f"Kurze Idee für Ihren Online-Auftritt – {name}"
    body = (
        f"Guten Tag {name}-Team,\n\n"
        "ich bin Webdesigner aus Berlin und schaue mir gern an, wie sich lokale Gastronomiebetriebe online präsentieren.\n\n"
        f"{name} macht auf mich einen tollen Eindruck – aber Ihre aktuelle Website hält "
        "mit der Qualität Ihres Angebots leider noch nicht ganz Schritt.\n\n"
        "Eine frische, mobilfreundliche Website mit digitalem Menü und Reservierungsmöglichkeit "
        "kann da wirklich viel ausmachen.\n\n"
        "Preis: ab €500–800 für ein Redesign, einmalig.\n\n"
        "Haben Sie Interesse an einem kostenlosen 15-Minuten-Call? Schreiben Sie mir einfach zurück!\n\n"
        f"Herzliche Grüße,\n{sender}"
    )
    return betreff, body

def r3(name, sender):
    betreff = "Ihre Website in Berlin – eine kurze Idee von mir"
    body = (
        f"Hallo {name}-Team,\n\n"
        f"{name} ist mir beim Entdecken lokaler Berliner Gastronomiebetriebe aufgefallen – schöner Laden!\n\n"
        "Ich bin Webdesigner in Berlin und helfe kleinen Betrieben dabei, online mehr Gäste zu gewinnen. "
        "Oft macht schon ein modernes, mobilfreundliches Design einen großen Unterschied.\n\n"
        "Ein Redesign gibt es bei mir ab €500–800 – einmalig und transparent kalkuliert.\n\n"
        "Hätten Sie kurz Zeit für ein 15-Minuten-Gespräch? Ich freue mich auf Ihre Antwort!\n\n"
        f"Mit freundlichen Grüßen aus Berlin,\n{sender}"
    )
    return betreff, body

def c1(name, sender):
    betreff = f"Ihr Café verdient eine schönere Website – {name}"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Ihr Café ist mir beim Stöbern nach Berliner Lieblingsorten aufgefallen – eine wirklich einladende Adresse!\n\n"
        "Als Webdesigner in Berlin frage ich mich allerdings: Strahlt Ihre Website dieselbe Gemütlichkeit "
        "aus wie Ihr Café selbst?\n\n"
        "Ich helfe Berliner Cafés mit modernen Websites, die genauso einladen wie der Laden selbst – "
        "aktuelles Menü, stimmungsvolle Fotos, mobiles Design.\n\n"
        "Kosten: ab €500–800 für ein Redesign.\n\n"
        "Haben Sie Lust auf ein kurzes 15-Minuten-Gespräch? Einfach auf diese E-Mail antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def c2(name, sender):
    betreff = "Guter Kaffee, bessere Website – kurze Idee aus Berlin"
    body = (
        f"Guten Tag {name}-Team,\n\n"
        "guter Kaffee verdient einen großartigen Auftritt – online wie offline.\n\n"
        "Ich bin Webdesigner aus Berlin und helfe Cafés dabei, im Netz genauso gut rüberzukommen wie in echt. "
        "Ob Speisekarte, Öffnungszeiten oder Veranstaltungshinweise – eine moderne Website macht den Unterschied.\n\n"
        "Berliner Cafés biete ich ein professionelles Website-Redesign ab €500–800 an – ohne Monatsgebühren.\n\n"
        "Interesse an einem kurzen 15-Minuten-Call? Schreiben Sie mir einfach!\n\n"
        f"Viele Grüße,\n{sender}"
    )
    return betreff, body

def c3(name, sender):
    betreff = f"Mehr Gäste für {name} – Idee aus Berlin"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Ihr Café hier in Berlin hat mich beim Recherchieren angesprochen – schöne Atmosphäre!\n\n"
        "Ich bin Webdesigner in Berlin und schaue mir gern an, wie lokale Cafés online auftreten. "
        "Viele haben Websites, die dem Charme ihres Ladens leider noch nicht ganz gerecht werden.\n\n"
        "Mit einem frischen Redesign können Sie online genauso viel Eindruck machen wie persönlich – "
        "ab €500–800, einmalig.\n\n"
        "Kurzes 15-Minuten-Gespräch? Einfach antworten!\n\n"
        f"Mit freundlichen Grüßen aus Berlin,\n{sender}"
    )
    return betreff, body

def h1(name, sender):
    betreff = "Online-Terminbuchung & frisches Design für Euren Salon"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Euer Salon ist mir beim Recherchieren aufgefallen – tolles Handwerk!\n\n"
        "Ich bin Webdesigner in Berlin und frage mich: Können Eure Kunden direkt über Eure Website "
        "Termine buchen? Und macht die Seite auf dem Handy einen guten Eindruck?\n\n"
        "Online-Terminbuchung, Foto-Galerie und ein modernes mobilfreundliches Design – "
        "das biete ich Friseursalons für ein Redesign ab €500–800.\n\n"
        "Habt Ihr kurz Zeit für ein 15-Minuten-Gespräch? Antwortet einfach auf diese Mail!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def h2(name, sender):
    betreff = f"Kurze Frage zu Ihrer Friseur-Website – {name}"
    body = (
        f"Guten Tag {name}-Team,\n\n"
        "als Webdesigner aus Berlin schaue ich mir regelmäßig Friseur-Websites an – "
        "dabei bin ich auf Sie aufmerksam geworden.\n\n"
        "Ihr Salon macht einen super Eindruck, doch Ihre Website könnte eine Auffrischung vertragen – "
        "besonders für mobile Nutzer ist das heute entscheidend.\n\n"
        "Ich biete Berliner Friseursalons ein professionelles Redesign an: "
        "klares Design, Galerie, Online-Terminbuchung – ab €500–800.\n\n"
        "Kurzes 15-Minuten-Gespräch? Einfach auf diese E-Mail antworten!\n\n"
        f"Mit freundlichen Grüßen,\n{sender}"
    )
    return betreff, body

def h3(name, sender):
    betreff = "Mehr Neukunden durch eine modernere Website"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Ihr Friseurladen in Berlin hat mich beim Recherchieren überzeugt – schöner Salon!\n\n"
        "Eine Frage: Wirkt Ihre Website genauso einladend wie Ihr Geschäft? "
        "Viele Kunden googeln einen Friseur, bevor sie buchen. "
        "Mit einer modernen Seite mit Online-Terminbuchung lassen sich deutlich mehr Neukunden gewinnen.\n\n"
        "Ein Redesign gibt es bei mir ab €500–800 – einmalig, klar und fair.\n\n"
        "Ich würde mich über ein 15-Minuten-Gespräch freuen – einfach antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def b1(name, sender):
    betreff = "Freshe Website für euren Barbershop?"
    body = (
        f"Hey {name}-Team,\n\n"
        "euer Barbershop in Berlin ist mir aufgefallen – cooler Laden!\n\n"
        "Ich bin Webdesigner in Berlin und frage mich: Passt eure Website zum Vibe eures Shops?\n\n"
        "Viele Barbershops haben Websites, die etwas angestaubt wirken. "
        "Ich mache das frisch – mit starkem Design, Online-Terminbuchung und guter Darstellung auf dem Handy.\n\n"
        "Redesign ab €500–800 – einmalig.\n\n"
        "Bock auf einen kurzen 15-Minuten-Call? Schreibt mir einfach zurück!\n\n"
        f"Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def b2(name, sender):
    betreff = f"Moderner Online-Auftritt für {name}"
    body = (
        f"Hallo {name}-Team,\n\n"
        "ich bin Webdesigner aus Berlin und spezialisiere mich auf lokale Geschäfte – "
        "dabei bin ich auf euren Barbershop gestoßen.\n\n"
        "Der erste Eindruck online entscheidet oft, ob jemand bucht. "
        "Mit einer modernen Website mit Galerie und Online-Terminbuchung holt ihr mehr aus eurer Sichtbarkeit raus.\n\n"
        "Angebot: Redesign ab €500–800, einmalig.\n\n"
        "Habt ihr Zeit für einen 15-Minuten-Call? Einfach auf diese E-Mail antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def bt1(name, sender):
    betreff = "Eure Boutique, noch stylischer online"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Eure Boutique in Berlin ist mir aufgefallen – schöne Auswahl und tolles Konzept!\n\n"
        "Als Webdesigner in Berlin frage ich mich: Spiegelt Eure Website Euren Stil "
        "genauso gut wider wie Euer Laden selbst?\n\n"
        "Ich helfe Berliner Modeboutiquen mit stilvollen, modernen Online-Auftritten – "
        "übersichtlich, mobilfreundlich, ansprechend.\n\n"
        "Redesign ab €500–800, einmalig.\n\n"
        "Hätte ich kurz Euer Ohr für 15 Minuten? Antwortet einfach auf diese Mail!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def bt2(name, sender):
    betreff = f"Kurze Idee für Ihren Boutique-Auftritt – {name}"
    body = (
        f"Guten Tag {name}-Team,\n\n"
        "gute Mode verdient eine gute Website – das ist meine Überzeugung als Berliner Webdesigner.\n\n"
        f"Beim Recherchieren bin ich auf {name} gestoßen – toller Laden! "
        "Ich frage mich jedoch, ob Ihre aktuelle Website Ihren Kollektionen wirklich gerecht wird, "
        "besonders auf dem Smartphone.\n\n"
        "Professionelles Website-Redesign für Berliner Boutiquen: elegantes Design, Produktgalerie, "
        "mobil optimiert – ab €500–800.\n\n"
        "Interesse an einem 15-Minuten-Gespräch? Einfach antworten!\n\n"
        f"Mit freundlichen Grüßen,\n{sender}"
    )
    return betreff, body

def f1(name, sender):
    betreff = "Neue Mitglieder durch eine moderne Studio-Website"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Euer Studio in Berlin macht einen starken Eindruck – genau das suchen Sportbegeisterte in der Stadt!\n\n"
        "Ich frage mich: Können potenzielle Mitglieder Euren Kursplan und Eure Angebote "
        "einfach online finden und buchen?\n\n"
        "Als Webdesigner in Berlin baue ich Fitness-Studios moderne Websites mit Kursübersicht, "
        "Online-Buchung und Trainer-Profilen – Redesign ab €500–800.\n\n"
        "Kurzes 15-Minuten-Gespräch? Schreibt mir einfach!\n\n"
        f"Sportliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def f2(name, sender):
    betreff = f"Mehr Kursteilnehmer für {name} – kurze Idee"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Euer Studio in Berlin ist mir beim Recherchieren aufgefallen – eine tolle Adresse!\n\n"
        "Frage: Findet Ihr auch genug neue Kursteilnehmer über Eure Website? "
        "Viele Studiowebsites sind nicht mobil optimiert oder wirken etwas veraltet.\n\n"
        "Ich biete Berliner Studios ein modernes Redesign an: Kursplan, Online-Buchung, "
        "stimmungsvolle Darstellung – ab €500–800.\n\n"
        "Interesse an einem 15-Minuten-Gespräch? Einfach antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def pt1(name, sender):
    betreff = "Mehr Klienten durch einen professionellen Webauftritt"
    body = (
        f"Hallo {name},\n\n"
        "als Personal Trainer in Berlin lebt man von Empfehlungen – aber auch von der Online-Sichtbarkeit.\n\n"
        "Ich bin Webdesigner aus Berlin und helfe Trainern dabei, online professionell aufzutreten "
        "und neue Klienten zu gewinnen: Leistungsübersicht, Erfolgsgeschichten, Kontaktformular.\n\n"
        "Landing Page ab €350–500, vollständiges Redesign ab €500–800 – einmalig, ohne Monatsgebühren.\n\n"
        "Hätten Sie Interesse an einem kurzen 15-Minuten-Gespräch? Einfach auf diese E-Mail antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def n1(name, sender):
    betreff = "Terminbuchung & moderne Website für euer Nagelstudio"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Euer Nagelstudio in Berlin ist mir aufgefallen – tolle Arbeit!\n\n"
        "Ich frage mich: Können Eure Kunden direkt über Eure Website Termine buchen? "
        "Und macht die Seite auf dem Handy einen guten Eindruck?\n\n"
        "Als Webdesigner in Berlin helfe ich Nagelstudios mit modernen Websites: "
        "Galerie, Preisliste, Online-Terminbuchung – ab €500–800.\n\n"
        "Kurzes 15-Minuten-Gespräch? Einfach auf diese E-Mail antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def t1(name, sender):
    betreff = "Euer Portfolio online – so wie es verdient"
    body = (
        f"Hey {name}-Team,\n\n"
        "euer Studio in Berlin ist mir aufgefallen – wirklich beeindruckendes Portfolio!\n\n"
        "Ich bin Webdesigner aus Berlin und frage mich: Zeigt eure Website euer Können "
        "so, wie es verdient?\n\n"
        "Tattoo-Kunden schauen sich online intensiv um, bevor sie buchen. "
        "Eine moderne Website mit Künstler-Galerie und Portfolio macht da einen Riesenunterschied.\n\n"
        "Redesign ab €500–800, einmalig.\n\n"
        "Bock auf einen kurzen 15-Minuten-Call? Schreibt mir einfach!\n\n"
        f"Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def t2(name, sender):
    betreff = f"Kurze Idee für eure Tattoo-Website – {name}"
    body = (
        f"Hallo {name}-Team,\n\n"
        "als Webdesigner aus Berlin schaue ich mir regelmäßig Tattoo-Studio-Websites an – "
        "dabei bin ich auf euch gestoßen.\n\n"
        "Eure Arbeit ist beeindruckend. Aber bekommt euer Online-Auftritt der Qualität "
        "eurer Kunst wirklich gerecht?\n\n"
        "Eine moderne Tattoo-Website mit Portfolio, Künstlerprofilen und Buchungsmöglichkeit "
        "zieht genau die richtigen Kunden an – Redesign ab €500–800.\n\n"
        "Kurzes 15-Minuten-Gespräch? Einfach antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def lr1(name, sender):
    betreff = "Eure Buchhandlung online besser sichtbar machen"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Euer Buchladen in Berlin ist eine echte Bereicherung – solche unabhängigen "
        "Buchhandlungen braucht die Stadt!\n\n"
        "Ich frage mich: Finden Leseratten Euch auch online gut genug? "
        "Viele kleine Buchläden haben Websites, die dem Charme ihres Ladens noch nicht ganz gerecht werden.\n\n"
        "Als Webdesigner in Berlin helfe ich kleinen Händlern mit modernen Websites – "
        "Sortimentsübersicht, Öffnungszeiten, Veranstaltungshinweise.\n\n"
        "Landing Page ab €350–500, Redesign ab €500–800.\n\n"
        "Kurzes 15-Minuten-Gespräch? Einfach antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def lr2(name, sender):
    betreff = "Mehr Berliner Familien finden euren Laden"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Euer Spielzeugladen in Berlin ist mir aufgefallen – ein echter Schatz für Berliner Familien!\n\n"
        "Ich bin Webdesigner aus Berlin und frage mich: Können Eltern Euer Sortiment "
        "und Eure Öffnungszeiten einfach online finden?\n\n"
        "Viele kleine Läden haben Websites, die noch etwas Liebe brauchen – ich helfe gerne dabei.\n\n"
        "Eine moderne, übersichtliche Website gibt es bei mir ab €350–500.\n\n"
        "Kurzes 15-Minuten-Gespräch? Einfach auf diese E-Mail antworten!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body

def lr3(name, sender):
    betreff = "Euer Blumengeschäft mit einer schöneren Website"
    body = (
        f"Hallo {name}-Team,\n\n"
        "Euer Blumengeschäft in Berlin ist mir aufgefallen – wirklich schöne Arbeit!\n\n"
        "Ich frage mich: Können Kunden Eure Arrangements und Angebote auch online "
        "bewundern und direkt anfragen?\n\n"
        "Als Webdesigner in Berlin helfe ich kleinen Läden mit stimmungsvollen, modernen Websites: "
        "Galerie, Kontaktformular, mobiloptimiert.\n\n"
        "Landing Page ab €350–500, Redesign ab €500–800 – einmalig.\n\n"
        "Kurzes 15-Minuten-Gespräch gefällig? Schreibt mir einfach!\n\n"
        f"Herzliche Grüße aus Berlin,\n{sender}"
    )
    return betreff, body


# ---------------------------------------------------------------------------
# Business data: (Name, Category, Email, Website, template_fn)
# ---------------------------------------------------------------------------

businesses = [
    # --- RESTAURANTS (14) ---
    ("mittendrin – Restaurant & Café",  "Restaurant", "mail@mittendrin-in-berlin.de",    "https://www.mittendrin-in-berlin.de",              r1),
    ("Cô Chu",                          "Restaurant", "hello@co-chu.de",                 "https://co-chu.de",                                r1),
    ("KUCHI Restaurants",               "Restaurant", "mail@kuchi.de",                   "https://kuchi.de",                                 r1),
    ("Maximilians Restaurant",          "Restaurant", "info@maximilians-berlin.de",       "https://www.maximilians-berlin.de",                r1),
    ("Restauration 1840",               "Restaurant", "controlling@hm-restaurants.de",   "https://www.berlin-1840.de",                       r2),
    ("FREA Restaurant",                 "Restaurant", "reservierung@frea.de",            "https://www.frea.de",                              r2),
    ("Ga Ya Ya",                        "Restaurant", "info@gayaya.de",                  "https://www.gayaya.restaurant",                    r2),
    ("Jäger & Lustig",                  "Restaurant", "info@jaegerundlustig.de",         "https://jaegerundlustig.de",                       r2),
    ("3 Schwestern",                    "Restaurant", "info@3schwestern.com",            "https://www.3schwestern.com",                      r3),
    ("Chay Village",                    "Restaurant", "info@chayvillage.de",             "https://www.chayvillage.de",                       r3),
    ("Makan Enak",                      "Restaurant", "info@anugerah.de",                "https://makanenak.de",                             r3),
    ("Malafemmena",                     "Restaurant", "info@malafemmena.restaurant",     "https://malafemmena.restaurant",                   r3),
    ("EINS44",                          "Restaurant", "info@eins44.com",                 "https://www.eins44.com",                           r3),
    ("Burro Unchained",                 "Restaurant", "tables@burro-unchained.com",      "https://www.burro-unchained.com",                  r3),

    # --- CAFÉS (12) ---
    ("FREA Bakery",                     "Café", "hello@freabakery.de",                "https://www.freabakery.de",                       c1),
    ("Café Anna Blume",                 "Café", "info@cafe-anna-blume.de",            "https://cafe-anna-blume.de",                      c1),
    ("Café Chagall",                    "Café", "info@cafe-chagall.de",               "https://www.cafe-chagall.com",                    c1),
    ("Café Liebling",                   "Café", "hello@cafeliebling.berlin",          "https://www.cafeliebling.berlin",                 c1),
    ("Mo's Coffee",                     "Café", "info@moscoffee.de",                  "https://www.moscoffee.de",                        c2),
    ("KAFFEE.BAR",                      "Café", "info@kaffeebar.berlin",              "https://www.kaffeebar.berlin",                    c2),
    ("Café Krone",                      "Café", "cafekroneberlin@gmail.com",          "https://www.krone-berlin.com",                    c2),
    ("Café Tiergarten",                 "Café", "mail@cafetiergarten.berlin",         "https://cafetiergarten.berlin",                   c2),
    ("Café Berio",                      "Café", "post@berio-berlin.de",               "https://berio-berlin.de",                         c3),
    ("Saaldeck Café & Bar",             "Café", "mail@saaldeck.de",                   "https://www.saaldeck.de",                         c3),
    ("Blume an der Hasenheide",         "Café", "post@blumeberlin.de",                "https://blumeberlin.de",                          c3),
    ("Blumental",                       "Café", "reservierungen@blumental-berlin.de", "https://blumental-berlin.de",                     c3),

    # --- FRISEURSALONS (13) ---
    ("em-style",                   "Friseursalon", "kontakt@em-style.de",                 "https://www.em-style.de",                    h1),
    ("YAO Berlin",                 "Friseursalon", "info@yao-berlin.de",                  "https://www.yao-berlin.de",                   h1),
    ("Kleinod Salon",              "Friseursalon", "mail@kleinod-salon.de",               "https://www.kleinod-salon.de",                h1),
    ("FON Friseur Berlin",         "Friseursalon", "info@fon-friseur.de",                 "https://www.fon-friseur.de",                  h1),
    ("Haarmacher",                 "Friseursalon", "team@haarmacher.com",                 "https://www.haarmacher.com",                  h1),
    ("Art Cut",                    "Friseursalon", "info@artcut.eu",                      "https://www.artcut.eu",                       h2),
    ("Friseur Kristallglanz",      "Friseursalon", "info@kristallglanz.com",              "https://www.kristallglanz.com",               h2),
    ("van Baal Friseure",          "Friseursalon", "info@van-baal-friseure.de",           "https://www.van-baal-friseure.de",            h2),
    ("Friseur Kopfkultur",         "Friseursalon", "info@friseurkopfkultur-berlin.de",    "https://www.friseurkopfkultur-berlin.de",     h2),
    ("HARMS Friseure Berlin",      "Friseursalon", "info@harms-friseure-berlin.de",       "https://www.harms-friseure-berlin.de",        h2),
    ("Goldcut Friseure Weißensee", "Friseursalon", "info@goldcut-friseure.de",            "https://goldcut-friseure-weissensee.de",      h3),
    ("Haarstudio Yvonne",          "Friseursalon", "info@haarstudio-yvonne.de",           "https://haarstudioyvonne.de",                 h3),
    ("Unique Friseursalon",        "Friseursalon", "info@unique-friseur.de",              "http://www.unique-friseur.de",                h3),

    # --- BARBERSHOPS (8) ---
    ("Barbabella Berlin",           "Barbershop", "manoman@barbabella.berlin",              "https://barbabella.berlin",                   b1),
    ("Barber Studio",               "Barbershop", "info@barber.studio",                    "https://barber.studio",                       b1),
    ("BARBERLIN",                   "Barbershop", "info@barberlin.co",                     "https://barberlin.co",                        b1),
    ("ROWDY Barbershop",            "Barbershop", "info@gertrac.de",                       "https://www.rowdy-barber.de",                 b1),
    ("Barbers Berlin",              "Barbershop", "info@berlin-barbers.com",               "https://berlin-barbers.com",                  b2),
    ("Barber Shop Berlin",          "Barbershop", "vahel77@live.de",                       "https://www.barber-shop-berlin.de",           b2),
    ("Brothers Barbershop Berlin",  "Barbershop", "brothers.barbershop.berlin@gmail.com",  "https://brothers-barbershop-berlin.business.site", b2),
    ("Barber Who Berlin",           "Barbershop", "barberwhoberlin@gmail.com",             "https://barberwhoberlin.nearcut.de",          b2),

    # --- BOUTIQUEN (7) ---
    ("Ofelia Berlin",       "Boutique", "ofeliaberlin@gmx.net",       "http://www.ofelia-berlin.de",   bt1),
    ("Per Donna",           "Boutique", "info@perdonna-berlin.de",    "https://www.perdonna-berlin.de", bt1),
    ("MOOI Berlin",         "Boutique", "hallo@mooiberlin.com",       "https://mooiberlin.com",         bt1),
    ("NOVeL Concept Store", "Boutique", "info@novelberlin.de",        "https://www.novelberlin.de",     bt2),
    ("Image Modeboutique",  "Boutique", "mail@image-modeboutique.de", "https://image-modeboutique.de",  bt2),
    ("MK-Mode",             "Boutique", "info@mk-mode.de",            "https://www.mk-mode.de",         bt2),
    ("Broke + Schön",       "Boutique", "hello@brokeberlin.de",       "https://brokeundschoen.de",      bt2),

    # --- FITNESS / YOGA / PILATES (6) ---
    ("CrossFit Icke",        "Fitnessstudio", "kontakt@crossfiticke.com",     "https://www.crossfiticke.com",    f1),
    ("Green Gym Berlin",     "Fitnessstudio", "info@greengymberlin.de",       "https://www.greengymberlin.de",   f1),
    ("MAKEDA Pilates Studio","Pilates Studio","info@makeda-pilates.de",       "https://www.makeda-pilates.de",   f1),
    ("Berlin Pilates Studio","Pilates Studio","info@berlinpilatesstudio.com", "https://berlinpilatesstudio.com", f2),
    ("Peace Yoga Berlin",    "Yoga Studio",  "info@peaceyoga.de",             "https://peaceyoga.de",            f2),
    ("Kreuzberg Yoga",       "Yoga Studio",  "info@kreuzbergyoga.de",         "https://www.kreuzbergyoga.de",    f2),

    # --- PERSONAL TRAINER (3) ---
    ("Andreas Heumann Personal Training","Personal Trainer","andreas@heumann-personaltraining.berlin","https://heumann-personaltraining.berlin",  pt1),
    ("Sportsfreund Grüner",              "Personal Trainer","kontakt@sportsfreund-berlin.de",         "https://www.sportsfreund-berlin.de",        pt1),
    ("Berlin Personal Training",         "Personal Trainer","info@berlin-personal-training.de",       "https://www.berlin-personal-training.de",   pt1),

    # --- NAGELSTUDIOS (4) ---
    ("Beauty Nails Charlottenburg","Nagelstudio","beautynails80@gmail.com",      "https://beautynailscharlottenburg.de", n1),
    ("Angel Nails Berlin",         "Nagelstudio","info@angelnailsonline.de",     "https://angelnailsonline.de",          n1),
    ("Hauptstadt Nails",           "Nagelstudio","info@hauptstadt-nails.de",     "https://hauptstadt-nails.de",          n1),
    ("Thanh Dat Nagelstudio",      "Nagelstudio","info@thanhdat-nagelstudio.de", "https://www.thanhdat-nagelstudio.de", n1),

    # --- TATTOO STUDIOS (8) ---
    ("Nuclearabbit Tattoo Studio","Tattoo Studio","nuclearabbit.studio@gmail.com","https://www.nuclearabbit.com",  t1),
    ("Kiezliner Tattoo Studio",   "Tattoo Studio","kiezliner.tattoo@gmail.com",  "https://kiezliner-tattoo.de",    t1),
    ("Blut und Eisen Tattoo",     "Tattoo Studio","info@blutundeisen.de",        "https://blutundeisen.de",         t1),
    ("Selfmade Tattoo Berlin",    "Tattoo Studio","info@selfmade-tattoo.de",     "https://www.selfmade-tattoo.de",  t1),
    ("Mugshot Tattoo",            "Tattoo Studio","hello@mugshot-tattoo.com",    "https://mugshot-tattoo.com",      t2),
    ("CNX Tattoo & Piercing",     "Tattoo Studio","cnxtattoo@gmail.com",         "https://www.cnxtattoo.com",       t2),
    ("Tattoo Devil Berlin",       "Tattoo Studio","mail@tattoo-devil.de",        "https://www.tattoo-devil.de",     t2),
    ("Tiba Tattoo Studio",        "Tattoo Studio","info@tibatattoo.de",          "https://www.tibatattoo.com",      t2),

    # --- BUCHHANDLUNGEN (3) ---
    ("LeseGlück",      "Buchhandlung","email@leseglueck-berlin.de","https://www.leseglueck-berlin.de", lr1),
    ("buch|bund",      "Buchhandlung","info@buchbund.de",          "https://buchbund.de",               lr1),
    ("Die Buchkönigin","Buchhandlung","hallo@buchkoenigin.de",     "https://www.buchkoenigin.de",       lr1),

    # --- SPIELZEUGLADEN (1) ---
    ("Spielzeugladen an der Kaisereiche","Spielzeugladen","sadk-berlin@gmx.de","https://www.sadk-berlin.de", lr2),

    # --- FLORISTEN (3) ---
    ("Blumenbett",         "Florist","info@blumenbett.de",      "https://www.blumenbett.de",      lr3),
    ("Frau Rose Floristik","Florist","info@fraurose.de",        "https://www.fraurose.de",        lr3),
    ("Kornblume Floristik","Florist","info@lindes-kornblume.de","https://www.lindes-kornblume.de", lr3),
]


# ---------------------------------------------------------------------------
# Generate vertical CSV
# Layout: two columns — Field | Value
# Each business occupies a header row + 6 data rows + 1 blank separator row
# ---------------------------------------------------------------------------

def main():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        # Column headers
        writer.writerow(["Feld", "Wert"])

        for i, (name, category, email, website, tmpl_fn) in enumerate(businesses, start=1):
            betreff, body = tmpl_fn(name, SENDER_NAME)

            # Business separator / number header
            writer.writerow([f"━━━ #{i} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", ""])
            writer.writerow(["Business Name", name])
            writer.writerow(["Kategorie",     category])
            writer.writerow(["E-Mail",         email])
            writer.writerow(["Website",        website])
            writer.writerow(["Betreff",        betreff])
            writer.writerow(["E-Mail Text",    body])
            writer.writerow(["", ""])   # blank spacer

    print(f"✓ CSV exportiert → {OUTPUT_FILE}")
    print(f"  {len(businesses)} Unternehmen geschrieben.")
    print()
    print("WICHTIG: Ersetze '[DEIN NAME]' mit deinem echten Namen, bevor du die E-Mails versendest!")


if __name__ == "__main__":
    main()
