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

# ─── Batch 2 businesses (100 additional Berlin businesses) ─────────────────────
BUSINESSES_BATCH2 = [
    # ── Restaurant (15) ──────────────────────────────────────────────────────
    {"name": "Restaurant Friedrich", "category": "Restaurant", "email": "info@restaurantfriedrich.de", "website": "https://restaurantfriedrich.de", "has_website": True},
    {"name": "Jäger & Lustig", "category": "Restaurant", "email": "info@jaegerundlustig.de", "website": "https://jaegerundlustig.de", "has_website": True},
    {"name": "Bollenpiepe", "category": "Restaurant", "email": "info@bollenpiepe.de", "website": "https://bollenpiepe.de", "has_website": True},
    {"name": "QADMOUS", "category": "Restaurant", "email": "info@qadmous.de", "website": "https://qadmous.de", "has_website": True},
    {"name": "Speisegaststätte PILA", "category": "Restaurant", "email": "info@restaurant-pila.de", "website": "https://restaurant-pila.de", "has_website": True},
    {"name": "Gasthaus Alt Wien", "category": "Restaurant", "email": "service@altwien-berlin.de", "website": "https://altwien-berlin.de", "has_website": True},
    {"name": "Nußbaumerin", "category": "Restaurant", "email": "info@nussbaumerin.de", "website": "https://nussbaumerin.de", "has_website": True},
    {"name": "Bottega Seppel", "category": "Restaurant", "email": "sitzenbleiben@bottega-seppel.de", "website": "https://bottega-seppel.de", "has_website": True},
    {"name": "Die Garbe", "category": "Restaurant", "email": "info@diegarbe.de", "website": "https://diegarbe.de", "has_website": True},
    {"name": "Vedis Indian Restaurant", "category": "Restaurant", "email": "info@vedis.berlin", "website": "https://vedis.berlin", "has_website": True},
    {"name": "Best Friends Kreuzberg", "category": "Restaurant", "email": "info@bestfriends-kreuzberg.de", "website": "https://bestfriends-kreuzberg.de", "has_website": True},
    {"name": "Kreuzburger", "category": "Restaurant", "email": "info@kreuzburger.de", "website": "https://kreuzburger.de", "has_website": True},
    {"name": "Restaurant Amera", "category": "Restaurant", "email": "info@restaurant-amera.de", "website": "https://restaurant-amera.de", "has_website": True},
    {"name": "Restaurant Renger-Patzsch", "category": "Restaurant", "email": "info@renger-patzsch.com", "website": "https://renger-patzsch.com", "has_website": True},
    {"name": "Restaurant PALERMO Weissensee", "category": "Restaurant", "email": "info@palermo-restaurant.de", "website": "https://palermo-restaurant.de", "has_website": True},
    # ── Café (12) ────────────────────────────────────────────────────────────
    {"name": "Café Cralle", "category": "Café", "email": "cafecralle@riseup.net", "website": "https://cafecralle.de", "has_website": True},
    {"name": "THE CAFE Kreuzberg", "category": "Café", "email": "info@thecafe.berlin", "website": "https://thecafe.berlin", "has_website": True},
    {"name": "Café Cutie Pie", "category": "Café", "email": "info@cutiepie-berlin.de", "website": "https://cutiepie-berlin.de", "has_website": True},
    {"name": "LAAX Berlin", "category": "Café", "email": "kontakt@laax-berlin.de", "website": "https://laax-berlin.de", "has_website": True},
    {"name": "Café Augusta", "category": "Café", "email": "info@cafeaugusta.de", "website": "https://cafeaugusta.de", "has_website": True},
    {"name": "Café Blume Neukölln", "category": "Café", "email": "post@blumeberlin.de", "website": "https://blumeberlin.de", "has_website": True},
    {"name": "Café do Brasil", "category": "Café", "email": "mail@cafe-do-brasil.de", "website": "https://cafe-do-brasil.de", "has_website": True},
    {"name": "P-Berg Coffee", "category": "Café", "email": "info@p-berg-coffee.de", "website": "https://p-berg-coffee.de", "has_website": True},
    {"name": "Unser Café Berlin", "category": "Café", "email": "hi@unser-cafe-berlin.de", "website": "https://unser-cafe-berlin.de", "has_website": True},
    {"name": "Schwarzes Café Berlin", "category": "Café", "email": "info@schwarzescafe-berlin.de", "website": "https://schwarzescafe-berlin.de", "has_website": True},
    {"name": "KuchenZeit Berlin", "category": "Café", "email": "info@kuchenzeit.com", "website": "https://kuchenzeit.com", "has_website": True},
    {"name": "Café Friedrichs", "category": "Café", "email": "info@cafefriedrichs.com", "website": "https://cafefriedrichs.com", "has_website": True},
    # ── Friseursalon (10) ────────────────────────────────────────────────────
    {"name": "NeoBerlin Friseur", "category": "Friseursalon", "email": "salon@neoberlin.com", "website": "https://neoberlin.com", "has_website": True},
    {"name": "HARMS Friseure", "category": "Friseursalon", "email": "info@harms-friseure-berlin.de", "website": "https://harms-friseure-berlin.de", "has_website": True},
    {"name": "HD Performance Hairstudio", "category": "Friseursalon", "email": "info@hdperformance.de", "website": "https://hdperformance-hairstudio.de", "has_website": True},
    {"name": "Art Cut", "category": "Friseursalon", "email": "info@artcut.eu", "website": "https://artcut.eu", "has_website": True},
    {"name": "Kiezschnitt", "category": "Friseursalon", "email": "kiezschnitt-berlin@hotmail.de", "website": "https://kiezschnitt.com", "has_website": True},
    {"name": "Gabriela Goldbeck Friseur", "category": "Friseursalon", "email": "Friseur@gabrielagoldbeck.de", "website": "https://gabrielagoldbeck.de", "has_website": True},
    {"name": "Friseur Team Sandy Rank", "category": "Friseursalon", "email": "info@friseurteam-sandy.de", "website": "https://friseurteam-sandy.de", "has_website": True},
    {"name": "Harry Huth Friseure", "category": "Friseursalon", "email": "harryhuthfriseure@web.de", "website": "https://harryhuthfriseure.com", "has_website": True},
    {"name": "Frank Meiners Friseur", "category": "Friseursalon", "email": "info@friseur-frank-meiners.de", "website": "https://friseur-frank-meiners.de", "has_website": True},
    {"name": "Salon Bredow", "category": "Friseursalon", "email": "salonbredow@aol.com", "website": "https://salonbredow.de", "has_website": True},
    # ── Barbershop (8) ───────────────────────────────────────────────────────
    {"name": "Barbers Berlin", "category": "Barbershop", "email": "info@berlin-barbers.com", "website": "https://berlin-barbers.com", "has_website": True},
    {"name": "Benny Barbers", "category": "Barbershop", "email": "info@bennybarbers.com", "website": "https://bennybarbers.com", "has_website": True},
    {"name": "Barber Anil", "category": "Barbershop", "email": "info@barber-anil.de", "website": "https://barber-anil.de", "has_website": True},
    {"name": "SAWA BARBER", "category": "Barbershop", "email": "sawabarber@gmail.com", "website": "https://sawabarber.de", "has_website": True},
    {"name": "Barber Remz", "category": "Barbershop", "email": "barberremz@gmx.de", "website": "https://berlin-barber.de", "has_website": True},
    {"name": "KaNa Barbers of Berlin", "category": "Barbershop", "email": "info@barbers-of-berlin.de", "website": "https://barbers-of-berlin.de", "has_website": True},
    {"name": "Beardy Boys Berlin", "category": "Barbershop", "email": "info@beardy-boys.de", "website": "https://beardy-boys.de", "has_website": True},
    {"name": "Skillz Studio Berlin", "category": "Barbershop", "email": "skillz.studio@yahoo.com", "website": "https://skillz-studio.de", "has_website": True},
    # ── Boutique (9) ─────────────────────────────────────────────────────────
    {"name": "DearGoods Berlin", "category": "Boutique", "email": "berlin@deargoods.com", "website": "https://deargoods.com", "has_website": True},
    {"name": "Glamorous Berlin", "category": "Boutique", "email": "info@glamorous-berlin.de", "website": "https://glamorous-berlin.de", "has_website": True},
    {"name": "City Look Rottleb", "category": "Boutique", "email": "info@rottleb-city-look.de", "website": "https://rottleb-city-look.de", "has_website": True},
    {"name": "PECCATO Berlin", "category": "Boutique", "email": "berlin@peccato.de", "website": "https://peccato.de", "has_website": True},
    {"name": "supermarché Berlin", "category": "Boutique", "email": "info@supermarche-berlin.de", "website": "https://supermarche-berlin.de", "has_website": True},
    {"name": "LOVECO", "category": "Boutique", "email": "hello@loveco-shop.de", "website": "https://loveco-shop.de", "has_website": True},
    {"name": "KONK Berlin", "category": "Boutique", "email": "mail@konk-berlin.de", "website": "https://konk-berlin.de", "has_website": True},
    {"name": "Lenas Lovely Vintage", "category": "Boutique", "email": "hello@lenaslovelyvintage.com", "website": "https://lenaslovelyvintage.com", "has_website": True},
    {"name": "Gewandhaus Secondhand", "category": "Boutique", "email": "info@gewandhaus-verleih.de", "website": "https://gewandhaus-secondhand.de", "has_website": True},
    # ── Fitnessstudio (6) ─────────────────────────────────────────────────────
    {"name": "Casa Flow Studios", "category": "Fitnessstudio", "email": "hi@casaflow.de", "website": "https://casaflow.de", "has_website": True},
    {"name": "Rolands Fitness Lab", "category": "Fitnessstudio", "email": "info@rolandsfitnesslab.de", "website": "https://rolandsfitnesslab.de", "has_website": True},
    {"name": "Hi Studios", "category": "Fitnessstudio", "email": "sayhi@hiyogaberlin.de", "website": "https://hiyoga.studio", "has_website": True},
    {"name": "Formwandler", "category": "Fitnessstudio", "email": "info@formwandler.de", "website": "https://formwandler.de", "has_website": True},
    {"name": "NOIR Boutique Gym", "category": "Fitnessstudio", "email": "info@noirtherapy.de", "website": "https://noirboutiquegym.de", "has_website": True},
    {"name": "CrossFit Aorta", "category": "Fitnessstudio", "email": "info@crossfitaorta.com", "website": "https://crossfitaorta.com", "has_website": True},
    # ── Personal Trainer (8) ─────────────────────────────────────────────────
    {"name": "Sportsfreund Berlin", "category": "Personal Trainer", "email": "kontakt@sportsfreund-berlin.de", "website": "https://sportsfreund-berlin.de", "has_website": True},
    {"name": "Royal Private Coach Berlin", "category": "Personal Trainer", "email": "info@royalprivatecoach.com", "website": "https://berlin.royalprivatecoach.de", "has_website": True},
    {"name": "BEARBOX Berlin", "category": "Personal Trainer", "email": "hallo@bearbox.berlin", "website": "https://bearbox.berlin", "has_website": True},
    {"name": "Marcel Dyszkant", "category": "Personal Trainer", "email": "marceldyszkant@yahoo.de", "website": "https://personaltrainer-charlottenburg.de", "has_website": True},
    {"name": "Mathis Wagenbach Haltungsarchitekt", "category": "Personal Trainer", "email": "mathis.wagenbach@haltungsarchitekt.de", "website": "https://haltungsarchitekt.de", "has_website": True},
    {"name": "Tayfun Berlin Personal Trainer", "category": "Personal Trainer", "email": "service@berlin-personaltrainer.de", "website": "https://berlin-personaltrainer.de", "has_website": True},
    {"name": "Berlin Personaltraining", "category": "Personal Trainer", "email": "info@berlin-personaltraining.de", "website": "https://berlin-personaltraining.de", "has_website": True},
    {"name": "Diermann Personal Training", "category": "Personal Trainer", "email": "info@personaltrainerinberlin.de", "website": "https://personaltrainerinberlin.de", "has_website": True},
    # ── Nagelstudio (8) ──────────────────────────────────────────────────────
    {"name": "Conceptnails", "category": "Nagelstudio", "email": "hello@conceptnails.de", "website": "https://conceptnails.de", "has_website": True},
    {"name": "Beauty Nails Charlottenburg", "category": "Nagelstudio", "email": "beautynails80@gmail.com", "website": "https://beautynailscharlottenburg.de", "has_website": True},
    {"name": "Nail Art Mitte", "category": "Nagelstudio", "email": "kontakt@nail-art-mitte.de", "website": "https://nail-art-mitte.de", "has_website": True},
    {"name": "Allegra Nagelatelier", "category": "Nagelstudio", "email": "info@allegra-nagelatelier.de", "website": "https://allegra-nagelatelier.de", "has_website": True},
    {"name": "Die Ecke Nails", "category": "Nagelstudio", "email": "info@dieeckenails.de", "website": "https://dieeckenails.de", "has_website": True},
    {"name": "Omni Nails", "category": "Nagelstudio", "email": "Omninailstph9495@gmail.com", "website": "https://omninails.de", "has_website": True},
    {"name": "Hauptstadt-Nails", "category": "Nagelstudio", "email": "info@hauptstadt-nails.de", "website": "https://hauptstadt-nails.de", "has_website": True},
    {"name": "Finest Nails Berlin", "category": "Nagelstudio", "email": "info@finestnails.de", "website": "https://finestnails.de", "has_website": True},
    # ── Tattoo Studio (11) ────────────────────────────────────────────────────
    {"name": "LSD Tattoo", "category": "Tattoo Studio", "email": "info@lsd-tattoo.de", "website": "https://lsd-tattoo.de", "has_website": True},
    {"name": "Tiba Tattoo", "category": "Tattoo Studio", "email": "info@tibatattoo.de", "website": "https://tibatattoo.com", "has_website": True},
    {"name": "Usee Tattoo", "category": "Tattoo Studio", "email": "hello@useetattoo.de", "website": "https://useetattoo.com", "has_website": True},
    {"name": "AUTARK Tattoo", "category": "Tattoo Studio", "email": "info@tattoo-studio.berlin", "website": "https://tattoo-studio.berlin", "has_website": True},
    {"name": "Life Story Tattoo", "category": "Tattoo Studio", "email": "info@lifestorytattoo.de", "website": "https://lifestorytattoo.de", "has_website": True},
    {"name": "Moving Lines Tattoo", "category": "Tattoo Studio", "email": "info@movinglinestattoo.com", "website": "https://movinglinestattoo.de", "has_website": True},
    {"name": "OEK Factory Tattoo", "category": "Tattoo Studio", "email": "info@oekfactory.com", "website": "https://oekfactory.com", "has_website": True},
    {"name": "Studio Sturmfrei", "category": "Tattoo Studio", "email": "studiosturmfrei@gmail.com", "website": "https://studiosturmfrei.com", "has_website": True},
    {"name": "Erntezeit Tattoostudio", "category": "Tattoo Studio", "email": "info@erntezeit-taetowierungen.de", "website": "https://erntezeit-taetowierungen.de", "has_website": True},
    {"name": "CNX Tattoo Berlin", "category": "Tattoo Studio", "email": "cnxtattoo@gmail.com", "website": "https://cnxtattoo.com", "has_website": True},
    {"name": "TintenStrich Tattoo", "category": "Tattoo Studio", "email": "anfrage@tintenstrich-tattoo.de", "website": "https://tintenstrich-tattoo.de", "has_website": True},
    # ── Einzelhandel (13) ────────────────────────────────────────────────────
    {"name": "Die Buchkönigin", "category": "Einzelhandel", "email": "hallo@buchkoenigin.de", "website": "https://buchkoenigin.de", "has_website": True},
    {"name": "Neunest", "category": "Einzelhandel", "email": "hello@neunest.de", "website": "https://neunest.de", "has_website": True},
    {"name": "Flori by Tiffany", "category": "Einzelhandel", "email": "info@event-by-tiffany.de", "website": "https://flori-by-tiffany.de", "has_website": True},
    {"name": "LangerBlomqvist", "category": "Einzelhandel", "email": "shop@langer-blomqvist.de", "website": "https://langer-blomqvist.de", "has_website": True},
    {"name": "Buchhandlung oh21", "category": "Einzelhandel", "email": "kontakt@oh21.de", "website": "https://oh21.de", "has_website": True},
    {"name": "Extra-Buch", "category": "Einzelhandel", "email": "info@extra-buch.de", "website": "https://extra-buch.de", "has_website": True},
    {"name": "Otherland Buchhandlung", "category": "Einzelhandel", "email": "service@otherland-berlin.de", "website": "https://otherland-berlin.de", "has_website": True},
    {"name": "Ratzekatz", "category": "Einzelhandel", "email": "info@ratzekatz.de", "website": "https://ratzekatz.de", "has_website": True},
    {"name": "Majabell Kids Concept", "category": "Einzelhandel", "email": "info@majabell.de", "website": "https://majabell.de", "has_website": True},
    {"name": "Buchhandlung Paul und Paula", "category": "Einzelhandel", "email": "info@buchpaula.de", "website": "https://buchpaula.de", "has_website": True},
    {"name": "MUDDASTADT Berlin", "category": "Einzelhandel", "email": "info@muddastadt-berlin.de", "website": "https://muddastadt-berlin.de", "has_website": True},
    {"name": "Landbeck Keramik", "category": "Einzelhandel", "email": "kontakt@landbeck-keramik.de", "website": "https://landbeck-keramik.de", "has_website": True},
    {"name": "Clayers Collective", "category": "Einzelhandel", "email": "hello@clayerscollective.de", "website": "https://clayerscollective.de", "has_website": True},
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
