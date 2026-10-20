# Agent Registry

The single list of agents the Chief of Staff can command. Scripts read this file; no agent names are hard-coded in code.

**Status is never set here.** It is read from `/config/authority.md`. An agent is callable only if (1) it is in this table, (2) its agent file exists, and (3) `/config/authority.md` shows it as `shadow` or `live` (not `not built`). Otherwise requests for it escalate to Joaquin as "registered but not built".

The Chief of Staff itself is not a row here: it is the conductor, runs in the main session (`/cos`), and has its own proposed authority row (see `runbook/RUNBOOK.md`, Chief of Staff).

To add an agent, follow `/docs/adding-an-agent.md`.

| Name | Phase | Role | Agent file | SOP | Role source |
|---|---|---|---|---|---|
| Aaron | 1 | Lead sourcing, scoring, daily send list, weekly review, pre-call briefs | .claude/agents/aaron.md | sops/aaron-sop.md | repo |
| Cody | 1 | Outreach copy, proposal narrative, polishing email drafts | .claude/agents/cody.md | sops/cody-sop.md | repo |
| Patty | 1 | Campaign operations: inbox health, capacity, replies, dashboard | .claude/agents/patty.md | sops/patty-sop.md | repo |
| Frannie | 2 | Post-call coaching, objection log, next-step email draft, Apollo staging | .claude/agents/frannie.md | sops/frannie-sop.md | repo |
| Mark | 2 | Proposal scoping: three options, ROI, timeline, terms | .claude/agents/mark.md | sops/mark-sop.md | repo |
| Dolly | 2 | Visual design: covers, diagrams, one-pagers, social graphics | .claude/agents/dolly.md | sops/dolly-sop.md | repo |
| Vicky | 3 | Viral scripture content | .claude/agents/vicky.md | sops/vicky-sop.md | Joaquin, 2026-10-08 chat (confirmed) |
| Angelina | 3 | Translator | .claude/agents/angelina.md | sops/angelina-sop.md | Joaquin, 2026-10-08 chat; name spelled Angelina in the repo and the Blueprint v2 plan |
| Jerry | 3 | PR / press: press releases and media announcements | .claude/agents/jerry.md | sops/jerry-sop.md | Joaquin, 2026-10-08 chat (confirmed) |
| Maya | 3 | Course creator: client training and courses | .claude/agents/maya.md | sops/maya-sop.md | Joaquin, 2026-10-08 chat (confirmed) |

## Handoff contracts

Per-contract field checks live in `/config/handoff-contracts.md` and are run by `execution/check_handoff.py`. Prose contracts are in `/runbook/RUNBOOK.md`.
