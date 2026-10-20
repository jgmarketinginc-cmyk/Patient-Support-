#!/usr/bin/env python3
"""Read-only team rollup for the Chief of Staff (see sops/chief-of-staff-sop.md).

Combines config/agent-registry.md, config/authority.md and logs/shadow-log.csv into one row per agent:
phase, status, items logged, items awaiting Joaquin, approved-with-no-edits rate, critical errors.
Writes nothing.

Usage:
  python execution/team_status.py [--json]
"""
import csv
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from cos_common import ROOT, callable_agent, load_authority, load_registry


def status(root=ROOT):
    registry, authority = load_registry(root), load_authority(root)
    log = Path(root) / "logs" / "shadow-log.csv"
    rows = []
    if log.exists():
        with open(log, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    by_slug = {k.lower().replace(" ", "-"): k for k in list(registry) + list(authority)}
    extra = {by_slug.get(r["agent"].lower(), r["agent"].title()) for r in rows}
    names = list(registry) + sorted(n for n in extra if n.lower() not in {k.lower() for k in registry})
    out = []
    for name in names:
        mine = [r for r in rows if r["agent"].lower() == name.lower().replace(" ", "-")]
        approved = [r for r in mine if r["approved"].lower() in ("yes", "approved")]
        decided = [r for r in mine if r["approved"].lower() not in ("pending", "")]
        clean = [r for r in approved if (r.get("edits") or "0").strip() in ("", "0", "none")]
        ok, why = callable_agent(name, root, registry, authority) if name in registry else (False, "not in registry")
        out.append({
            "agent": name,
            "phase": registry.get(name, {}).get("Phase", "0" if name in authority else "?"),
            "authority_status": authority.get(name, "not listed"),
            "callable": ok,
            "items_logged": len(mine),
            "awaiting_joaquin": sum(1 for r in mine if r["approved"].lower() == "pending"),
            "approved_no_edit_rate": round(len(clean) / len(decided), 2) if decided else None,
            "critical_errors": sum(1 for r in mine if (r.get("error_severity") or "").lower() == "critical"),
        })
    return out


def render(rows):
    head = f"{'Agent':<10} {'Ph':<3} {'Authority status':<24} {'Call':<5} {'Logged':>6} {'Await':>5} {'NoEdit%':>8} {'Crit':>4}"
    lines = [head, "-" * len(head)]
    for r in rows:
        rate = "n/a" if r["approved_no_edit_rate"] is None else f"{int(r['approved_no_edit_rate'] * 100)}%"
        lines.append(f"{r['agent']:<10} {r['phase']:<3} {r['authority_status']:<24} {'yes' if r['callable'] else 'no':<5} "
                     f"{r['items_logged']:>6} {r['awaiting_joaquin']:>5} {rate:>8} {r['critical_errors']:>4}")
    return "\n".join(lines)


if __name__ == "__main__":
    data = status()
    print(json.dumps(data, indent=2) if "--json" in sys.argv else render(data))
