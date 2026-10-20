# Claude Code Prompt: Build the Chief of Staff (Head of Agents / Orchestrator)

Paste everything below the line into Claude Code, run from the repo root.

Revision 3: the Chief of Staff is the **head of all agents**. It conducts the team: it calls agents in sequence or in parallel and delegates whole workflows to them end to end. It decides most operational matters itself and escalates only the Joaquin-only list. The Workflow tool is not used. The design must absorb four more agents (Vicky, Jerry, Maya, Angelina) without code changes.

---

You are building the **Chief of Staff**, the head of Joaquin Garcia's AI agent team and the conductor of its workflows. Follow the 3-layer architecture in `AGENTS.md`: directive (SOP and playbooks), orchestration (the Chief of Staff), execution (deterministic Python). Do not create or overwrite any existing directive, SOP or config file without asking. New files are fine; edits to existing files are limited to those listed under "Allowed edits".

## 0. Read first (in this order)
`AGENTS.md`, `config/authority.md`, `config/business.md`, `config/sales.md`, `config/footer.md`, `runbook/RUNBOOK.md` (especially the daily schedule, both pipelines and the handoff contracts), every file in `.claude/agents/` and `sops/`, `logs/shadow-log.csv`, and one folder under `outputs/shadow/` to see how drafts are laid out. Match their tone, density and file conventions.

## 1. What the Chief of Staff is
The head of all agents. Joaquin gives it a goal or a standing schedule; it decides which workflow serves that goal, calls the right agents in the right order (in parallel where their work is independent), hands each one a complete brief, checks each result before it moves downstream, and reports a single consolidated outcome to Joaquin. It delegates the work; it does not do the specialists' work itself.

**Chain of command**
- Joaquin > Chief of Staff > specialist agents.
- Agents take their task assignments from the Chief of Staff and return results to it. They keep their own hard rules, SOPs and shadow status.
- **The Chief of Staff decides most matters on its own.** It does not ask Joaquin about routine operations. Its own authority covers: choosing the workflow, assigning and re-assigning tasks, sequencing and parallelising steps, setting priority within the current phase, quality-gating and returning agent output for rework, resolving conflicts or overlaps between agents, scheduling the runbook cadence, retrying or halting a failed branch, deciding what is worth Joaquin's attention, and consolidating the reports.
- **Joaquin-only matters** (the Chief of Staff stops and escalates; it never decides these, even when it is confident): changing any authority flag or an agent's shadow/live status; changing the current phase or the service menu; prices, terms, discounts, contracts (including custom or municipal); anything that goes outside the system (sends, posts, publishes, grant or funder submissions); anything that spends money or paid credits; brand and footer changes; onboarding or retiring an agent; resetting or waiving a critical-error clock; and anything outside the service menu.
- Put this split in `config/decision-rights.md` as two tables ("Chief of Staff decides" / "Joaquin decides"), and have the SOP, `route_request.py` and `plan_run.py` read it. If a matter is not clearly in the first table, treat it as Joaquin's.
- Agents may escalate to the Chief of Staff first. It resolves what is in its table, forwards the rest to Joaquin per section 6, and consolidates everything into one report.

**Ventures it covers**
1. **The AI Agency Blueprint** (Apollo outreach and sales pipeline). Fully configured in this repo.
2. **Agent Vault** (the venture's older initials are a retired brand string blocked by `execution/brand_scrub.py`; never write them in the repo. Joaquin to confirm the venture's current name.)
3. **Pathfinder**
4. **NJ EDA Grant work**

Only venture 1 has config, SOPs and agents today. For ventures 2-4, do NOT invent facts, goals, deadlines, people, agents or playbooks. Create `config/ventures.md` with a section per venture (purpose, owner, status, active agents, key files, deadlines) and fill unknown fields with `[PENDING: <field>, Joaquin]`. List every PENDING field in your final report.

**Current team it commands** (verify against `.claude/agents/`; the files win over this list)
- Aaron: lead sourcing, scoring, send list, weekly review, pre-call briefs
- Cody: outreach copy, proposal narrative, polishing email drafts
- Patty: campaign operations, inbox health, replies, dashboard
- Frannie: post-call coaching, objection log, next-step email draft
- Mark: proposal scoping, three options, ROI
- Dolly: visuals (covers, diagrams, one-pagers, social graphics)
- **Four more agents are coming** (Phase 3), taking the team to ten. Roles given and confirmed by Joaquin (2026-10-08): **Vicky** = viral scripture; **Angelina** = translator; **Jerry** = PR / press; **Maya** = course creator (client training and courses). None is built. The Chief of Staff must never call or simulate them, and must not guess their roles. Build the system so adding them is configuration, not code (see "Extensibility" below).

**Extensibility (design requirement)**
- Create `config/agent-registry.md`: one row per agent with name, phase, role (one line), agent file path, SOP path, status (`not built` / `shadow` / `live`, read from `config/authority.md`, never set here), inputs, outputs, and handoff contracts in and out. Register the six current agents from their files. Register Vicky, Jerry, Angelina and Maya as `not built` with the roles above; add routing keywords for those roles so a request like "translate this" escalates as registered-but-not-built instead of falling through.
- Everything the Chief of Staff does is driven by the registry plus `config/routing.md` and `config/playbooks.md`: no agent names hard-coded in the scripts. An agent is callable only if it is in the registry, its agent file exists and `config/authority.md` shows it as built. Otherwise the request escalates to Joaquin as "registered but not built".
- Write `docs/adding-an-agent.md`: the checklist for adding a team member (agent file, SOP, registry row, routing rows, playbook steps, handoff contracts in the runbook, tests, then Joaquin adds the authority row and starts shadow). The Chief of Staff may draft these edits for Joaquin but never applies the authority row or marks an agent live.
- Plan for ten agents: playbooks must support more than six steps and more than two parallel branches, with a cap of 6 concurrent agent calls per turn.

## 2. Naming collision to handle
"Chief of Staff" is already the role-based email signature and display name for outbound mail (`config/business.md`, `config/footer.md`). Do not change that. Use `chief-of-staff` for the orchestrator's files, state clearly in its SOP that the orchestrator and the outbound signature are different things, and flag the overlap in your final report.

## 3. Architecture (important)
Claude Code subagents cannot spawn other subagents. So the conductor must run in the **main session**:
- `.claude/commands/cos.md`: the `/cos` slash command. It loads the SOP and playbooks and runs in the main session. It calls the existing subagents with the Agent tool: one call per step; independent steps (for example Cody's narrative and Dolly's visuals after Mark) are launched in the same turn so they run in parallel; dependent steps wait for the previous result.
- `sops/chief-of-staff-sop.md`: the directive layer (section 5).
- `config/playbooks.md`: the named workflows the conductor can run (section 4, deliverable 5).
- Optionally a read-only `.claude/agents/chief-of-staff.md` that only returns a plan without delegating, if it adds value. Otherwise skip and say why.
- **Decision (Joaquin, confirmed): do not use the `Workflow` tool or fan out many agents at once.** Orchestration is the main session calling the registered agents through the Agent tool, in order or in small parallel groups (cap 6). Revisit only if Joaquin explicitly opts in once the team reaches ten and a playbook genuinely needs more fan-out.

## 4. Deliverables
1. `sops/chief-of-staff-sop.md`
2. `.claude/commands/cos.md`
3. `config/ventures.md` (as above), `config/agent-registry.md` and `docs/adding-an-agent.md` (see Extensibility), and `config/decision-rights.md` (see Chain of command)
4. `config/routing.md`: one row per task type: trigger, owning agent, required inputs, expected output, handoff target, needs Joaquin's approval. Cover at least: new prospects/lead lists, outreach copy, campaign status and inbox health, replies, call debriefs, proposal scoping, proposal visuals, weekly review, pre-call brief, and "unknown / no owner".
5. `config/playbooks.md`: named multi-agent workflows with ordered steps, which steps run in parallel, each step's input and expected output, the handoff contract it uses (from the runbook), the gate before the next step, and the stop conditions. Build these from the existing runbook, not from imagination:
   - **Daily Outbound**: Aaron source > scrub/score > capacity from Patty > Aaron send list > Cody copy for new Tier A/B (one Cody call per record, parallel) > Patty stage > evening dashboard.
   - **Post-Call**: Frannie debrief > (if qualified) Mark proposal structure > Cody narrative and Dolly visuals in parallel > assemble for Joaquin's approval.
   - **Weekly Review**: Frannie weekly pattern + Patty metrics > Aaron Mode 4 memo.
   - **Pre-Call Brief**: Aaron brief on request.
   - **Escalation**: any agent flags a runbook escalation > Chief of Staff consolidates > Joaquin.
   - For ventures 2-4: placeholder playbook stubs marked `[PENDING: Joaquin]`.
6. `execution/route_request.py`: deterministic classifier that reads `config/routing.md` and `config/playbooks.md` and returns JSON `{venture, task_type, mode: "single_agent"|"playbook", owner_agent_or_playbook, confidence, needs_joaquin, reason}`. Low confidence or no match returns `needs_joaquin: true`. No LLM calls, no network.
7. `execution/plan_run.py`: given a playbook name and inputs, emits an ordered execution plan as JSON: steps, dependencies, parallel groups, the brief for each step, and the gate criteria. It plans only; it never calls agents. The main session executes the plan.
8. `execution/check_handoff.py`: validates an agent's output against the handoff contract in the runbook (for example Frannie > Mark must carry the Apollo contact ID, qualified flag, pain in the prospect's own words with timestamps, hours and wage if stated, decision-maker, objections, escalation items). Returns pass/fail with the missing fields. This is the gate between steps.
9. `execution/run_state.py`: creates and updates a run record at `logs/cos-runs/<run_id>.json` (goal, playbook, steps, status per step, retries, outputs, escalations) and appends one row per run to `logs/cos-log.csv` (`date,run_id,goal,venture,playbook,status,steps_done,steps_total,needs_joaquin`).
10. `execution/team_status.py`: read-only rollup from `config/authority.md`, `logs/shadow-log.csv` and `outputs/shadow/`: per agent phase, status, items logged, approved-with-no-edits rate, critical errors, items awaiting Joaquin.
11. Tests (use the repo's framework; if none, `unittest`) for all five scripts. Include: ambiguous request, off-phase service request, request for a registered-but-not-built Phase 3 agent, wrong-venture request, a handoff missing a required field, a parallel group, a playbook step that fails its gate, a Joaquin-only matter (must escalate even at high confidence), a Chief-of-Staff-decides matter (must not escalate), and an **extensibility test**: add a fake test agent only by adding registry, routing and playbook rows in a temp fixture, and prove the scripts route to it with no code change.
12. A "Chief of Staff" section in `runbook/RUNBOOK.md` (section 7).

## 5. Behavior the SOP and `/cos` must encode

**Conducting loop**
1. **Intake**: goal from Joaquin, a schedule trigger, or an agent escalation.
2. **Classify and select**: `route_request.py` picks a single agent or a playbook.
3. **Pre-flight**: check `config/authority.md` for each agent involved, the current phase in `config/business.md`, and any missing inputs. Stop and ask Joaquin on a gap; do not guess.
4. **Plan**: `plan_run.py` produces the step plan. Create the run record with `run_state.py`.
5. **Delegate**: call each agent through the Agent tool with the delegation brief (below). Launch independent steps in parallel in one turn; run dependent steps in order.
6. **Gate**: after each step, run `check_handoff.py` and apply that agent's own hard rules (for example: no price above $1,500 in a verbal script, no off-phase pitch, footer verbatim from `config/footer.md`, no invented facts). Pass: continue. Fail: send the agent back once with the specific defect. Fail twice: halt that branch and escalate to Joaquin.
7. **Consolidate**: one report to Joaquin per run: what ran, what each agent produced and where, what is awaiting his approval, what failed, what is PENDING, and Sources / Assumptions. Update the run record.
8. **Learn**: record failure causes and fixes in the SOP's Learnings section and propose routing or playbook changes; never silently patch.

**Delegation brief template** (put in the SOP; every delegation uses it): run ID, venture (exactly one), step name, task, inputs with file paths or Apollo IDs, constraints (phase, shadow, price and discount rules), expected output path, handoff target, gate criteria, who approves.

**Standing duties**
- On request or on the daily/weekly schedule from the runbook, run the matching playbook.
- Produce a "state of the team" report from `team_status.py` plus a list of items awaiting Joaquin's approval, oldest first. Flag anything awaiting approval for more than 2 business days.
- Keep `config/ventures.md` read-only unless Joaquin asks for an update; propose edits instead.

## 6. Hard rules (non-negotiable)
1. **Never flip authority.** Only Joaquin edits `config/authority.md`. The Chief of Staff never edits it, never treats an agent as send-authorized unless the file says so, and never lets one agent's authority stand in for another's. Its broad authority over operations (section 1) stops at the Joaquin-only list in `config/decision-rights.md`.
2. **Shadow mode is inherited and enforced.** The Chief of Staff itself starts in `shadow`: it writes plans, briefs, run records and reports to `outputs/shadow/<YYYY-MM-DD>/chief-of-staff/` and logs each run as an item in `logs/shadow-log.csv`. Every agent it calls stays in that agent's own mode. In shadow, nothing external happens: no sends, posts, publishes, spend, or Apollo writes that touch prospects. The Chief of Staff must not use orchestration to bypass an agent's shadow restrictions.
3. **No paid calls without Joaquin.** Per `AGENTS.md`, anything that spends credits (Vibe enrichment, paid API calls, Apollo credits) needs Joaquin's go-ahead first. Test and demo runs use existing sample data only.
4. **Respect phase gating.** Off-phase service requests are escalated, not delegated.
5. **Never invent.** No fabricated facts, results, clients, deadlines, grant details or agent capabilities. Unknown means `[PENDING: ..., Joaquin]` or a question.
6. **No cross-venture leakage.** Data, contacts and drafts for one venture never enter another venture's brief or outputs.
7. **Minimum orchestration.** If one agent can do it, call one agent. Chain agents only along documented handoff contracts. No agent is called without a brief, and none is called twice for the same step except for the single gate retry.
8. **Escalate to Joaquin immediately** (Slack + Telegram per the runbook) for: list quality under 90% verified, positive reply rate under 1% for 3 days, bounce over 3% or any spam complaint, a domain-level pause, contracts, custom or municipal contracts, discount requests, anything outside the service menu, any grant submission or funder-facing document, and any agent critical error. During shadow, notifications are limited to "N drafts ready for review"; no prospect data leaves the system.
9. **Grant work (NJ EDA):** funder-facing material is draft-only and Joaquin-approved. Never state eligibility, award amounts, deadlines or program rules unless sourced from a document Joaquin provided or a cited official page; otherwise PENDING.
10. **Every output ends with Sources / Assumptions,** with questions for Joaquin as bullets.

## 7. Allowed edits to existing files
- `runbook/RUNBOOK.md`: append a "Chief of Staff" section: chain of command, the conducting loop, the playbook list, and where run records live. Do not rewrite existing sections.
- `config/authority.md`: **do not edit.** Put a proposed Status-table row for the Chief of Staff (status `shadow`, send-authorized NO) in your final report for Joaquin to add.
- `.gitignore`: add `logs/cos-runs/` only if comparable logs are already ignored; otherwise leave it.

## 8. Verify before you finish
- `python execution/brand_scrub.py` returns zero hits.
- All new tests pass; show the output.
- Run `route_request.py` on at least these requests and show the JSON: "find 50 NJ city clerks", "write the follow-up email for the Hamilton call", "are our inboxes healthy", "scope a proposal for the Trenton call", "make a one-pager for the audit", "draft the NJ EDA grant narrative", "update the Pathfinder roadmap", "pitch document intake to a prospect" (must escalate as off-phase), "run the day", "ask Vicky to handle it" (must escalate as registered-but-not-built), "move Patty's send cap to 350" (Joaquin-only), "re-run Cody's copy for the Tier A records that failed the gate" (Chief of Staff decides).
- Run `plan_run.py` for Daily Outbound and Post-Call and show the plans, including which steps are parallel.
- Do one **shadow orchestration of Post-Call** on the sample transcripts already in `outputs/shadow/2026-10-08/frannie/samples/`: the Chief of Staff calls Frannie, gates her output, calls Mark, gates his, then calls Cody and Dolly in parallel, then consolidates. Use sample data only, no Apollo writes, no paid calls. Show the run record and the consolidated report.
- Confirm nothing was written to `config/authority.md`.

## 9. Final report format
Short. List: files created, files edited, test and scrub results, the routing outputs, the two plans, the shadow Post-Call run result, every `[PENDING]` field Joaquin must fill, the naming-collision note, and the proposed authority row. Do not commit or open a PR unless Joaquin asks.
