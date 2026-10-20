#!/usr/bin/env python3
"""Gate a handoff between agents (see sops/chief-of-staff-sop.md, config/handoff-contracts.md).

Checks an agent's output file against a named contract. The generic `any` contract
(Sources / Assumptions present) is always applied.

Usage:
  python execution/check_handoff.py <contract> <output-file>
Prints JSON {contract, pass, failed[], warnings[], checked}. Exit 0 = pass, 1 = fail, 2 = bad usage.
"""
import json
import re
import sys

sys.dont_write_bytecode = True
from cos_common import ROOT, first_table, read

ENTRY_PRICE = 1500       # AI Audit; anything above is written-proposal only (config/business.md)


def contracts(root=ROOT):
    rows = first_table(read(root, "config/handoff-contracts.md"))
    out = {}
    for r in rows:
        out.setdefault(r["Contract"], []).append(r)
    return out


def _json(text):
    try:
        data = json.loads(text)
        return data if isinstance(data, dict) else None
    except ValueError:
        return None


def body_only(text):
    """Text before the Sources / Assumptions section: that note may legitimately say 'no discount'."""
    m = re.search(r"^#+\s*Sources\s*/\s*Assumptions", text, re.I | re.M)
    return text[:m.start()] if m else text


def check(contract, text, root=ROOT):
    table = contracts(root)
    if contract not in table:
        return {"contract": contract, "pass": False, "failed": [f"unknown contract '{contract}'"], "warnings": [], "checked": 0}
    rules = table["any"] + (table[contract] if contract != "any" else [])
    data = _json(text)
    failed, warnings = [], []
    for r in rules:
        kind, spec, field = r["Kind"], r["Spec"], r["Field"]
        ok, detail = True, ""
        if kind == "regex":
            ok = re.search(spec, text) is not None
            detail = f"pattern {spec!r} not found"
        elif kind == "absent":
            m = re.search(spec, body_only(text))
            ok = m is None
            detail = f"forbidden text found: {m.group(0)!r}" if m else ""
        elif kind == "json_key":
            ok = data is not None and spec in data and data[spec] not in (None, "", [])
            detail = "output is not a JSON object" if data is None else f"key '{spec}' missing or empty"
        elif kind == "json_len":
            key, _, n = spec.partition("=")
            ok = data is not None and isinstance(data.get(key), list) and len(data[key]) == int(n)
            detail = "output is not a JSON object" if data is None else f"'{key}' must be a list of {n}"
        elif kind == "max_price":
            amounts = [float(a.replace(",", "")) for a in re.findall(r"\$\s?(\d[\d,]*(?:\.\d+)?)", body_only(text))]
            over = [a for a in amounts if a > float(spec)]
            ok = not over
            detail = f"price(s) above ${int(float(spec)):,}: {over}"
        else:
            ok, detail = False, f"unknown kind '{kind}'"
        if not ok:
            (failed if r["Required"].upper() == "Y" else warnings).append(f"{field}: {detail}")
    return {"contract": contract, "pass": not failed, "failed": failed, "warnings": warnings, "checked": len(rules)}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    result = check(sys.argv[1], open(sys.argv[2], encoding="utf-8").read())
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["pass"] else 1)
