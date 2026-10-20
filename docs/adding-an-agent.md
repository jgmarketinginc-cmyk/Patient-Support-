# Adding an Agent to the Team

The Chief of Staff reads the team from config, not from code. Adding Vicky, Angelina, Jerry, Maya (or any later agent) is a checklist of files, in this order. The Chief of Staff may draft any of these edits for Joaquin; it never applies the authority row or marks an agent live.

1. **Agent file**: `.claude/agents/<name>.md`. Copy the shape of an existing one: front matter (`name`, `description`, `tools`), "Read first" list, "Single job", numbered Hard rules (shadow mode first; Sources / Assumptions; escalation triggers).
2. **SOP**: `sops/<name>-sop.md` (purpose, shadow behavior, trigger and input, steps, output, rules recap).
3. **Registry row**: `config/agent-registry.md`: name, phase, one-line role, agent file, SOP, role source. Do not set status here.
4. **Routing rows**: `config/routing.md`: task type, keywords, owner = the agent name, mode `agent`, priority, needs Joaquin. Keywords for Vicky (viral scripture), Angelina (translation), Jerry (PR / press) and Maya (course creator: client training and courses) are already there.
5. **Handoff contracts**: if the agent receives or hands over work, add its contract to `/runbook/RUNBOOK.md` (prose) and its field checks to `config/handoff-contracts.md`.
6. **Playbook steps**: add the agent to the playbooks it belongs in (`config/playbooks.md`), or add a new playbook.
7. **Runbook**: schedule or trigger in `runbook/RUNBOOK.md`.
8. **Tests**: run `python -m unittest discover -s tests`. The extensibility test shows that registry, authority, agent file, routing and playbook rows are enough for the router and planner to use a new agent with no code change.
9. **Brand scrub**: `python execution/brand_scrub.py` must return zero hits.
10. **Joaquin only**: add the agent's row to the Status table in `config/authority.md` (`shadow`, start date, 0 errors, `send-authorized: NO`) and set the exit-test rule for it. Until that row says `shadow` or `live`, the Chief of Staff treats the agent as "registered but not built" and escalates any request for it.

Current Phase 3 roles (Joaquin, 2026-10-08, confirmed): Vicky = viral scripture; Angelina = translator; Jerry = PR / press; Maya = course creator (client training and courses).
