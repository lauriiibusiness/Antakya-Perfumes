#!/usr/bin/env python3
"""
Berlin Cold Email Outreach Tool
Pre-loaded with 51 verified Berlin businesses.
Generates personalised German cold emails, exports CSV, sends via Gmail SMTP.
"""

import csv
import hashlib
import smtplib
import getpass
import sys
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

SENDER_NAME  = "Ioana Laura Mocanu"
CSV_FILE     = "berlin_outreach.csv"
LOG_FILE     = "sent_log.txt"

# ─── Business data ─────────────────────────────────────────────────────────────
# All businesses are real Berlin small businesses found via web research.
# "has_website": True  → redesign pitch  |  False → new-website pitch
BUSINESSES = [
    # ── Restaurants ──────────────────────────────────────────────────────────
    {
        "name": "3 Schwestern",
        "category": "Restaurant",
        "email": "info@3schwestern.com",
        "website": "https://www.3schwestern.com",
        "has_website": True,
    },
    {
        "name": "EINS44",
        "category": "Restaurant",
        "email": "info@eins44.com",
        "website": "https://www.eins44.com",
        "has_website": True,
    },
    {
        "name": "NU Restaurant",
        "category": "Restaurant",
        "email": "info@nu-eat.de",
        "website": "https://www.nu-eat.de",
        "has_website": True,
    },
    {
        "name": "Dicke Wirtin",
        "category": "Restaurant",
        "email": "post@dicke-wirtin.de",
        "website": "https://dicke-wirtin.de",
        "has_website": True,
    },
    {
        "name": "Ausspanne",
        "category": "Restaurant",
        "email": "ausspanne@kastanienhof.berlin",
        "website": "https://www.deutsches-restaurant.berlin",
        "has_website": True,
    },
    {
        "name": "Ong Cat",
        "category": "Restaurant",
        "email": "info@ongcat-berlin.de",
        "website": "https://www.ongcat-berlin.de",
        "has_website": True,
    },
    {
        "name": "Vietland",
        "category": "Restaurant",
        "email": "info@vietland.de",
        "website": "https://vietland.de",
        "has_website": True,
    },
    # ── Cafés ────────────────────────────────────────────────────────────────
    {
        "name": "Café Anna Blume",
        "category": "Café",
        "email": "info@cafe-anna-blume.de",
        "website": "https://cafe-anna-blume.de",
        "has_website": True,
    },
    {
        "name": "Vilja Café",
        "category": "Café",
        "email": "kontakt@vilja-cafe.de",
        "website": "https://vilja-cafe.de",
        "has_website": True,
    },
    {
        "name": "Ataya Caffé",
        "category": "Café",
        "email": "info@atayacaffe.de",
        "website": "https://www.atayacaffe.de",
        "has_website": True,
    },
    {
        "name": "Café Liebling",
        "category": "Café",
        "email": "hello@cafeliebling.berlin",
        "website": "https://www.cafeliebling.berlin",
        "has_website": True,
    },
    {
        "name": "Café ILOstan",
        "category": "Café",
        "email": "info@cafeilostan.de",
        "website": "https://cafeilostan.de",
        "has_website": True,
    },
    {
        "name": "Saaldeck Café",
        "category": "Café",
        "email": "mail@saaldeck.de",
        "website": "https://www.saaldeck.de",
        "has_website": True,
    },
    {
        "name": "SowohlAlsAuch",
        "category": "Café",
        "email": "",
        "website": "https://www.sowohlalsauch.berlin",
        "has_website": True,
    },
    # ── Friseursalon ─────────────────────────────────────────────────────────
    {
        "name": "Said Rubaii Hairstyling",
        "category": "Friseursalon",
        "email": "contact@saidrubaii.com",
        "website": "https://saidrubaii.com",
        "has_website": True,
    },
    {
        "name": "Der Friseur Charlottenburg",
        "category": "Friseursalon",
        "email": "info@der-friseur-charlottenburg.de",
        "website": "https://www.der-friseur-charlottenburg.de",
        "has_website": True,
    },
    {
        "name": "Deine Lieblingsfriseure",
        "category": "Friseursalon",
        "email": "mail@lieblingsfriseure.de",
        "website": "https://lieblingsfriseure.de",
        "has_website": True,
    },
    # ── Barbershop ───────────────────────────────────────────────────────────
    {
        "name": "Barbabella Berlin",
        "category": "Barbershop",
        "email": "manoman@barbabella.berlin",
        "website": "https://barbabella.berlin",
        "has_website": True,
    },
    {
        "name": "MADO BarberShop",
        "category": "Barbershop",
        "email": "wael@mado-barbershop.com",
        "website": "https://mado-barbershop.com",
        "has_website": True,
    },
    {
        "name": "The Blade Barbercraft",
        "category": "Barbershop",
        "email": "hello@theblade.berlin",
        "website": "https://theblade.berlin",
        "has_website": True,
    },
    {
        "name": "The Barber Yard",
        "category": "Barbershop",
        "email": "",
        "website": "https://barber-yard.com",
        "has_website": True,
    },
    {
        "name": "Barber Shop Berlin",
        "category": "Barbershop",
        "email": "",
        "website": "https://www.barber-shop-berlin.de",
        "has_website": True,
    },
    # ── Boutique ─────────────────────────────────────────────────────────────
    {
        "name": "Rotation Boutique",
        "category": "Boutique",
        "email": "post@rotation-boutique.de",
        "website": "https://rotation-boutique.de",
        "has_website": True,
    },
    {
        "name": "Fête de la Boutique",
        "category": "Boutique",
        "email": "hello@fetedelaboutique.com",
        "website": "https://www.fetedelaboutique.com",
        "has_website": True,
    },
    {
        "name": "WiDDA Berlin",
        "category": "Boutique",
        "email": "shop@widda-berlin.de",
        "website": "https://shop.widda-berlin.de",
        "has_website": True,
    },
    {
        "name": "ME AND ME Berlin",
        "category": "Boutique",
        "email": "",
        "website": "https://www.me-and-me-berlin.de",
        "has_website": True,
    },
    # ── Fitnessstudio ─────────────────────────────────────────────────────────
    {
        "name": "FitnessCenter aTB",
        "category": "Fitnessstudio",
        "email": "fitnesscenter@web.de",
        "website": "https://fitnesscenter-atb.com",
        "has_website": True,
    },
    {
        "name": "Das Fitness Atelier",
        "category": "Fitnessstudio",
        "email": "info@dasfitnessatelier.de",
        "website": "https://www.dasfitnessatelier.de",
        "has_website": True,
    },
    {
        "name": "Becycle Berlin",
        "category": "Fitnessstudio",
        "email": "info@becycle.de",
        "website": "https://www.becycle.de",
        "has_website": True,
    },
    # ── Personal Trainer ─────────────────────────────────────────────────────
    {
        "name": "Das Trainingslager",
        "category": "Personal Trainer",
        "email": "info@dastrainingslager.de",
        "website": "https://dastrainingslager.de",
        "has_website": True,
    },
    {
        "name": "Andreas Heumann Personal Training",
        "category": "Personal Trainer",
        "email": "",
        "website": "https://heumann-personaltraining.berlin",
        "has_website": True,
    },
    {
        "name": "Berlin Personal Training",
        "category": "Personal Trainer",
        "email": "info@berlin-personal-training.de",
        "website": "https://www.berlin-personal-training.de",
        "has_website": True,
    },
    {
        "name": "Mary aus Moabit",
        "category": "Personal Trainer",
        "email": "info@maryausmoabit.com",
        "website": "https://www.maryausmoabit.com",
        "has_website": True,
    },
    {
        "name": "RYZZFIT Berlin",
        "category": "Personal Trainer",
        "email": "info@ryzzfit.com",
        "website": "https://ryzzfit.com",
        "has_website": True,
    },
    # ── Nagelstudio ──────────────────────────────────────────────────────────
    {
        "name": "Angel Nails Berlin",
        "category": "Nagelstudio",
        "email": "info@angelnailsonline.de",
        "website": "https://myangelnails.de",
        "has_website": True,
    },
    {
        "name": "Studio 358 Nails",
        "category": "Nagelstudio",
        "email": "hello@studio358.berlin",
        "website": "https://studio358.de",
        "has_website": True,
    },
    {
        "name": "Thanh Dat Nagelstudio",
        "category": "Nagelstudio",
        "email": "",
        "website": "https://www.thanhdat-nagelstudio.de",
        "has_website": True,
    },
    {
        "name": "Unique Nail Berlin",
        "category": "Nagelstudio",
        "email": "",
        "website": "https://www.unique-nail.com",
        "has_website": True,
    },
    # ── Tattoo Studio ─────────────────────────────────────────────────────────
    {
        "name": "OMEN Tattoo Berlin",
        "category": "Tattoo Studio",
        "email": "info@omentattoo.de",
        "website": "https://omentattoo.de",
        "has_website": True,
    },
    {
        "name": "Inklabs Tattoo Berlin",
        "category": "Tattoo Studio",
        "email": "info@inklabs.de",
        "website": "https://www.inklabs.de",
        "has_website": True,
    },
    {
        "name": "Blut und Eisen Tattoo",
        "category": "Tattoo Studio",
        "email": "info@blutundeisen.de",
        "website": "https://blutundeisen.de",
        "has_website": True,
    },
    {
        "name": "Mugshot Tattoo Berlin",
        "category": "Tattoo Studio",
        "email": "info@mugshot-tattoo.com",
        "website": "https://www.mugshot-tattoo.com",
        "has_website": True,
    },
    # ── Einzelhandel ─────────────────────────────────────────────────────────
    {
        "name": "R.S.V.P. Berlin",
        "category": "Einzelhandel",
        "email": "info@rsvp-berlin.de",
        "website": "https://rsvp-berlin.de",
        "has_website": True,
    },
    {
        "name": "Sommernest Concept Store",
        "category": "Einzelhandel",
        "email": "info@sommernest.de",
        "website": "https://sommernest.de",
        "has_website": True,
    },
    {
        "name": "Die kleine Gesellschaft",
        "category": "Einzelhandel",
        "email": "info@kleinegesellschaft.de",
        "website": "https://kleinegesellschaft.com",
        "has_website": True,
    },
    {
        "name": "Planty Skies Berlin",
        "category": "Einzelhandel",
        "email": "",
        "website": "https://www.plantyskies.com",
        "has_website": True,
    },
    {
        "name": "NOVeL Concept Store",
        "category": "Einzelhandel",
        "email": "support@novelberlin.de",
        "website": "https://www.novelberlin.de",
        "has_website": True,
    },
    {
        "name": "das goodshaus",
        "category": "Einzelhandel",
        "email": "contact@goodshaus.com",
        "website": "https://www.goodshaus.com",
        "has_website": True,
    },
    {
        "name": "Kornblume Floristik",
        "category": "Einzelhandel",
        "email": "info@lindes-kornblume.de",
        "website": "https://www.lindes-kornblume.de",
        "has_website": True,
    },
    {
        "name": "Frau Rose Floristik",
        "category": "Einzelhandel",
        "email": "info@fraurose.de",
        "website": "https://www.fraurose.de",
        "has_website": True,
    },
    {
        "name": "Blumenbett Berlin",
        "category": "Einzelhandel",
        "email": "info@blumenbett.de",
        "website": "https://www.blumenbett.de",
        "has_website": True,
    },
]

# ─── Email templates ────────────────────────────────────────────────────────────
# 5 redesign templates (all businesses have websites)
TEMPLATES_WEBSITE = [
    """\
Hallo {name}-Team,

ich bin neulich online auf {cat_phrase} in Berlin gestoßen – wirklich beeindruckend! Beim Besuch eurer Website ist mir aufgefallen, dass das Design etwas in die Jahre gekommen ist und auf dem Smartphone nicht optimal aussieht.

In Berlin suchen über 70 % der Kunden über ihr Handy – eine moderne, mobiloptimierte Website kann täglich neue Kunden bringen.

Ich biete professionelle Redesigns ab €500–800 an, fertig in 1–2 Wochen.

Hätte ich 15 Minuten für ein kostenloses Erstgespräch? Einfach antworten – ich freue mich!

Herzliche Grüße aus Berlin,
{sender}""",

    """\
Hallo {name},

kurze Nachricht: Ich bin Webdesignerin und habe eure Seite angeschaut. Das Konzept ist wirklich sympathisch – aber das Design verdient ein frisches Update, vor allem für Handy-Nutzer in Berlin.

Ein modernes Redesign (ab €500–800, fertig in 2 Wochen) hilft euch, online mehr Kunden zu gewinnen.

Würdet ihr kurz 15 Minuten für ein kostenloses Erstgespräch einplanen? Einfach auf diese Mail antworten!

Liebe Grüße,
{sender}""",

    """\
Hi {name}-Team,

ich habe {cat_phrase} in Berlin entdeckt und direkt eure Website besucht – tolles Konzept! Mir ist aufgefallen, dass die Seite auf dem Handy noch nicht ganz ideal lädt und das Design etwas veraltet wirkt.

Da in Berlin fast alles über mobile Suche läuft, kann das potenzielle Neukunden kosten.

Ich biete schnelle, professionelle Redesigns ab €500–800 an – in 2 Wochen fertig und mobiloptimiert.

Habt ihr Lust auf 15 Minuten kostenlosen Call? Einfach antworten!

Viele Grüße aus Berlin,
{sender}""",

    """\
Hallo {name}-Team,

ich bin Webdesignerin und habe eure Seite aufgerufen – {cat_phrase} in Berlin, das gefällt mir! Eine Sache: Das Design ist noch nicht vollständig für Smartphones optimiert, und gerade weil viele Berliner über ihr Handy suchen, kann das Kunden kosten.

Ein Redesign gibt's bei mir ab €500–800, fertig in 2 Wochen.

Hätte ich 15 Minuten für einen kostenlosen Kennenlern-Call? Einfach hier antworten!

Herzliche Grüße,
{sender}""",

    """\
Hallo {name},

ich bin in Berlin auf {cat_phrase} aufmerksam geworden und habe sofort eure Website besucht. Das Konzept ist wirklich schön! Was mir aufgefallen ist: Das Design wirkt an manchen Stellen noch etwas veraltet – besonders auf dem Handy könnte es frischer und schneller sein.

In einer Stadt wie Berlin, wo Kunden täglich online suchen, ist eine moderne Website ein echter Vorteil.

Ich biete Redesigns ab €500–800 an – 2 Wochen Lieferzeit. 15 Minuten kostenloses Gespräch?

Einfach antworten – ich freue mich!

Viele Grüße aus Berlin,
{sender}""",
]

# Templates when no website exists
TEMPLATES_NO_WEBSITE = [
    """\
Hallo {name}-Team,

beim Stöbern online bin ich auf {cat_phrase} in Berlin gestoßen – wirklich schön! Mir ist aufgefallen, dass ihr noch keine eigene Website habt.

In Berlin suchen die meisten Kunden zuerst bei Google, bevor sie irgendwo hingehen. Mit einer professionellen Landingpage (ab €350–500, fertig in 1–2 Wochen) seid ihr sofort sichtbar.

Hätte ich kurz 15 Minuten für ein kostenloses Gespräch? Einfach antworten!

Herzliche Grüße aus Berlin,
{sender}""",

    """\
Hi {name},

ich habe {cat_phrase} in Berlin entdeckt – aber eine eigene Website fehlt noch.

Das ist schade, denn viele Berliner Kunden suchen heute zuerst im Internet. Mit einer schlanken Landingpage (ab €350) seid ihr sofort bei Google sichtbar – fertig in 1–2 Wochen.

Kurze Frage: Hätte jemand 15 Minuten für einen kostenlosen Call? Einfach antworten!

Liebe Grüße,
{sender}""",
]


def pick_template(name: str, has_website: bool) -> str:
    pool = TEMPLATES_WEBSITE if has_website else TEMPLATES_NO_WEBSITE
    idx  = int(hashlib.md5(name.encode()).hexdigest(), 16) % len(pool)
    return pool[idx]


def _cat_article(cat: str) -> str:
    """Return German article+category pair for natural phrasing."""
    mapping = {
        "Restaurant":     "euer Restaurant",
        "Café":           "euer Café",
        "Friseursalon":   "euren Friseursalon",
        "Barbershop":     "euren Barbershop",
        "Boutique":       "eure Boutique",
        "Fitnessstudio":  "euer Fitnessstudio",
        "Personal Trainer": "euer Personal-Training-Angebot",
        "Nagelstudio":    "euer Nagelstudio",
        "Tattoo Studio":  "euer Tattoo-Studio",
        "Einzelhandel":   "euren Laden",
    }
    return mapping.get(cat, f"euer {cat}")


def generate_email(biz: dict) -> str:
    tpl = pick_template(biz["name"], biz["has_website"])
    return tpl.format(
        name       = biz["name"],
        cat_phrase = _cat_article(biz["category"]),
        sender     = SENDER_NAME,
    )


def export_csv(businesses: list[dict]) -> str:
    rows = []
    for b in businesses:
        rows.append({
            "Business Name": b["name"],
            "Category":      b["category"],
            "Email":         b["email"],
            "Website":       b["website"],
            "Email Body":    generate_email(b),
        })

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Business Name","Category","Email","Website","Email Body"])
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"CSV saved → {CSV_FILE}  ({len(rows)} rows)")
    return CSV_FILE


def send_emails(rows: list[dict], gmail_address: str, app_password: str) -> tuple[list, list]:
    to_send = [r for r in rows if r["Email"].strip()]
    logger.info(f"Businesses with email addresses: {len(to_send)}")

    sent, failed = [], []

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(gmail_address, app_password)
        logger.info("Gmail login successful")
    except Exception as e:
        logger.error(f"Gmail login failed: {e}")
        return sent, [{"error": str(e)}]

    for i, row in enumerate(to_send, 1):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Kurze Frage zu {row['Business Name']}"
            msg["From"]    = f"{SENDER_NAME} <{gmail_address}>"
            msg["To"]      = row["Email"]
            msg.attach(MIMEText(row["Email Body"], "plain", "utf-8"))

            server.sendmail(gmail_address, row["Email"], msg.as_string())

            sent.append(row["Email"])
            logger.info(f"[{i}/{len(to_send)}] ✓  {row['Business Name']} → {row['Email']}")

            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"SENT | {row['Business Name']} | {row['Email']} | {row['Category']}\n")

            if i < len(to_send):
                delay = random.uniform(30, 60)
                logger.info(f"   Waiting {delay:.0f}s …")
                time.sleep(delay)

        except Exception as e:
            failed.append({"name": row["Business Name"], "email": row["Email"], "error": str(e)})
            logger.error(f"[{i}/{len(to_send)}] ✗  {row['Business Name']}: {e}")
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"FAILED | {row['Business Name']} | {row['Email']} | {e}\n")

    server.quit()
    return sent, failed


if __name__ == "__main__":
    print("=" * 60)
    print(f" Berlin Cold Email Outreach — {len(BUSINESSES)} businesses")
    print(f" Signed as: {SENDER_NAME}")
    print("=" * 60)

    # ── Step 1: generate emails + export CSV ──────────────────────────────
    print("\n[1/2] Generating emails and exporting CSV …")
    rows = []
    for b in BUSINESSES:
        rows.append({
            "Business Name": b["name"],
            "Category":      b["category"],
            "Email":         b["email"],
            "Website":       b["website"],
            "Email Body":    generate_email(b),
        })

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Business Name","Category","Email","Website","Email Body"])
        writer.writeheader()
        writer.writerows(rows)

    with_email    = sum(1 for r in rows if r["Email"])
    without_email = len(rows) - with_email
    print(f"   Total businesses : {len(rows)}")
    print(f"   With email       : {with_email}")
    print(f"   Without email    : {without_email} (in CSV for manual outreach)")
    print(f"   CSV saved        : {CSV_FILE}")

    # ── Step 2: send emails ────────────────────────────────────────────────
    print("\n[2/2] Email sending")
    if with_email == 0:
        print("No email addresses — review CSV manually. Exiting.")
        sys.exit(0)

    gmail_address = input("\nEnter your Gmail address: ").strip()
    app_password  = getpass.getpass("Enter your Gmail App Password (16 chars, no spaces): ").strip()

    confirm = input(
        f"\nAbout to send {with_email} emails from {gmail_address}.\n"
        "Type 'yes' to confirm, anything else to cancel: "
    ).strip().lower()

    if confirm != "yes":
        print(f"\nCancelled. CSV is ready at: {CSV_FILE}")
        sys.exit(0)

    sent, failed = send_emails(rows, gmail_address, app_password)

    print(f"\n{'='*60}")
    print(f"Done!  Sent: {len(sent)}  |  Failed: {len(failed)}")
    if failed:
        print("\nFailed deliveries:")
        for f in failed:
            if "email" in f:
                print(f"  - {f['name']} ({f['email']}): {f['error']}")
    print(f"\nFull log → {LOG_FILE}")
