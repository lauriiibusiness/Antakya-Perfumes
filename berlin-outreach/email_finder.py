"""
email_finder.py — Extract contact email from a business website.
Checks main page, then /kontakt, /impressum, /contact paths.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Optional

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')

CONTACT_PATHS = [
    "/impressum", "/kontakt", "/contact",
    "/ueber-uns", "/uber-uns", "/about", "/contact-us",
]

_BLACKLIST = [
    "example", "domain", "noreply", "no-reply", "sentry",
    "wixpress", "wordpress", "support@w", ".png", ".jpg", ".gif",
    "@schema", "@context",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def find_email(website_url: str, timeout: int = 8) -> Optional[str]:
    if not website_url:
        return None
    if not website_url.startswith(("http://", "https://")):
        website_url = "https://" + website_url

    parsed = urlparse(website_url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    # Try main page first, then contact paths
    for url in [website_url] + [base + p for p in CONTACT_PATHS]:
        email = _extract_from_url(url, timeout)
        if email:
            return email

    return None


def _extract_from_url(url: str, timeout: int) -> Optional[str]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # Prefer mailto: links — most reliable
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("mailto:"):
                email = href[7:].split("?")[0].strip().lower()
                if _is_valid(email):
                    return email

        # Fallback: regex scan
        for match in EMAIL_REGEX.findall(resp.text):
            if _is_valid(match.lower()):
                return match.lower()

    except Exception:
        pass

    return None


def _is_valid(email: str) -> bool:
    if not email or "@" not in email:
        return False
    return not any(bad in email for bad in _BLACKLIST)
