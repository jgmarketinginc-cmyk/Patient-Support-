# Routing Table

Read by `execution/route_request.py`. One row per task type. `Owner` is an agent name from `/config/agent-registry.md`, a playbook name from `/config/playbooks.md`, or `-` (no owner: escalate). `Mode` is `agent`, `playbook` or `escalate`. `Priority` breaks ties (higher wins). `Keywords` are `|`-separated regex fragments (case-insensitive); confidence rises with the number of keywords matched. `Needs Joaquin` is `YES` when the task type always requires him.

Rules the router applies on top of this table (see `/config/decision-rights.md`): a request naming a registered agent by name goes to that agent; a Joaquin-only matter sets `needs_joaquin` even when the owner is clear; an owner that is not callable (not in the registry, no agent file, or `not built` in `/config/authority.md`) escalates as "registered but not built"; low confidence or no match escalates.

| Task type | Venture | Keywords | Owner | Mode | Priority | Needs Joaquin |
|---|---|---|---|---|---|---|
| off_phase_service_request | aiab | document intake|inspection report|inspection and scheduling|resilience (operations )?platform | - | escalate | 100 | YES |
| outside_service_menu | aiab | outside the menu|custom build|out of scope | - | escalate | 100 | YES |
| run_the_day | aiab | run the day|daily run|run today|start the day | daily-outbound | playbook | 60 | NO |
| run_the_week | aiab | run the week|weekly review|weekly memo|monday memo | weekly-review | playbook | 60 | NO |
| spanish_outreach | aiab | spanish (outreach|sequence|campaign)|translate the sequence | spanish-outreach | playbook | 50 | NO |
| spanish_training | aiab | spanish training|training in spanish | client-training | playbook | 50 | NO |
| call_followup | aiab | follow-?up email.*call|call.*follow-?up email|after the call|debrief|post-?call|call transcript | post-call | playbook | 50 | NO |
| new_prospects | aiab | find|source|prospects?|leads?|city clerks?|clerks|score|send list | Aaron | agent | 30 | NO |
| pre_call_brief | aiab | pre-?call brief|brief me on|one-page brief | Aaron | agent | 40 | NO |
| outreach_copy | aiab | cold email|outreach|sequence|linkedin note|write the (email|copy) | Cody | agent | 30 | NO |
| campaign_ops | aiab | inbox(es)?|healthy|capacity|bounce|replies|reply|dashboard|deliverab | Patty | agent | 30 | NO |
| proposal_scoping | aiab | scope a proposal|proposal|options|roi|quote | Mark | agent | 35 | NO |
| visuals | aiab | one-pager|cover|diagram|graphic|infographic|visual | Dolly | agent | 35 | NO |
| call_coaching | aiab | coach|talk ratio|objection log|score the call | Frannie | agent | 35 | NO |
| viral_scripture | aiab | viral scripture|scripture|bible verse|devotional | Vicky | agent | 30 | NO |
| translation | aiab | translate|translation|spanish|portuguese|in another language | Angelina | agent | 30 | NO |
| client_training_courses | aiab | course|curriculum|lesson plan|module outline|training (video|library|course|module)|loom | Maya | agent | 30 | NO |
| pr_press | aiab | press release|press|media (outreach|announcement)|publicity|pr announcement | Jerry | agent | 30 | NO |
| agent_vault_work | vault | agent vault|vault | - | escalate | 40 | YES |
| pathfinder_work | pathfinder | pathfinder | - | escalate | 40 | YES |
| njeda_work | njeda | nj eda|eda grant|grant narrative|grant application | - | escalate | 40 | YES |
