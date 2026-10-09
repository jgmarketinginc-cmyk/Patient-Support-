#!/usr/bin/env python3
"""Plan a Chief of Staff run from a playbook (see sops/chief-of-staff-sop.md).

PLANS ONLY. It never calls an agent. The main session (/cos) executes the plan with the Agent tool:
steps in the same wave are launched together in one turn, later waves wait for earlier ones.

Usage:
  python execution/plan_run.py <playbook> [--inputs inputs.json] [--run-id RUN-...] [--date YYYY-MM-DD]
inputs.json example: {"transcript": "path", "apollo_contact_id": "X", "records": ["rec1", "rec2"]}
Prints the plan as JSON. `ready` is false when a required input is missing or an agent is not callable.
"""
import argparse
import datetime
import json
import sys

sys.dont_write_bytecode = True
from cos_common import (ROOT, callable_agent, current_phase, is_conductor, load_authority,
                        load_playbooks, load_registry, registry_name)

MAX_PARALLEL = 6          # cap on concurrent agent calls per turn (decision-rights C2)
RETRY_LIMIT = 1           # one rework per step, then halt and escalate


def _split(cell):
    return [] if cell.strip() in ("", "-") else [c.strip() for c in cell.split(",") if c.strip()]


def plan(playbook, inputs=None, root=ROOT, run_id="RUN-<id>", date=None):
    inputs = inputs or {}
    date = date or datetime.date.today().isoformat()
    books = load_playbooks(root)
    if playbook not in books:
        return {"playbook": playbook, "ready": False, "blocking": [f"unknown playbook {playbook}"], "steps": [], "waves": []}
    book = books[playbook]
    registry, authority = load_registry(root), load_authority(root)
    blocking = []

    if book["pending"]:
        blocking.append(f"playbook {playbook} has no steps defined [PENDING: Joaquin]")
    missing = [k for k in book["required_inputs"] if k not in inputs]
    if missing:
        blocking.append("missing required inputs: " + ", ".join(missing))

    # Expand per:<input> repeats into one step per item.
    steps = []
    for row in book["steps"]:
        base = {"id": row["Step"], "agent": row["Agent"], "depends_on": _split(row["Depends on"]),
                "condition": row["Condition"], "input": row["Input"], "output": row["Output"],
                "gate": None if row["Gate"].strip() in ("", "-") else row["Gate"].strip()}
        rep = row["Repeat"].strip()
        if rep.startswith("per:"):
            items = inputs.get(rep[4:])
            if items:
                for i, item in enumerate(items, 1):
                    steps.append({**base, "id": f"{row['Step']}.{i}", "item": item, "expands": row["Step"]})
            else:
                steps.append({**base, "item": None, "expands": row["Step"],
                              "note": f"expand one call per item once '{rep[4:]}' is known"})
        else:
            steps.append(base)

    # A dependency on an expanded step means all its copies.
    ids = {s["id"] for s in steps}
    expanded = {}
    for s in steps:
        if s.get("expands"):
            expanded.setdefault(s["expands"], []).append(s["id"])
    for s in steps:
        deps = []
        for d in s["depends_on"]:
            deps.extend(expanded.get(d, [d]))
        s["depends_on"] = deps
        unknown = [d for d in deps if d not in ids]
        if unknown:
            blocking.append(f"step {s['id']} depends on unknown step(s) {unknown}")

    # Waves = longest dependency chain depth; each wave split to the parallel cap.
    depth = {}

    def level(s, seen=()):
        if s["id"] in depth:
            return depth[s["id"]]
        if s["id"] in seen:
            blocking.append(f"dependency cycle at {s['id']}")
            return 0
        by_id = {x["id"]: x for x in steps}
        depth[s["id"]] = 1 + max([level(by_id[d], seen + (s["id"],)) for d in s["depends_on"] if d in by_id] or [-1])
        return depth[s["id"]]

    for s in steps:
        level(s)
    waves = []
    for lv in sorted(set(depth.values())):
        members = [s["id"] for s in steps if depth[s["id"]] == lv]
        for i in range(0, len(members), MAX_PARALLEL):
            waves.append(members[i:i + MAX_PARALLEL])

    phase = current_phase(root)
    for s in steps:
        agent = s["agent"]
        if is_conductor(agent):
            s["callable"], s["status"] = True, "conductor (Chief of Staff does this step)"
        else:
            ok, why = callable_agent(agent, root, registry, authority)
            s["callable"], s["status"] = ok, why
            if not ok:
                blocking.append(f"step {s['id']}: {why}")
        name = registry_name(agent, registry) or agent
        s["brief"] = {
            "run_id": run_id,
            "venture": book["meta"].get("venture"),
            "step": s["id"],
            "task": s["output"],
            "owning_agent": name,
            "inputs": s["input"] + (f" | item: {s['item']}" if s.get("item") else "") + (f" | inputs: {inputs}" if inputs else ""),
            "constraints": [f"current phase: {phase}",
                            f"agent status: {authority.get(name, 'n/a')} (shadow = drafts only, no external action, no Apollo writes, no paid calls)",
                            "no price above $1,500 in a verbal script; never discount; reduced scope is the only lever",
                            "never invent facts; unknown = [PENDING: <x>, Joaquin]"],
            "expected_output_path": f"outputs/shadow/{date}/{name.lower()}/cos-{run_id}-{s['id']}-<name>",
            "handoff_target": next((o["id"] for o in steps if s["id"] in o["depends_on"]), "Chief of Staff"),
            "gate": s["gate"],
            "approver": "Joaquin",
            "retry_limit": RETRY_LIMIT,
        }

    return {
        "playbook": playbook,
        "venture": book["meta"].get("venture"),
        "trigger": book["meta"].get("trigger"),
        "stop_conditions": book["meta"].get("stop_conditions"),
        "run_id": run_id,
        "ready": not blocking,
        "blocking": blocking,
        "max_parallel": MAX_PARALLEL,
        "waves": waves,
        "steps": steps,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("playbook")
    ap.add_argument("--inputs")
    ap.add_argument("--run-id", default="RUN-<id>")
    ap.add_argument("--date")
    a = ap.parse_args()
    data = json.load(open(a.inputs)) if a.inputs else {}
    print(json.dumps(plan(a.playbook, data, run_id=a.run_id, date=a.date), indent=2))
