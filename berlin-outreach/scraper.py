"""
scraper.py — Fetch Berlin businesses using Google Places Text Search API.
"""

import requests
import time
from typing import Optional

CATEGORIES = {
    "Restaurant": ["restaurant Berlin Mitte", "restaurant Berlin Prenzlauer Berg"],
    "Café": ["café Berlin", "Kaffeehaus Berlin"],
    "Friseursalon": ["Friseursalon Berlin", "hair salon Berlin"],
    "Barbershop": ["barbershop Berlin", "Barbier Berlin"],
    "Boutique": ["Boutique Berlin", "Modeboutique Berlin"],
    "Fitnessstudio": ["Fitnessstudio Berlin", "gym Berlin"],
    "Personal Trainer": ["personal trainer Berlin"],
    "Nagelstudio": ["Nagelstudio Berlin", "nail salon Berlin"],
    "Tattoostudio": ["Tattoostudio Berlin"],
    "Einzelhandel": ["lokales Geschäft Berlin", "Laden Berlin Kreuzberg"],
}


def search_places(query: str, api_key: str, max_results: int = 8) -> list[dict]:
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    results = []
    params = {
        "query": query,
        "key": api_key,
        "language": "de",
        "region": "de",
    }

    while len(results) < max_results:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        status = data.get("status")

        if status == "ZERO_RESULTS":
            break
        if status != "OK":
            print(f"  API error [{status}]: {data.get('error_message', '')}")
            break

        for place in data.get("results", []):
            if len(results) >= max_results:
                break
            details = _get_place_details(place["place_id"], api_key)
            results.append({
                "name": place.get("name", ""),
                "address": place.get("formatted_address", ""),
                "website": details.get("website", ""),
                "phone": details.get("formatted_phone_number", ""),
                "place_id": place.get("place_id", ""),
            })
            time.sleep(0.3)

        next_token = data.get("next_page_token")
        if not next_token or len(results) >= max_results:
            break
        params = {"pagetoken": next_token, "key": api_key}
        time.sleep(2)  # required before next_page_token becomes valid

    return results


def _get_place_details(place_id: str, api_key: str) -> dict:
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "website,formatted_phone_number",
        "key": api_key,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        return resp.json().get("result", {})
    except Exception:
        return {}
