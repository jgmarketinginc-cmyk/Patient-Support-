"""Tests for the Chief of Staff scripts. Run:  python -m unittest discover -s tests -v

Uses a temp copy of config/ (and the agent files) for the extensibility test so the repo is untouched.
"""
import csv
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "execution"))

import check_handoff  # noqa: E402
import plan_run  # noqa: E402
import route_request  # noqa: E402
import run_state  # noqa: E402
import team_status  # noqa: E402
from cos_common import callable_agent  # noqa: E402


def route(text, root=REPO):
    return route_request.route(text, root)


class RouteTests(unittest.TestCase):
    def test_sourcing_goes_to_aaron(self):
        r = route("find 50 NJ city clerks")
        self.assertEqual((r["mode"], r["owner"], r["needs_joaquin"]), ("agent", "Aaron", False))

    def test_post_call_playbook(self):
        r = route("write the follow-up email for the Hamilton call")
        self.assertEqual((r["mode"], r["owner"]), ("playbook", "post-call"))

    def test_run_the_day(self):
        self.assertEqual(route("run the day")["owner"], "daily-outbound")

    def test_ambiguous_request_escalates(self):
        r = route("hello there")
        self.assertTrue(r["needs_joaquin"])
        self.assertEqual(r["owner"], "-")

    def test_off_phase_service_escalates(self):
        r = route("pitch document intake to a prospect")
        self.assertEqual((r["task_type"], r["mode"], r["needs_joaquin"]), ("off_phase_service_request", "escalate", True))

    def test_unbuilt_agent_escalates(self):
        tmp = _unbuilt_repo("Vicky")
        try:
            r = route("ask Vicky to handle it", tmp)
            self.assertTrue(r["needs_joaquin"])
            self.assertTrue(any("registered but not built" in x for x in r["reasons"]))
        finally:
            shutil.rmtree(tmp)

    def test_role_keywords_route_to_the_right_agent_and_escalate_when_unbuilt(self):
        expected = {
            "translate this welcome email into Spanish": "Angelina",
            "write a press release on the Camden win": "Jerry",
            "build the client training library videos": "Maya",
            "script a viral scripture reel": "Vicky",
        }
        tmp = _unbuilt_repo("Vicky", "Jerry", "Maya", "Angelina")
        try:
            for text, owner in expected.items():
                live = route(text)                                           # real authority.md: shadow, callable
                self.assertEqual((live["owner"], live["needs_joaquin"]), (owner, False), text)
                gated = route(text, tmp)                                     # same request when not built
                self.assertEqual(gated["owner"], owner, text)
                self.assertTrue(gated["needs_joaquin"], text)
                self.assertTrue(any("registered but not built" in x for x in gated["reasons"]), text)
        finally:
            shutil.rmtree(tmp)

    def test_wrong_or_other_venture_escalates_without_inventing(self):
        for text in ("draft the NJ EDA grant narrative", "update the Pathfinder roadmap"):
            r = route(text)
            self.assertEqual(r["mode"], "escalate", text)
            self.assertTrue(r["needs_joaquin"], text)
            self.assertNotEqual(r["venture"], "aiab", text)

    def test_joaquin_only_matter_escalates_even_when_owner_is_clear(self):
        r = route("move Patty's send cap to 350")
        self.assertEqual(r["owner"], "Patty")
        self.assertTrue(r["needs_joaquin"])
        self.assertTrue(r["joaquin_matters"])

    def test_chief_of_staff_decides_rework_without_escalating(self):
        r = route("re-run Cody's copy for the Tier A records that failed the gate")
        self.assertEqual(r["owner"], "Cody")
        self.assertFalse(r["needs_joaquin"])
        self.assertTrue(r["cos_decides"])


class PlanTests(unittest.TestCase):
    def test_post_call_waves_and_parallel_group(self):
        p = plan_run.plan("post-call", {"transcript": "t", "apollo_contact_id": "A-1"}, REPO)
        self.assertTrue(p["ready"], p["blocking"])
        self.assertEqual(p["waves"], [["s1"], ["s2", "s3"], ["s4", "s5"], ["s6"]])   # Cody||Dolly in one wave

    def test_missing_required_input_blocks(self):
        p = plan_run.plan("post-call", {}, REPO)
        self.assertFalse(p["ready"])
        self.assertTrue(any("missing required inputs" in b for b in p["blocking"]))

    def test_fan_out_expands_per_record_and_respects_cap(self):
        p = plan_run.plan("daily-outbound", {"records": [f"r{i}" for i in range(8)]}, REPO)
        cody_waves = [w for w in p["waves"] if any(s.startswith("s4.") for s in w)]
        self.assertEqual([len(w) for w in cody_waves], [6, 2])                       # cap of 6 per turn
        self.assertTrue(all(len(w) <= plan_run.MAX_PARALLEL for w in p["waves"]))

    def test_pending_playbook_stub_is_blocked(self):
        p = plan_run.plan("njeda-stub", {}, REPO)
        self.assertFalse(p["ready"])

    def test_unbuilt_agent_in_playbook_blocks(self):
        tmp = _unbuilt_repo("Vicky")
        try:
            _append(tmp / "config/playbooks.md", """
## playbook: needs-vicky
- venture: aiab
- trigger: test
- required_inputs: none
- stop_conditions: none

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | Vicky | - | - | - | x | y | - |
""")
            p = plan_run.plan("needs-vicky", {}, tmp)
            self.assertFalse(p["ready"])
            self.assertTrue(any("registered but not built" in b for b in p["blocking"]))
        finally:
            shutil.rmtree(tmp)


class HandoffTests(unittest.TestCase):
    def test_real_frannie_note_passes_frannie_mark(self):
        text = (REPO / "outputs/shadow/2026-10-08/frannie/S1-note.md").read_text()
        self.assertTrue(check_handoff.check("frannie-mark", text)["pass"])

    def test_missing_field_fails_gate(self):
        text = "Qualified. Apollo SAMPLE-APOLLO-001. Pain (00:48). Decision-maker is Dana.\n\n## Sources / Assumptions\nx"
        res = check_handoff.check("frannie-mark", text)
        self.assertFalse(res["pass"])
        joined = " ".join(res["failed"])
        self.assertIn("objections", joined)
        self.assertIn("escalation_items", joined)

    def test_price_above_entry_in_email_body_fails(self):
        text = "Hi Dana,\nThe install is $18,000.\n\n## Sources / Assumptions\nx"
        res = check_handoff.check("frannie-cody", text)
        self.assertFalse(res["pass"])
        self.assertIn("no_price_above_entry", " ".join(res["failed"]))

    def test_negation_in_assumptions_note_is_not_flagged(self):
        text = "Hi Dana,\nThanks.\n\n## Sources / Assumptions\nNo discount, no price above $1,500."
        self.assertTrue(check_handoff.check("frannie-cody", text)["pass"])

    def test_cody_patty_json_contract(self):
        good = {"prospect_id": "p1", "emails": ["a", "b", "c"], "linkedin_note": "n", "sender": "s",
                "footer_ref": "config/footer.md", "sources_assumptions": "x Sources / Assumptions"}
        self.assertTrue(check_handoff.check("cody-patty", json.dumps(good))["pass"])
        bad = dict(good, emails=["a", "b"])
        self.assertFalse(check_handoff.check("cody-patty", json.dumps(bad))["pass"])

    def test_unknown_contract(self):
        self.assertFalse(check_handoff.check("nope", "x")["pass"])


class RunStateTests(unittest.TestCase):
    def test_run_lifecycle_and_csv(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            plan = plan_run.plan("post-call", {"transcript": "t", "apollo_contact_id": "A"}, REPO)
            run = run_state.new_run("debrief", "aiab", "post-call", plan, root=tmp, date="2026-10-08")
            self.assertEqual(run["run_id"], "RUN-20261008-001")
            run_state.update_step(run["run_id"], "s1", "passed", output="x", root=tmp)
            run_state.update_step(run["run_id"], "s2", "escalated", note="contract ask", root=tmp)
            run_state.finish(run["run_id"], "escalated", root=tmp)
            with open(tmp / "logs/cos-log.csv") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 1)
            self.assertEqual((rows[0]["steps_done"], rows[0]["needs_joaquin"], rows[0]["status"]), ("1", "YES", "escalated"))
            self.assertEqual(run_state.next_run_id(tmp, "2026-10-08"), "RUN-20261008-002")
        finally:
            shutil.rmtree(tmp)


class StatusTests(unittest.TestCase):
    def test_shadow_log_rows_all_have_six_fields(self):
        """A hand-written row with an unquoted comma shifts the columns and hides pending items from team_status."""
        with open(REPO / "logs/shadow-log.csv", newline="") as f:
            bad = [i for i, row in enumerate(csv.reader(f), 1) if len(row) != 6]
        self.assertEqual(bad, [], f"malformed shadow-log rows (quote any item that contains a comma): {bad}")

    def test_rollup_lists_all_registered_agents(self):
        rows = {r["agent"]: r for r in team_status.status(REPO)}
        registered = {"Aaron", "Cody", "Patty", "Frannie", "Mark", "Dolly", "Vicky", "Angelina", "Jerry", "Maya"}
        self.assertTrue(registered <= set(rows))          # all ten registered agents, plus any logger such as the Chief of Staff
        self.assertTrue(rows["Frannie"]["callable"])
        self.assertTrue(rows["Vicky"]["callable"])                         # Phase 3 rows are shadow since 2026-10-08
        tmp = _unbuilt_repo("Vicky")
        try:
            self.assertFalse({r["agent"]: r for r in team_status.status(tmp)}["Vicky"]["callable"])
        finally:
            shutil.rmtree(tmp)


class ExtensibilityTests(unittest.TestCase):
    """Adding an agent is config only: registry + authority + agent file + routing + playbook rows. No code change."""

    def test_new_agent_routes_with_no_code_change(self):
        tmp = _copy_repo()
        try:
            self.assertFalse(callable_agent("Zed", tmp)[0])
            _append(tmp / "config/agent-registry.md", "")
            reg = tmp / "config/agent-registry.md"
            reg.write_text(reg.read_text().replace(
                "\n## Handoff contracts",
                "| Zed | 3 | Test agent | .claude/agents/zed.md | sops/zed-sop.md | test |\n\n## Handoff contracts"))
            auth = tmp / "config/authority.md"
            auth.write_text(auth.read_text().replace(
                "\n## Patty post-exit ramp", "| Zed | 3 | shadow | 2026-10-09 | 0/10 | 0 | NO |\n\n## Patty post-exit ramp"))
            (tmp / ".claude/agents/zed.md").write_text("---\nname: zed\n---\n")
            rt = tmp / "config/routing.md"
            rt.write_text(rt.read_text().rstrip("\n") + "\n| zed_task | aiab | zebra stripes | Zed | agent | 30 | NO |\n")
            _append(tmp / "config/playbooks.md", """
## playbook: zed-then-cody
- venture: aiab
- trigger: test
- required_inputs: none
- stop_conditions: none

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | Zed | - | - | - | x | y | - |
| s2 | Cody | s1 | - | - | y | z | - |
""")
            self.assertTrue(callable_agent("Zed", tmp)[0])
            r = route("check the zebra stripes", tmp)
            self.assertEqual((r["mode"], r["owner"], r["needs_joaquin"]), ("agent", "Zed", False))
            p = plan_run.plan("zed-then-cody", {}, tmp)
            self.assertTrue(p["ready"], p["blocking"])
            self.assertEqual(p["waves"], [["s1"], ["s2"]])
        finally:
            shutil.rmtree(tmp)


class Phase3ActivationTests(unittest.TestCase):
    """The four Phase 3 agents have files, SOPs and (since 2026-10-08) shadow rows in config/authority.md."""

    def test_files_exist_and_agents_are_callable_in_shadow(self):
        for name in ("vicky", "angelina", "jerry", "maya"):
            self.assertTrue((REPO / f".claude/agents/{name}.md").exists(), name)
            self.assertTrue((REPO / f"sops/{name}-sop.md").exists(), name)
            ok, why = callable_agent(name.title(), REPO)
            self.assertTrue(ok, why)
        p = plan_run.plan("spanish-outreach", {"cody_json": "x"}, REPO)
        self.assertTrue(p["ready"], p["blocking"])
        self.assertEqual(p["waves"], [["s1"], ["s2"]])

    def test_not_built_rows_block_them_until_joaquin_flips_the_flag(self):
        tmp = _unbuilt_repo("Vicky", "Jerry", "Maya", "Angelina")
        try:
            for n in ("Vicky", "Jerry", "Maya", "Angelina"):
                self.assertFalse(callable_agent(n, tmp)[0], n)
            self.assertFalse(plan_run.plan("spanish-outreach", {"cody_json": "x"}, tmp)["ready"])
        finally:
            shutil.rmtree(tmp)


def _unbuilt_repo(*names):
    """Temp copy of the repo where the named agents read 'not built' in config/authority.md."""
    tmp = _copy_repo()
    auth = tmp / "config/authority.md"
    text = auth.read_text()
    for n in names:
        text = re.sub(rf"\| {n} \| 3 \| shadow \|[^\n]*", f"| {n} | 3 | not built | - | - | - | NO |", text)
    auth.write_text(text)
    return tmp


def _copy_repo():
    tmp = Path(tempfile.mkdtemp())
    shutil.copytree(REPO / "config", tmp / "config")
    shutil.copytree(REPO / ".claude", tmp / ".claude")
    return tmp


def _append(path, text):
    path.write_text(path.read_text() + text)


if __name__ == "__main__":
    unittest.main()
