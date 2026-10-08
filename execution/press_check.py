#!/usr/bin/env python3
"""Jerry's pre-handoff check on a press release (sops/jerry-sop.md step 4).

Fails on: honorifics (Mr./Ms./Mrs./Miss assume gender; use the last name on second reference), missing headline, dateline, "About The AI Agency Blueprint" boilerplate or media contact; body outside
300-500 words; superlatives, unsourced "first" claims and "guarantee" (a line carrying "[source: ...]" is exempt);
percentages or dollar amounts (unless --allow-stats); a quotation without an approval tag
("[quote approved: name, date]" or "[QUOTE PENDING approval: name]"); an off-phase service; an unapproved client name;
retired brand names. Warns on internal compliance language in public copy (for example "has not approved", "no case studies"), when no
--client names were supplied to check against, or Sources are missing.

Usage: python execution/press_check.py release.md [--client "Name"]... [--approved-client "Name"]... [--allow-stats]
  --client           a client name that is NOT approved for use (must be absent), like asset_check.py
  --approved-client  a client name Joaquin recorded as approved (cancels a matching --client)
Exit 0 = PASS, 1 = FAIL.
"""
import os
import re
import sys

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "execution"))
from brand_scrub import PATTERNS  # noqa: E402

MIN_WORDS, MAX_WORDS = 300, 500
SUPERLATIVES = re.compile(r"\b(first|leading|best|only|largest|revolutionary|groundbreaking|world-class|"
                          r"cutting-edge|unparalleled|guarantee[ds]?)\b", re.I)
OFF_PHASE = re.compile(r"document intake|inspection|scheduling|resilience", re.I)
DATELINE = re.compile(r"(?m)^\s*(\[[^\]\n]+\]|[A-Z][A-Za-z .]+,\s*[A-Z]{2}(?:,[^—–\-\n]*)?)\s*[—–-]")
QUOTE = re.compile(r"[\"“]([^\"“”]{8,})[\"”]")
HONORIFIC = re.compile(r"\b(Mr|Mrs|Ms|Miss)\.(?=\s)")
INTERNAL_NOTE = re.compile(r"has not approved|not (yet )?approved|no case stud|makes? no claims|not available to cite", re.I)
TAG = re.compile(r"\[(quote approved:|QUOTE PENDING)", re.I)


def body_of(text):
    m = re.search(r"(?mi)^#+\s*Sources\s*/\s*Assumptions", text)
    return text[:m.start()] if m else text


def check(text, banned_clients=(), approved_clients=(), allow_stats=False):
    fails, warns = [], []
    body = body_of(text)
    if not re.search(r"(?m)^#\s+\S", body):
        fails.append("missing headline (a '# ' heading)")
    if not DATELINE.search(body):
        fails.append("missing dateline, for example '[CITY, NJ, DATE] -' at the start of the lead")
    if not re.search(r"About The AI Agency Blueprint", body):
        fails.append("missing 'About The AI Agency Blueprint' boilerplate")
    if not re.search(r"(?i)media contact", body):
        fails.append("missing media contact")
    words = len(re.sub(r"(?m)^#+\s.*$", " ", body).split())
    if not (MIN_WORDS <= words <= MAX_WORDS):
        fails.append(f"body is {words} words; must be {MIN_WORDS}-{MAX_WORDS}")
    for i, line in enumerate(body.splitlines(), 1):
        if "[source:" in line.lower():
            continue
        m = SUPERLATIVES.search(line)
        if m:
            fails.append(f"line {i}: superlative or unsourced claim '{m.group(0)}' (add '[source: ...]' only if documented)")
    if not allow_stats:
        for m in re.finditer(r"\d+(?:\.\d+)?\s?%|\$\s?\d[\d,]*", body):
            fails.append(f"percentage or dollar amount '{m.group(0)}' (use --allow-stats only for client-approved figures)")
    for m in QUOTE.finditer(body):
        tail = body[m.end():m.end() + 140]
        if not TAG.search(tail):
            fails.append(f"quotation without an approval tag: \"{m.group(1)[:40]}...\"")
    m = OFF_PHASE.search(body)
    if m:
        fails.append(f"off-phase service named: '{m.group(0)}'")
    m = HONORIFIC.search(body)
    if m:
        fails.append(f"honorific '{m.group(0)}' assumes gender: use the last name only unless Joaquin supplies the preferred form")
    public = re.sub(r"\[[^\]]*\]", " ", body)
    m = INTERNAL_NOTE.search(public)
    if m:
        warns.append(f"internal compliance language in public copy: '{m.group(0)}' (belongs in the open-facts list, not the release)")
    banned = [c for c in banned_clients if c.lower() not in {a.lower() for a in approved_clients}]
    for name in banned:
        if re.search(re.escape(name), text, re.I):
            fails.append(f"unapproved client name present: '{name}'")
    if not banned_clients:
        warns.append("no --client names supplied; client names were not checked automatically")
    if not re.search(r"(?mi)^#+\s*Sources", text):
        warns.append("missing Sources / Assumptions section")
    for p in PATTERNS:
        if p.search(text):
            fails.append("retired brand name present (see execution/brand_scrub.py)")
            break
    return {"pass": not fails, "fails": fails, "warns": warns, "words": words}


if __name__ == "__main__":
    args = sys.argv[1:]
    banned, approved, stats = [], [], False
    path = None
    i = 0
    while i < len(args):
        if args[i] == "--client":
            banned.append(args[i + 1]); i += 2
        elif args[i] == "--approved-client":
            approved.append(args[i + 1]); i += 2
        elif args[i] == "--allow-stats":
            stats = True; i += 1
        else:
            path = args[i]; i += 1
    if not path:
        print(__doc__)
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        res = check(f.read(), banned, approved, stats)
    print("PASS" if res["pass"] else "FAIL", f"({res['words']} words)")
    for f in res["fails"]:
        print("  FAIL:", f)
    for w in res["warns"]:
        print("  WARN:", w)
    sys.exit(0 if res["pass"] else 1)
