"""
main.py — Orchestrate the full Berlin outreach pipeline.

Steps:
  1. Scrape businesses from OpenStreetMap (free, no API key)
  2. Find email addresses on their websites
  3. Generate personalized German cold emails
  4. Export berlin_outreach.csv

Then run:  python sender.py [--dry-run]
"""

import csv
import time

from scraper import CATEGORIES, fetch_businesses
from email_finder import find_email
from email_generator import generate_email, get_subject

OUTPUT_CSV = "berlin_outreach.csv"


def main() -> None:
    all_businesses: list[dict] = []
    seen: set[str] = set()

    # ── 1. Scrape businesses ─────────────────────────────────────────────────
    for category in CATEGORIES:
        print(f"\n=== {category} ===")
        results = fetch_businesses(category)
        for biz in results:
            key = biz["name"].lower().strip()
            if key in seen:
                continue
            seen.add(key)
            biz["category"] = category
            all_businesses.append(biz)
            print(f"  + {biz['name']:<40} website: {biz.get('website') or '—'}")

    print(f"\n{'─'*60}")
    print(f"Total unique businesses: {len(all_businesses)}")

    # ── 2. Find emails on websites ───────────────────────────────────────────
    print("\nSearching for email addresses on websites…")
    for i, biz in enumerate(all_businesses, 1):
        # OSM sometimes already has the email in tags
        if biz.get("email"):
            print(f"  [{i}/{len(all_businesses)}] {biz['name']} → {biz['email']} (from OSM)")
            continue

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
    print(f"\n{'='*60}")
    print(f"Saved {len(all_businesses)} businesses to {OUTPUT_CSV}")
    print(f"  {with_email} have email addresses  ← ready to send")
    print(f"  {len(all_businesses) - with_email} without emails")
    print(f"\nNext steps:")
    print(f"  Preview:  python sender.py --dry-run")
    print(f"  Send:     python sender.py")


if __name__ == "__main__":
    main()
