#!/usr/bin/env python3
"""Send a Telegram notification (shadow mode: counts and status only).

Reads TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID from the environment. Neither
value is ever printed, logged, or echoed in an error message.

Shadow mode allows ONLY these message shapes (allowlist, not blocklist):
    "N drafts ready for review"      e.g. "3 drafts ready for review"
    "Telegram connection test OK"
Anything else is refused, which keeps prospect data (names, emails, orgs,
cities, links, phone numbers, free text) from ever leaving the system.

Usage:  python execution/notify_telegram.py "3 drafts ready for review"
Exit 0 = sent. 1 = refused (policy). 2 = missing env. 3 = delivery failed.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ALLOWED = [
    re.compile(r"\d{1,4} drafts? ready for review"),
    re.compile(r"Telegram connection test OK"),
]


def is_allowed(message: str) -> bool:
    return any(p.fullmatch(message) for p in ALLOWED)


def send(message: str) -> int:
    if not is_allowed(message):
        print("REFUSED: shadow mode only allows 'N drafts ready for review'. No prospect data may be sent.")
        return 1
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("MISSING: set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in the environment.")
        return 2
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    body = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=15) as resp:
            ok = json.load(resp).get("ok") is True
    except Exception as exc:  # exception text can embed the URL (and token); report type only
        print(f"FAILED: delivery error ({type(exc).__name__}).")
        return 3
    print("SENT" if ok else "FAILED: Telegram did not accept the message.")
    return 0 if ok else 3


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(send(sys.argv[1]))
