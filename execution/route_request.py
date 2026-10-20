#!/usr/bin/env python3
"""Chief of Staff request router (see sops/chief-of-staff-sop.md).

Deterministic: keyword and rule matching over config/routing.md, config/agent-registry.md,
config/authority.md, config/playbooks.md, config/ventures.md and config/decision-rights.md.
No LLM calls, no network. The conductor (Claude, in the main session) makes the final call;
this script supplies a repeatable first classification.

Usage:
  python execution/route_request.py "find 50 NJ city clerks"
Prints JSON: {request, venture, task_type, mode, owner, confidence, needs_joaquin, reasons,
              cos_decides, joaquin_matters}
Exit 0 always (a routing result, including an escalation, is a valid result).
"""
import json
import re
import sys

sys.dont_write_bytecode = True
from cos_common import (ROOT, callable_agent, distinct_matches, is_conductor, load_authority,
                        load_playbooks, load_registry, load_rights, load_routing, load_ventures,
                        registry_name)

CONFIDENCE_FLOOR = 0.6


def detect_venture(text, ventures):
    best, best_n = None, 0
    for v in ventures:
        n = len(distinct_matches(v["Keywords"], text))
        if n > best_n:
            best, best_n = v["Key"], n
    return best


def route(request, root=ROOT):
    registry = load_registry(root)
    authority = load_authority(root)
    playbooks = load_playbooks(root)
    rights = load_rights(root)
    ventures = load_ventures(root)
    reasons = []

    joaquin_matters = [r["ID"] + " " + r["Matter"] for r in rights["joaquin"]
                       if re.search(r["Keywords"], request, re.I)]
    cos_decides = [r["ID"] + " " + r["Matter"] for r in rights["cos"]
                   if re.search(r["Keywords"], request, re.I)]

    # Score routing rows: (priority, distinct keyword matches).
    scored = []
    for row in load_routing(root):
        hits = distinct_matches(row["Keywords"], request)
        if hits:
            scored.append(((int(row["Priority"]), len(hits)), row))
    scored.sort(key=lambda s: s[0], reverse=True)

    mentioned = [n for n in registry if re.search(r"\b" + re.escape(n) + r"\b", request, re.I)]

    row, confidence = None, 0.0
    if scored:
        row = scored[0][1]
        confidence = min(0.9, 0.5 + 0.2 * scored[0][0][1])
        top_pri = scored[0][0][0]
        if top_pri >= 100:
            confidence = 0.95
        elif len(scored) > 1 and scored[1][0] == scored[0][0] and scored[1][1]["Owner"] != row["Owner"]:
            confidence = 0.4
            reasons.append(f"ambiguous: '{row['Task type']}' and '{scored[1][1]['Task type']}' tie")

    task_type = row["Task type"] if row else None
    venture = row["Venture"] if row else detect_venture(request, ventures)
    mode = row["Mode"] if row else "escalate"
    owner = row["Owner"] if row else "-"
    needs_joaquin = bool(row and row["Needs Joaquin"].upper() == "YES")

    # An explicit agent name wins, unless the row is a hard escalation (priority >= 100).
    hard_escalation = bool(row and int(row["Priority"]) >= 100)
    if mentioned and not hard_escalation:
        pick = next((n for n in mentioned if row and n.lower() == row["Owner"].lower()), mentioned[0])
        owner, mode, confidence = pick, "agent", max(confidence, 0.9)
        task_type = task_type if task_type and row and row["Owner"].lower() == pick.lower() else f"named_agent:{pick}"
        reasons.append(f"request names {pick}")
        if venture is None:
            venture = "aiab"
        if row and row["Owner"].lower() != pick.lower():
            reasons.append(f"routing row '{row['Task type']}' pointed to {row['Owner']}; explicit name wins")
        needs_joaquin = False

    # Callability.
    if mode == "agent" and owner != "-":
        ok, why = callable_agent(owner, root, registry, authority)
        reasons.append(why)
        if not ok:
            needs_joaquin = True
    elif mode == "playbook":
        book = playbooks.get(owner)
        if book is None:
            needs_joaquin = True
            reasons.append(f"playbook {owner} is not in config/playbooks.md")
        else:
            blocked = []
            for step in book["steps"]:
                if is_conductor(step["Agent"]):
                    continue
                ok, why = callable_agent(step["Agent"], root, registry, authority)
                if not ok:
                    blocked.append(why)
            if blocked:
                needs_joaquin = True
                reasons.extend(sorted(set(blocked)))
            if book["required_inputs"]:
                reasons.append("required inputs: " + ", ".join(book["required_inputs"]))
    elif mode == "escalate":
        needs_joaquin = True
        if venture and venture != "aiab":
            reasons.append(f"no agents or playbooks are defined for venture '{venture}' (see config/ventures.md, PENDING)")
        else:
            reasons.append(f"'{task_type}' always goes to Joaquin")

    if row is None and not mentioned:
        reasons.append("no routing rule matched")
        needs_joaquin = True
    if confidence < CONFIDENCE_FLOOR:
        reasons.append(f"confidence {confidence:.2f} below {CONFIDENCE_FLOOR}")
        needs_joaquin = True
        mode, owner = "escalate", "-"
    if joaquin_matters:
        needs_joaquin = True
        reasons.append("Joaquin-only matter: " + "; ".join(joaquin_matters))

    return {
        "request": request,
        "venture": venture,
        "task_type": task_type,
        "mode": mode,
        "owner": owner,
        "owner_agent_or_playbook": owner,
        "confidence": round(confidence, 2),
        "needs_joaquin": needs_joaquin,
        "reasons": reasons,
        "cos_decides": cos_decides,
        "joaquin_matters": joaquin_matters,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(route(" ".join(sys.argv[1:])), indent=2))
