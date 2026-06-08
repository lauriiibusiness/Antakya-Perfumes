"""
scraper.py — Fetch Berlin businesses from OpenStreetMap via Overpass API.
Completely free, no API key needed.
"""

import time
import requests
from typing import Optional

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

CATEGORIES = {
    "Restaurant":       [('amenity', 'restaurant')],
    "Café":             [('amenity', 'cafe')],
    "Friseursalon":     [('shop', 'hairdresser')],
    "Barbershop":       [('shop', 'barber')],
    "Boutique":         [('shop', 'clothes'), ('shop', 'boutique')],
    "Fitnessstudio":    [('leisure', 'fitness_centre')],
    "Personal Trainer": [('sport', 'fitness')],
    "Nagelstudio":      [('shop', 'nail_salon')],
    "Tattoostudio":     [('shop', 'tattoo')],
    "Einzelhandel":     [('shop', 'gift'), ('shop', 'interior_decoration')],
}

MAX_PER_TAG = 10  # results per OSM tag query


def _build_query(key: str, value: str, limit: int) -> str:
    return f"""
[out:json][timeout:30];
area["name"="Berlin"]["admin_level"="4"]->.berlin;
(
  node["{key}"="{value}"]["name"](area.berlin);
  way["{key}"="{value}"]["name"](area.berlin);
);
out center {limit};
"""


def _extract(element: dict) -> dict:
    tags = element.get("tags", {})
    center = element.get("center", {})
    lat = center.get("lat") or element.get("lat", "")
    lon = center.get("lon") or element.get("lon", "")

    website = (
        tags.get("website") or
        tags.get("contact:website") or
        tags.get("url") or ""
    )
    email = (
        tags.get("email") or
        tags.get("contact:email") or ""
    )
    phone = (
        tags.get("phone") or
        tags.get("contact:phone") or ""
    )
    city = tags.get("addr:city", "Berlin")
    street = tags.get("addr:street", "")
    housenumber = tags.get("addr:housenumber", "")
    address = f"{street} {housenumber}, {city}".strip(", ")

    return {
        "name": tags.get("name", ""),
        "website": website,
        "email": email,
        "phone": phone,
        "address": address,
    }


def fetch_businesses(category: str, limit: int = MAX_PER_TAG) -> list[dict]:
    results = []
    seen_names: set[str] = set()

    for key, value in CATEGORIES.get(category, []):
        query = _build_query(key, value, limit)
        try:
            resp = requests.post(
                OVERPASS_URL,
                data={"data": query},
                timeout=40,
            )
            resp.raise_for_status()
            elements = resp.json().get("elements", [])
            for el in elements:
                biz = _extract(el)
                if not biz["name"] or biz["name"].lower() in seen_names:
                    continue
                seen_names.add(biz["name"].lower())
                results.append(biz)
        except Exception as exc:
            print(f"  Overpass error ({key}={value}): {exc}")
        time.sleep(1)  # be polite to the free API

    return results
