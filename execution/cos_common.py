#!/usr/bin/env python3
"""Shared readers for the Chief of Staff scripts (see sops/chief-of-staff-sop.md).

Parses the markdown tables in /config so no agent, venture or playbook name is hard-coded in code.
Every function takes `root` (default: the repo root) so tests can point at a temp copy.

Table convention: cell delimiter is " | " (space-pipe-space). A bare "|" inside a cell
(no surrounding spaces) is regex alternation and is left alone.
"""
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
CONDUCTOR = {"cos", "chief of staff"}   # step agents the conductor performs itself


def read(root, rel):
    return (Path(root) / rel).read_text(encoding="utf-8")


def _cells(line):
    inner = line.strip()
    if not (inner.startswith("|") and inner.endswith("|")):
        return None
    inner = " " + inner[1:-1] + " "
    return [c.strip() for c in re.split(r"\s\|\s", inner)]


def parse_tables(text):
    """Return [(heading, [row dict, ...]), ...] for each markdown table, in order."""
    tables, heading, block = [], "", []

    def flush():
        if len(block) >= 2:
            header = _cells(block[0])
            rows = []
            for ln in block[2:]:
                cells = _cells(ln)
                if cells is None:
                    continue
                cells += [""] * (len(header) - len(cells))
                rows.append(dict(zip(header, cells)))
            tables.append((heading, rows))
        block.clear()

    for line in text.splitlines():
        if line.startswith("#"):
            flush()
            heading = line.lstrip("#").strip()
        elif _cells(line) is not None:
            block.append(line)
        else:
            flush()
    flush()
    return tables


def table_under(text, heading_prefix):
    for heading, rows in parse_tables(text):
        if heading.lower().startswith(heading_prefix.lower()):
            return rows
    return []


def first_table(text):
    tables = parse_tables(text)
    return tables[0][1] if tables else []


# ---- registry, authority, callability ---------------------------------------

def load_registry(root=ROOT):
    rows = first_table(read(root, "config/agent-registry.md"))
    return {r["Name"]: r for r in rows if r.get("Name")}


def load_authority(root=ROOT):
    """name -> status string, from the Status table in config/authority.md."""
    rows = table_under(read(root, "config/authority.md"), "Status")
    return {r["Agent"]: r["Status"].lower() for r in rows if r.get("Agent")}


def is_conductor(agent):
    return agent.strip().lower() in CONDUCTOR


def callable_agent(name, root=ROOT, registry=None, authority=None):
    """(ok, reason). Callable = in registry + agent file exists + authority shows shadow or live."""
    registry = registry if registry is not None else load_registry(root)
    authority = authority if authority is not None else load_authority(root)
    key = next((k for k in registry if k.lower() == name.lower()), None)
    if key is None:
        return False, f"{name} is not in config/agent-registry.md"
    status = authority.get(key, "not listed")
    if not (Path(root) / registry[key]["Agent file"]).exists():
        return False, f"registered but not built: {key} has no agent file ({registry[key]['Agent file']}); authority status: {status}"
    if not (status.startswith("shadow") or status.startswith("live")):
        return False, f"registered but not built: {key} status in config/authority.md is '{status}'"
    return True, f"{key} callable (authority status: {status})"


def registry_name(name, registry):
    return next((k for k in registry if k.lower() == name.lower()), None)


# ---- playbooks ----------------------------------------------------------------

def load_playbooks(root=ROOT):
    text = read(root, "config/playbooks.md")
    books, current = {}, None
    for line in text.splitlines():
        m = re.match(r"##\s+playbook:\s*(\S+)", line)
        if m:
            current = {"name": m.group(1), "meta": {}, "steps": [], "_lines": []}
            books[current["name"]] = current
            continue
        if line.startswith("## ") and current is not None:
            current = None
        if current is not None:
            current["_lines"].append(line)
            mm = re.match(r"-\s+([a-z_]+):\s*(.*)$", line)
            if mm:
                current["meta"][mm.group(1)] = mm.group(2).strip()
    for book in books.values():
        rows = first_table("\n".join(book.pop("_lines")))
        book["steps"] = rows
        req = book["meta"].get("required_inputs", "none")
        book["required_inputs"] = [] if req.lower() == "none" or "PENDING" in req else [r.strip() for r in req.split(",") if r.strip()]
        book["pending"] = not rows
    return books


# ---- routing, ventures, decision rights ----------------------------------------

def load_routing(root=ROOT):
    return first_table(read(root, "config/routing.md"))


def load_ventures(root=ROOT):
    return first_table(read(root, "config/ventures.md"))


def load_rights(root=ROOT):
    text = read(root, "config/decision-rights.md")
    return {
        "cos": table_under(text, "Chief of Staff decides"),
        "joaquin": table_under(text, "Joaquin decides"),
    }


def distinct_matches(pattern, text):
    """Distinct (lower-cased) match strings of `pattern` in `text`."""
    found = set()
    for m in re.finditer(pattern, text, re.I):
        if m.group(0):
            found.add(m.group(0).lower())
    return found


def current_phase(root=ROOT):
    m = re.search(r"Current phase:\s*\*\*(Phase \d+)\*\*", read(root, "config/business.md"))
    return m.group(1) if m else "[PENDING: current phase, Joaquin]"
