# Playbooks

Named multi-agent workflows the Chief of Staff conducts. Read by `execution/route_request.py` and `execution/plan_run.py`. Built from `/runbook/RUNBOOK.md`; nothing here is invented. Add a playbook by copying a block; add an agent by following `/docs/adding-an-agent.md`.

Format per playbook: a `## playbook: <name>` heading, bullet metadata, then one table.
- `Agent` is a name from `/config/agent-registry.md`, or `COS` for steps the Chief of Staff does itself (assembling, consolidating).
- `Depends on` lists step IDs (`-` = none). Steps with the same dependencies and no ordering between them run in parallel (max 6 per wave).
- `Condition` is `-` or a short condition the conductor checks before running the step.
- `Repeat` is `-` or `per:<input>`: one call per item in that input list.
- `Gate` is a contract name from `/config/handoff-contracts.md`, or `-`.
- Cell delimiter is ` | ` (with spaces); a bare `|` inside a cell is regex alternation.

Every step also passes the receiving agent's own hard rules (its agent file). Failing a gate: one rework with the specific defect, then halt that branch and escalate.

## playbook: daily-outbound
- venture: aiab
- trigger: runbook daily schedule (Mon-Fri), or "run the day"
- required_inputs: none
- stop_conditions: capacity_tomorrow is 0 (no list); list quality under 90% verified; any critical error; any domain-level pause

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | Aaron | - | - | - | Niche A/B filters (Modes 1 and 2: source, scrub, score) | Tiered records in Apollo pool, trigger lines on Tier A | - |
| s2 | Patty | - | - | - | Apollo inbox warm/health status | capacity_tomorrow and inbox health | patty-aaron |
| s3 | Aaron | s1,s2 | - | - | capacity_tomorrow, scheduled follow-ups (Mode 3) | Send list for the next business day, never over capacity | - |
| s4 | Cody | s3 | new Tier A/B records only | per:records | One Aaron-scored record with trigger line | Sequence JSON (3 emails + LinkedIn note) | cody-patty |
| s5 | Patty | s4 | - | - | Cody JSON + send list | Re-verified emails staged in Apollo sequences across healthy inboxes | - |
| s6 | Patty | s5 | - | - | Apollo stats | Evening dashboard (Slack + Telegram per runbook) | - |

## playbook: post-call
- venture: aiab
- trigger: call ends or transcript arrives, or "debrief the call"
- required_inputs: transcript, apollo_contact_id
- stop_conditions: contract request, custom or municipal contract, discount request, out-of-menu ask, ready to buy (Mark also runs); any critical error

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | Frannie | - | - | - | Transcript or notes + Apollo contact | One-page coach note, objection log, next-step email draft, staged Apollo update | frannie-mark |
| s2 | Mark | s1 | Frannie marks the call qualified or ready to buy | - | Frannie note and analysis, discovery notes | Proposal outline, 3 options, ROI table, timeline, terms, briefs for Cody and Dolly | - |
| s3 | Cody | s1 | - | - | Frannie next-step email draft | Polished next-step email (footer from /config/footer.md) | frannie-cody |
| s4 | Cody | s2 | s2 ran | - | Mark narrative brief | Proposal narrative | mark-cody |
| s5 | Dolly | s2 | s2 ran | - | Mark visual brief | Primary + alternate asset, editable source | mark-dolly |
| s6 | COS | s3,s4,s5 | - | - | All step outputs | Consolidated package for Joaquin's approval | - |

## playbook: weekly-review
- venture: aiab
- trigger: Sunday evening, or "run the week"
- required_inputs: none
- stop_conditions: any critical error

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | Frannie | - | - | - | The week's calls | weekly-pattern.md | - |
| s2 | Patty | - | - | - | Apollo stats for the week | Weekly campaign metrics | patty-aaron |
| s3 | Aaron | s1,s2 | - | - | All agents' metrics (Mode 4) | One-page Monday memo (worst metric, one fix, the one thing not to do) | - |

## playbook: pre-call-brief
- venture: aiab
- trigger: "pre-call brief" request
- required_inputs: apollo_contact_id
- stop_conditions: none

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | Aaron | - | - | - | Apollo contact | One-page pre-call brief | - |

## playbook: escalation
- venture: aiab
- trigger: any agent raises a runbook escalation, or a Joaquin-only matter appears mid-run
- required_inputs: escalation_text
- stop_conditions: none (this playbook ends at Joaquin)

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | COS | - | - | - | Escalation text, /config/decision-rights.md | Classification: Chief of Staff decides or Joaquin decides | - |
| s2 | COS | s1 | Joaquin decides | - | Classification | One consolidated escalation message (shadow: "N drafts ready for review" only; no prospect data leaves the system) | - |

## playbook: spanish-outreach
- venture: aiab
- trigger: Joaquin approves Spanish outreach for municipal contacts with Hispanic leadership, or "translate the sequence for ..."
- required_inputs: cody_json
- stop_conditions: Spanish opt-out wording not approved; no native-speaker reviewer named; list not approved by Joaquin; any critical error

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | Angelina | - | Cody JSON already passed its assembler PASS | - | Approved English sequence JSON (Cody) | Spanish sequence JSON, glossary, flags; translation_check PASS | angelina-patty |
| s2 | Patty | s1 | Joaquin approved the Spanish opt-out wording, the reviewer and the list | - | Spanish JSON + send list | Re-verified emails staged (shadow: draft only) | - |

## playbook: client-training
- venture: aiab
- trigger: an install reaches build phase or delivery, or "build the training library for ..."
- required_inputs: scope_outline, install_notes
- stop_conditions: a module covers a feature not delivered; any critical error

| Step | Agent | Depends on | Condition | Repeat | Input | Output | Gate |
|---|---|---|---|---|---|---|---|
| s1 | Maya | - | - | - | Signed-scope outline (Mark) + install notes | Six core module scripts, shot lists, reference materials; course_check PASS | - |
| s2 | Angelina | s1 | client staff need Spanish and Joaquin approved | - | Approved module scripts | Spanish module scripts; translation_check PASS | - |
| s3 | COS | s1,s2 | - | - | All outputs | Recording package for Joaquin (order, shot lists) | - |

## playbook: vault-stub
- venture: vault
- trigger: [PENDING: Joaquin]
- required_inputs: [PENDING: Joaquin]
- stop_conditions: [PENDING: Joaquin]

No steps defined. Requests for this venture escalate to Joaquin.

## playbook: pathfinder-stub
- venture: pathfinder
- trigger: [PENDING: Joaquin]
- required_inputs: [PENDING: Joaquin]
- stop_conditions: [PENDING: Joaquin]

No steps defined. Requests for this venture escalate to Joaquin.

## playbook: njeda-stub
- venture: njeda
- trigger: [PENDING: Joaquin]
- required_inputs: [PENDING: Joaquin]
- stop_conditions: all funder-facing material is draft-only and Joaquin-approved

No steps defined. Requests for this venture escalate to Joaquin.
