#!/usr/bin/env python3
"""Vicky's pre-handoff check on a scripture short-form script (sops/vicky-sop.md step 4).

Script file format (one field per line):
  Reference: John 3:16          (repeat Reference/Quote pairs for more than one verse)
  Translation: KJV
  Quote: "For God so loved the world, ..."
  Platform: Reels
  Script:
  <hook line, 15 words or fewer>
  <body ...>
  Caption: ...
  Hashtags: ...

Fails on: missing fields, malformed reference, translation not listed in config/scripture.md, a Quote that
does not appear in the Script as quoted, a Quote that is not a contiguous part of the verse text (when
config/scripture/<TRANSLATION>.txt exists), a hook over 15 words, spoken length outside 15-60 seconds
(2.5 words/second), outcome promises or percentages outside quotation marks, retired brand names.
Warns on: translation not yet confirmed by Joaquin, UNVERIFIED quotes (no local verse text), missing
caption/hashtags/Sources.

Usage: python execution/scripture_check.py script.md [--root DIR]
Exit 0 = PASS, 1 = FAIL.
"""
import os
import re
import sys

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "execution"))
from brand_scrub import PATTERNS  # noqa: E402
from cos_common import first_table  # noqa: E402

WORDS_PER_SEC = 2.5
MIN_SEC, MAX_SEC = 15, 60
HOOK_MAX_WORDS = 15
REF = re.compile(r"^(?:[1-3]\s)?[A-Za-z]+(?:\s[A-Za-z]+)*\s\d+:\d+(?:[-–]\d+)?$")
# Outcome promises and numbers claims; checked outside quotation marks only (a verse may say anything).
PROMISES = re.compile(r"guarantee|god will (make you rich|heal you|give you|bless you with)|"
                      r"send (us |me )?(money|a seed)|sow a seed|get rich|\d\s?%", re.I)


def norm(s):
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split())


def parse(text):
    fields = {"Reference": [], "Quote": []}
    single = {}
    script, in_script = [], False
    for line in text.splitlines():
        m = re.match(r"^(Reference|Translation|Quote|Platform|Caption|Hashtags|Hooks|Script):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            in_script = key == "Script"
            if key in fields:
                fields[key].append(val)
            elif key == "Script":
                if val:
                    script.append(val)
            else:
                single[key] = val
            continue
        if re.match(r"^#+\s*Sources", line, re.I):
            in_script = False
            single["Sources"] = True
        if in_script:
            script.append(line)
    return fields, single, "\n".join(script).strip()


def load_translations(root):
    path = os.path.join(root, "config", "scripture.md")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        rows = first_table(f.read())
    return {r["Translation"].upper(): r["Status"] for r in rows if r.get("Translation")}


def verse_text(root, translation, ref):
    """Joined verse text for `ref` from config/scripture/<TRANSLATION>.txt, or None if unavailable."""
    path = os.path.join(root, "config", "scripture", f"{translation.upper()}.txt")
    if not os.path.exists(path):
        return None
    verses = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "\t" in line:
                k, v = line.rstrip("\n").split("\t", 1)
                verses[k.strip().lower()] = v
    m = re.match(r"^(.*\s\d+):(\d+)(?:[-–](\d+))?$", ref)
    if not m:
        return None
    book_ch, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    parts = [verses.get(f"{book_ch}:{n}".lower()) for n in range(a, b + 1)]
    return None if any(p is None for p in parts) else " ".join(parts)


def check(text, root=ROOT):
    fails, warns = [], []
    fields, single, script = parse(text)
    for key in ("Reference", "Quote"):
        if not fields[key]:
            fails.append(f"missing {key}")
    for key in ("Translation",):
        if not single.get(key):
            fails.append(f"missing {key}")
    if not script:
        fails.append("missing Script")
    for key in ("Caption", "Hashtags"):
        if not single.get(key):
            warns.append(f"missing {key}")
    if not single.get("Sources"):
        warns.append("missing Sources / Assumptions section")
    if len(fields["Reference"]) != len(fields["Quote"]):
        fails.append("each Reference needs exactly one Quote (counts differ)")

    translation = (single.get("Translation") or "").upper()
    allowed = load_translations(root)
    if translation:
        if translation not in allowed:
            fails.append(f"translation {translation} is not listed in config/scripture.md (needs Joaquin's approval)")
        elif not allowed[translation].upper().startswith("SET"):
            warns.append(f"translation {translation} is '{allowed[translation]}', not yet confirmed by Joaquin")

    script_n = norm(script)
    for ref, quote in zip(fields["Reference"], fields["Quote"]):
        if not REF.match(ref):
            fails.append(f"reference '{ref}' is not 'Book C:V' or 'Book C:V-V'")
        q = quote.strip().strip('"“”')
        if "[VERSE TEXT PENDING" in quote:
            warns.append(f"{ref}: verse text pending")
            continue
        if norm(q) not in script_n:
            fails.append(f"{ref}: the Quote does not appear in the Script exactly as quoted")
        vt = verse_text(root, translation, ref) if translation else None
        if vt is None:
            warns.append(f"{ref}: UNVERIFIED (no local verse text in config/scripture/{translation or '?'}.txt); a person must check it against the approved source")
        elif norm(q) not in norm(vt):
            fails.append(f"{ref}: the Quote is not a contiguous part of the {translation} text")

    lines = [ln.strip() for ln in script.splitlines() if ln.strip()]
    if lines and len(lines[0].split()) > HOOK_MAX_WORDS:
        fails.append(f"hook is {len(lines[0].split())} words (max {HOOK_MAX_WORDS})")
    words = len(script.split())
    secs = words / WORDS_PER_SEC
    if not (MIN_SEC <= secs <= MAX_SEC):
        fails.append(f"spoken length about {secs:.0f}s ({words} words); must be {MIN_SEC}-{MAX_SEC}s")

    outside_quotes = re.sub(r'["“][^"“”]*["”]', " ", script)
    m = PROMISES.search(outside_quotes)
    if m:
        fails.append(f"outcome promise or percentage outside quotation marks: '{m.group(0)}'")
    for p in PATTERNS:
        if p.search(text):
            fails.append("retired brand name present (see execution/brand_scrub.py)")
            break
    return {"pass": not fails, "fails": fails, "warns": warns, "words": words, "seconds": round(secs)}


if __name__ == "__main__":
    args = sys.argv[1:]
    root = ROOT
    if "--root" in args:
        i = args.index("--root")
        root = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    with open(args[0], encoding="utf-8") as f:
        res = check(f.read(), root)
    print("PASS" if res["pass"] else "FAIL", f"({res['words']} words, ~{res['seconds']}s)")
    for f in res["fails"]:
        print("  FAIL:", f)
    for w in res["warns"]:
        print("  WARN:", w)
    sys.exit(0 if res["pass"] else 1)
