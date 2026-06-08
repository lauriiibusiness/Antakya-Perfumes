"""
main.py — Orchestrate the full Berlin outreach pipeline.

Steps:
  1. Scrape businesses from Google Places API
  2. Find email addresses on their websites
  3. Generate personalized German cold emails
  4. Export berlin_outreach.csv

Then run:  python sender.py [--dry-run]
"""

import csv
import os
import sys
import time

from dotenv import load_dotenv

from scraper import CATEGORIES, search_places
from email_finder import find_email
from email_generator import generate_email, get_subject

load_dotenv()

OUTPUT_CSV = "berlin_outreach.csv"
MAX_PER_QUERY = 8  # Places API returns max 20, we cap here


def main() -> None:
    api_key = os.getenv("GOOGLE_PLACES_API_KEY", "").strip()
    if not api_key:
        sys.exit("Error: Set GOOGLE_PLACES_API_KEY in .env")

    # ── 1. Scrape businesses ─────────────────────────────────────────────────
    all_businesses: list[dict] = []
    seen: set[str] = set()

    for category, queries in CATEGORIES.items():
        print(f"\n=== {category} ===")
        for query in queries:
            results = search_places(query, api_key, max_results=MAX_PER_QUERY)
            for biz in results:
                key = biz["name"].lower().strip()
                if key in seen:
                    continue
                seen.add(key)
                biz["category"] = category
                all_businesses.append(biz)
                print(f"  + {biz['name']:<40} website: {biz.get('website') or '—'}")

    print(f"\n{'─'*60}")
    print(f"Total unique businesses found: {len(all_businesses)}")

    # ── 2. Find email addresses ──────────────────────────────────────────────
    print("\nSearching for email addresses on websites…")
    for i, biz in enumerate(all_businesses, 1):
        if biz.get("website"):
            print(f"  [{i}/{len(all_businesses)}] {biz['name']}… ", end="", flush=True)
            email = find_email(biz["website"])
            biz["email"] = email or ""
            print(email or "not found")
        else:
            biz["email"] = ""
            print(f"  [{i}/{len(all_businesses)}] {biz['name']} — no website")
        time.sleep(0.8)

    # ── 3. Generate emails ───────────────────────────────────────────────────
    print("\nGenerating personalized emails…")
    for biz in all_businesses:
        has_website = bool(biz.get("website"))
        biz["email_body"] = generate_email(biz["name"], biz["category"], has_website)
        biz["subject"] = get_subject(biz["name"], has_website)

    # ── 4. Export CSV ────────────────────────────────────────────────────────
    fieldnames = ["Business Name", "Category", "Email", "Website",
                  "Subject", "Email Body", "Address", "Phone"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for biz in all_businesses:
            writer.writerow({
                "Business Name": biz.get("name", ""),
                "Category":      biz.get("category", ""),
                "Email":         biz.get("email", ""),
                "Website":       biz.get("website", ""),
                "Subject":       biz.get("subject", ""),
                "Email Body":    biz.get("email_body", ""),
                "Address":       biz.get("address", ""),
                "Phone":         biz.get("phone", ""),
            })

    with_email = sum(1 for b in all_businesses if b.get("email"))
    no_email = len(all_businesses) - with_email

    print(f"\n{'='*60}")
    print(f"Saved {len(all_businesses)} businesses to {OUTPUT_CSV}")
    print(f"  {with_email} have email addresses  ← ready to send")
    print(f"  {no_email} without emails           ← email body still generated")
    print(f"\nNext steps:")
    print(f"  Preview:  python sender.py --dry-run")
    print(f"  Send:     python sender.py")


if __name__ == "__main__":
    main()
