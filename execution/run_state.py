#!/usr/bin/env python3
"""Chief of Staff run records (see sops/chief-of-staff-sop.md).

One JSON record per run at logs/cos-runs/<run_id>.json, and one summary row per run in
logs/cos-log.csv (date,run_id,goal,venture,playbook,status,steps_done,steps_total,needs_joaquin).
Records only; it never calls an agent.

Usage:
  python execution/run_state.py new   --goal "..." --venture aiab --playbook post-call --plan plan.json [--date D]
  python execution/run_state.py step  RUN-ID STEP-ID STATUS [--output PATH] [--note TEXT] [--retry]
  python execution/run_state.py finish RUN-ID STATUS [--needs-joaquin]
  python execution/run_state.py show  RUN-ID
STATUS for steps: pending | running | passed | failed | skipped | escalated.  Run STATUS: running | complete | halted | escalated.
"""
import argparse
import csv
import datetime
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from cos_common import ROOT

HEADER = ["date", "run_id", "goal", "venture", "playbook", "status", "steps_done", "steps_total", "needs_joaquin"]
DONE = {"passed", "skipped"}


def _paths(root):
    return Path(root) / "logs" / "cos-runs", Path(root) / "logs" / "cos-log.csv"


def _write_csv_row(root, run):
    _, csv_path = _paths(root)
    rows = []
    if csv_path.exists():
        with open(csv_path, newline="", encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f)]
    row = {"date": run["date"], "run_id": run["run_id"], "goal": run["goal"], "venture": run["venture"],
           "playbook": run["playbook"], "status": run["status"],
           "steps_done": sum(1 for s in run["steps"] if s["status"] in DONE),
           "steps_total": len(run["steps"]), "needs_joaquin": "YES" if run["needs_joaquin"] else "NO"}
    rows = [r for r in rows if r["run_id"] != run["run_id"]] + [row]
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)


def _save(root, run):
    runs_dir, _ = _paths(root)
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir / f"{run['run_id']}.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    _write_csv_row(root, run)


def load(run_id, root=ROOT):
    return json.loads((_paths(root)[0] / f"{run_id}.json").read_text(encoding="utf-8"))


def next_run_id(root=ROOT, date=None):
    date = date or datetime.date.today().isoformat()
    runs_dir, _ = _paths(root)
    stamp = date.replace("-", "")
    n = len(list(runs_dir.glob(f"RUN-{stamp}-*.json"))) + 1 if runs_dir.exists() else 1
    return f"RUN-{stamp}-{n:03d}"


def new_run(goal, venture, playbook, plan=None, root=ROOT, date=None):
    date = date or datetime.date.today().isoformat()
    run_id = next_run_id(root, date)
    steps = [{"id": s["id"], "agent": s["agent"], "status": "pending", "retries": 0, "output": None, "note": None}
             for s in (plan or {}).get("steps", [])]
    run = {"run_id": run_id, "date": date, "goal": goal, "venture": venture, "playbook": playbook,
           "status": "running", "needs_joaquin": False, "waves": (plan or {}).get("waves", []),
           "steps": steps, "escalations": []}
    _save(root, run)
    return run


def update_step(run_id, step_id, status, output=None, note=None, retry=False, root=ROOT):
    run = load(run_id, root)
    step = next((s for s in run["steps"] if s["id"] == step_id), None)
    if step is None:
        raise KeyError(f"{run_id} has no step {step_id}")
    step["status"] = status
    if output:
        step["output"] = output
    if note:
        step["note"] = note
    if retry:
        step["retries"] += 1
    if status == "escalated":
        run["needs_joaquin"] = True
        run["escalations"].append({"step": step_id, "note": note})
    _save(root, run)
    return run


def finish(run_id, status, needs_joaquin=None, root=ROOT):
    run = load(run_id, root)
    run["status"] = status
    if needs_joaquin is not None:
        run["needs_joaquin"] = needs_joaquin
    _save(root, run)
    return run


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("--goal", required=True)
    n.add_argument("--venture", required=True)
    n.add_argument("--playbook", required=True)
    n.add_argument("--plan")
    n.add_argument("--date")
    s = sub.add_parser("step")
    s.add_argument("run_id")
    s.add_argument("step_id")
    s.add_argument("status")
    s.add_argument("--output")
    s.add_argument("--note")
    s.add_argument("--retry", action="store_true")
    f = sub.add_parser("finish")
    f.add_argument("run_id")
    f.add_argument("status")
    f.add_argument("--needs-joaquin", action="store_true")
    sh = sub.add_parser("show")
    sh.add_argument("run_id")
    a = ap.parse_args()
    if a.cmd == "new":
        plan = json.load(open(a.plan)) if a.plan else None
        print(json.dumps(new_run(a.goal, a.venture, a.playbook, plan, date=a.date), indent=2))
    elif a.cmd == "step":
        print(json.dumps(update_step(a.run_id, a.step_id, a.status, a.output, a.note, a.retry), indent=2))
    elif a.cmd == "finish":
        print(json.dumps(finish(a.run_id, a.status, True if a.needs_joaquin else None), indent=2))
    else:
        print(json.dumps(load(a.run_id), indent=2))
