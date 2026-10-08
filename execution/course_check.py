#!/usr/bin/env python3
"""Maya's pre-handoff check on a training module script (sops/maya-sop.md step 5).

Module file format:
  Module: 3
  Title: Reviewing auto-drafted responses
  Target minutes: 8
  Task: Decide whether to send, edit or escalate a drafted response.
  Audience: Staff who review drafts daily
  On-screen steps:
  1. <what the viewer sees and clicks>
  Spoken:
  <narration>
  What to do next:
  <one line>
  ## Sources / Assumptions

Fails on: missing fields; an off-phase service named as something the system does (naming it in a "does not do"
clause, such as "does not handle inspections", is allowed); target or estimated length outside 3-8 minutes (130 words/minute of Spoken text);
more than one Task; no numbered on-screen steps; result claims, percentages, testimonials; prices above the
entry offer; an unapproved client name; retired brand names.
Warns when the estimate differs from the target by more than 20%, or Sources are missing.

Usage: python execution/course_check.py module.md [--client "Name"]...
  --client   a client name that is NOT approved for use (must be absent)
Exit 0 = PASS, 1 = FAIL.
"""
import os
import re
import sys

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "execution"))
from brand_scrub import PATTERNS  # noqa: E402

WORDS_PER_MIN = 130
MIN_MIN, MAX_MIN = 3, 8
ENTRY_PRICE = 1500
CLAIMS = re.compile(r"testimonial|trusted by|case stud|guarantee|proven|award|\d\s?%", re.I)
OFF_PHASE = re.compile(r"document intake|inspection|scheduling|resilience", re.I)
# An off-phase service may be NAMED when the clause says the system does not do it ("does not handle inspections").
NEGATION = re.compile(r"\b(does not|do not|doesn't|don't|will not|won't|cannot|can't|never|is not|isn't|not part of|not covered|"
                      r"not in scope|out of scope|outside)\b", re.I)
SECTIONS = ("On-screen steps", "Spoken", "What to do next")


def sections(text):
    """Split into {section name: text} on lines like 'Spoken:'; header fields stay in 'head'."""
    out, current = {"head": []}, "head"
    for line in text.splitlines():
        m = re.match(r"^(On-screen steps|Spoken|What to do next):\s*(.*)$", line)
        if m:
            current = m.group(1)
            out[current] = [m.group(2)] if m.group(2) else []
            continue
        if re.match(r"^#+\s*Sources", line, re.I):
            current = "sources"
            out[current] = []
            continue
        out.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def check(text, banned_clients=()):
    fails, warns = [], []
    sec = sections(text)
    head = sec["head"]
    for field in ("Module", "Title", "Target minutes", "Task"):
        if not re.search(rf"(?m)^{field}:\s*\S", head):
            fails.append(f"missing {field}")
    for name in SECTIONS:
        if not sec.get(name):
            fails.append(f"missing or empty '{name}' section")
    if len(re.findall(r"(?m)^Task:", head)) > 1:
        fails.append("more than one Task: one task per module")
    task = re.search(r"(?m)^Task:\s*(.+)$", head)
    if task and ";" in task.group(1):
        fails.append("the Task line lists more than one task (';'): split into modules")
    if sec.get("On-screen steps") and not re.search(r"(?m)^\s*\d+[.)]\s+\S", sec["On-screen steps"]):
        fails.append("On-screen steps must be a numbered list")

    target = re.search(r"(?m)^Target minutes:\s*(\d+(?:\.\d+)?)", head)
    t = float(target.group(1)) if target else None
    if t is not None and not (MIN_MIN <= t <= MAX_MIN):
        fails.append(f"target {t:g} min is outside {MIN_MIN}-{MAX_MIN}")
    words = len(sec.get("Spoken", "").split())
    est = words / WORDS_PER_MIN
    if sec.get("Spoken") and not (MIN_MIN <= est <= MAX_MIN):
        fails.append(f"spoken text is about {est:.1f} min ({words} words); must be {MIN_MIN}-{MAX_MIN} min")
    elif t and sec.get("Spoken") and abs(est - t) / t > 0.20:
        warns.append(f"estimate {est:.1f} min differs from the {t:g} min target by more than 20%")

    body = text[:re.search(r"(?mi)^#+\s*Sources", text).start()] if re.search(r"(?mi)^#+\s*Sources", text) else text
    m = CLAIMS.search(body)
    if m:
        fails.append(f"result claim, percentage or testimonial language: '{m.group(0)}'")
    over = [a for a in re.findall(r"\$\s?(\d[\d,]*)", body) if float(a.replace(",", "")) > ENTRY_PRICE]
    if over:
        fails.append(f"price above ${ENTRY_PRICE:,} in a training asset: {over}")
    for clause in re.split(r"[.!?;:\n]+", body):
        m = OFF_PHASE.search(clause)
        if m and not re.search(NEGATION.pattern + r".*" + re.escape(m.group(0)), clause, re.I):
            fails.append(f"off-phase service named as something the system does: '{m.group(0)}' (naming it is allowed only in a 'does not do' clause)")
            break
    for name in banned_clients:
        if re.search(re.escape(name), text, re.I):
            fails.append(f"unapproved client name present: '{name}'")
    for p in PATTERNS:
        if p.search(text):
            fails.append("retired brand name present (see execution/brand_scrub.py)")
            break
    if "sources" not in sec:
        warns.append("missing Sources / Assumptions section")
    return {"pass": not fails, "fails": fails, "warns": warns, "words": words, "minutes": round(est, 1)}


if __name__ == "__main__":
    args = sys.argv[1:]
    banned, path, i = [], None, 0
    while i < len(args):
        if args[i] == "--client":
            banned.append(args[i + 1]); i += 2
        else:
            path = args[i]; i += 1
    if not path:
        print(__doc__)
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        res = check(f.read(), banned)
    print("PASS" if res["pass"] else "FAIL", f"({res['words']} spoken words, ~{res['minutes']} min)")
    for f in res["fails"]:
        print("  FAIL:", f)
    for w in res["warns"]:
        print("  WARN:", w)
    sys.exit(0 if res["pass"] else 1)
