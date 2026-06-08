"""
sender.py — Send cold emails via Resend API.

Usage:
    python sender.py [--csv berlin_outreach.csv] [--dry-run]

Requires .env with:
    RESEND_API_KEY=re_...
    FROM_EMAIL=you@yourdomain.com   (must be a verified Resend sender)
"""

import argparse
import csv
import os
import random
import sys
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

SENDER_NAME = "Ioana Laura Mocanu"
RESEND_URL = "https://api.resend.com/emails"


def load_businesses(csv_path: str) -> list[dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("Email", "").strip()]


def send_one(api_key: str, from_email: str, to_email: str, subject: str, body: str) -> dict:
    resp = requests.post(
        RESEND_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": f"{SENDER_NAME} <{from_email}>",
            "to": [to_email],
            "subject": subject,
            "text": body,
        },
        timeout=15,
    )
    return resp.json()


def run(csv_path: str, dry_run: bool) -> None:
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    from_email = os.getenv("FROM_EMAIL", "").strip()

    if not api_key:
        sys.exit("Error: set RESEND_API_KEY in .env")
    if not from_email:
        sys.exit("Error: set FROM_EMAIL in .env (must be a verified Resend sender address)")

    businesses = load_businesses(csv_path)
    if not businesses:
        sys.exit(f"No businesses with email addresses found in {csv_path}")

    log_path = f"sent_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    print(f"{'[DRY RUN] ' if dry_run else ''}Sending to {len(businesses)} recipients → log: {log_path}\n")

    sent = failed = 0

    with open(log_path, "w", newline="", encoding="utf-8") as logfile:
        log = csv.writer(logfile)
        log.writerow(["Business Name", "Email", "Status", "Timestamp"])

        for i, biz in enumerate(businesses, 1):
            email = biz["Email"].strip()
            subject = biz.get("Subject") or f"Kurze Frage – {biz['Business Name']}"
            body = biz["Email Body"]

            if dry_run:
                print(f"[DRY RUN {i}/{len(businesses)}] → {biz['Business Name']} <{email}>")
                print(f"  Subject: {subject}")
                print(f"  Body preview: {body[:80].replace(chr(10), ' ')}…\n")
                log.writerow([biz["Business Name"], email, "DRY_RUN", datetime.now().isoformat()])
                sent += 1
                continue

            try:
                result = send_one(api_key, from_email, email, subject, body)
                if result.get("id"):
                    print(f"✓ [{i}/{len(businesses)}] {biz['Business Name']} <{email}>  id={result['id']}")
                    log.writerow([biz["Business Name"], email, "SENT", datetime.now().isoformat()])
                    sent += 1
                else:
                    error = result.get("message") or str(result)
                    print(f"✗ [{i}/{len(businesses)}] {biz['Business Name']} <{email}> — {error}")
                    log.writerow([biz["Business Name"], email, f"FAILED: {error}", datetime.now().isoformat()])
                    failed += 1
            except Exception as exc:
                print(f"✗ [{i}/{len(businesses)}] {biz['Business Name']} <{email}> — {exc}")
                log.writerow([biz["Business Name"], email, f"FAILED: {exc}", datetime.now().isoformat()])
                failed += 1

            if i < len(businesses):
                delay = random.randint(30, 60)
                print(f"  Waiting {delay}s…")
                time.sleep(delay)

    print(f"\nDone. Sent: {sent}  Failed: {failed}  Log: {log_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="berlin_outreach.csv")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview emails without sending")
    args = parser.parse_args()
    run(args.csv, args.dry_run)
