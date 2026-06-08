"""
sender.py — Send cold emails via Gmail SMTP.

Usage:
    python sender.py [--csv berlin_outreach.csv] [--dry-run]

Requires .env with:
    GMAIL_ADDRESS=you@gmail.com
    GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
"""

import argparse
import csv
import os
import random
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

SENDER_NAME = "Ioana Laura Mocanu"


def load_businesses(csv_path: str) -> list[dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("Email", "").strip()]


def run(csv_path: str, dry_run: bool) -> None:
    gmail_user = os.getenv("GMAIL_ADDRESS", "").strip()
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD", "").strip()

    if not gmail_user or not gmail_pass:
        sys.exit("Error: set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env")

    businesses = load_businesses(csv_path)
    if not businesses:
        sys.exit(f"No businesses with email addresses found in {csv_path}")

    log_path = f"sent_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    print(f"{'[DRY RUN] ' if dry_run else ''}Sending to {len(businesses)} recipients → log: {log_path}\n")

    sent = failed = 0

    with open(log_path, "w", newline="", encoding="utf-8") as logfile:
        log = csv.writer(logfile)
        log.writerow(["Business Name", "Email", "Status", "Timestamp"])

        smtp = None
        if not dry_run:
            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp.login(gmail_user, gmail_pass)

        try:
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
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = subject
                    msg["From"] = f"{SENDER_NAME} <{gmail_user}>"
                    msg["To"] = email
                    msg.attach(MIMEText(body, "plain", "utf-8"))
                    smtp.sendmail(gmail_user, email, msg.as_string())

                    print(f"✓ [{i}/{len(businesses)}] {biz['Business Name']} <{email}>")
                    log.writerow([biz["Business Name"], email, "SENT", datetime.now().isoformat()])
                    sent += 1
                except Exception as exc:
                    print(f"✗ [{i}/{len(businesses)}] {biz['Business Name']} <{email}> — {exc}")
                    log.writerow([biz["Business Name"], email, f"FAILED: {exc}", datetime.now().isoformat()])
                    failed += 1

                if i < len(businesses):
                    delay = random.randint(30, 60)
                    print(f"  Waiting {delay}s…")
                    time.sleep(delay)

        finally:
            if smtp:
                smtp.quit()

    print(f"\nDone. Sent: {sent}  Failed: {failed}  Log: {log_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="berlin_outreach.csv")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview emails without sending")
    args = parser.parse_args()
    run(args.csv, args.dry_run)
