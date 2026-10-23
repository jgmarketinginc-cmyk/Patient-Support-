#!/usr/bin/env python3
"""Shadow exit-test status per agent from logs/shadow-log.csv.
Exit test (config/authority.md): 10 business days, >=95% approved with no edits, zero critical errors.
Rows with approved=pending are counted as awaiting review, not as passes."""
import csv, sys, collections
path = sys.argv[1] if len(sys.argv) > 1 else "logs/shadow-log.csv"
a = collections.defaultdict(lambda: {"days": set(), "clean": 0, "reviewed": 0, "pending": 0, "critical": 0})
for r in csv.DictReader(open(path)):
    if r["item"].startswith("DRYRUN"):
        continue
    s = a[r["agent"]]
    s["days"].add(r["date"])
    st = (r["approved"] or "").strip().lower()
    if st in ("", "pending"):
        s["pending"] += 1
        continue
    s["reviewed"] += 1
    if st in ("yes", "approved", "y") and not (r["edits"] or "").strip():
        s["clean"] += 1
    if (r["error_severity"] or "").strip().lower() == "critical":
        s["critical"] += 1
print(f"{'agent':<12}{'days':>5}{'reviewed':>9}{'clean%':>8}{'pending':>8}{'critical':>9}  exit")
for k, s in sorted(a.items()):
    pct = 100 * s["clean"] / s["reviewed"] if s["reviewed"] else 0
    ok = len(s["days"]) >= 10 and s["reviewed"] and pct >= 95 and s["critical"] == 0 and s["pending"] == 0
    print(f"{k:<12}{len(s['days']):>5}{s['reviewed']:>9}{pct:>8.0f}{s['pending']:>8}{s['critical']:>9}  {'READY' if ok else 'not yet'}")
