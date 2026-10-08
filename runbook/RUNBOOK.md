# RUNBOOK: Order of Operation

Constants live in /config/business.md. Authority flags live in /config/authority.md. Times are America/New_York, Mon-Fri unless noted. Apollo is the system of record at every step.

## Pipeline (Phase 1)

```
Aaron (source > scrub/score > send list)
   > Cody (copy for new Tier A/B)
      > Patty (re-verify, load Apollo, send, classify replies)
         > Evening dashboard (Slack + Telegram)
Sunday: Aaron weekly review > Monday memo
```

## Daily schedule

| Time | Agent | Job | Input | Output / handoff |
|---|---|---|---|---|
| 07:00 | Aaron | Mode 1 SOURCE | Niche A/B filters | New prospects in Apollo (label `pool`) |
| 08:00 | Aaron | Mode 2 SCRUB + SCORE | Pool | Tiered records (A/B/C), trigger line on Tier A |
| 09:00 | Patty | Capacity check | Apollo inbox warm/health status | `capacity_tomorrow` number to Aaron |
| 09:15 | Aaron | Mode 3 DAILY SEND LIST | Capacity, scheduled follow-ups | Send list for NEXT business day: `capacity - follow-ups` slots, never over |
| 10:00 | Cody | Copy | Each new Tier A/B record | JSON (3 emails + LinkedIn note) to Patty |
| 12:00 | Patty | Stage | Cody JSON + send list | Re-verify emails, load Apollo sequences, stagger across healthy inboxes |
| 09:00-17:00 | Patty | Send + replies | Apollo | Classify replies; "interested" => draft reply + instant Slack+Telegram alert; unsubscribe/bounce => suppress within the hour |
| 17:30 | Patty | Dashboard | Apollo stats | Sends, opens, replies, positive reply rate, meetings, bounces, inbox health |
| Sun 19:00 | Aaron | Mode 4 WEEKLY REVIEW | All agents' metrics | One-page Monday memo (worst metric, one fix, "the one thing not to do") |

Phase 2 agents run on demand (see Phase 2 pipeline below). Phase 3 agents (Vicky, Jerry, Maya, Angelina) are in shadow since 2026-10-08 (Joaquin, /config/authority.md); see the Phase 3 section below. Aaron also produces pre-call briefs on request.

## Phase 2 pipeline (on demand)

```
Call ends / transcript arrives
   > Frannie (coach note, objection log, email draft, Apollo update staged)
      > [qualified call or ready to buy] Mark (3 options, ROI, timeline, terms)
         > Cody (proposal narrative)  +  Dolly (visuals)
            > Joaquin approves  > sent by Joaquin
Sunday: Frannie weekly pattern summary > Aaron's Mode 4 review
```

| Trigger | Agent | Job | Input | Output / handoff |
|---|---|---|---|---|
| Call ends or transcript/notes arrive | Frannie | Post-call coaching | Transcript/notes + Apollo contact | One-page note, next-step email draft (to Cody), Apollo update (stage, objections, next step, date) |
| Frannie logs a qualified call, or Joaquin asks | Mark | Proposal scoping | Frannie note, discovery notes, /config/business.md + /config/sales.md | Outline, 3 options, ROI table, timeline, terms; briefs to Cody and Dolly |
| Request from Mark, Cody or Joaquin | Dolly | Visuals | Brief + /config/brand.md + supporting copy | Primary + alternate asset, editable source |
| Sunday | Frannie | Weekly pattern summary | The week's calls | `weekly-pattern.md` to Aaron |

Handoff contracts (Phase 2):
- **Frannie > Mark**: Apollo contact ID, qualified flag, pain in the prospect's own words with timestamps, hours and wage if stated, decision-maker, objections, escalation items.
- **Frannie > Cody**: email draft (no price above $1,500, no discount). Cody polishes; footer from /config/footer.md.
- **Mark > Cody**: option structure and rationale; narrative uses only sourced facts.
- **Mark > Dolly**: format, in-scope workflow steps, approved copy. Client names only after Joaquin approves.
- **Frannie > Joaquin (Slack + Telegram)**: ready to buy, contract request, custom/municipal contract, anything outside the service menu, discount request. Ready to buy also goes to Mark.

Phase 2 shadow exit test is item-based: 10 real approved items per agent, >=95% approved with no edits, zero critical errors (see /config/authority.md).

Phase 2 rules: Apollo is the system of record; drafts and staging only; price above $1,500 in writing only; never discount on a first meeting (offer reduced scope); constants in /config/sales.md and /config/brand.md. Authority flags for Frannie, Mark and Dolly start as `shadow` once Joaquin updates /config/authority.md (it still reads "not built").

## Phase 3 agents (on demand)

| Agent | Role | Trigger | Output / handoff | Checker |
|---|---|---|---|---|
| Vicky | Viral scripture short-form video scripts | Joaquin request (reference or theme) | Script file: 3 hooks, body, caption, hashtags. Joaquin records and posts. | `execution/scripture_check.py` |
| Angelina | Translator (Spanish first, for NJ/PA municipalities with Hispanic leadership) | Request from Cody, Jerry, Maya or Joaquin with an approved English asset | Translated asset, glossary, flags. Outreach JSON goes to Patty only through the Chief of Staff gate (`angelina-patty`). | `execution/translation_check.py` |
| Jerry | PR and press for documented wins | Joaquin request with a source of truth | Press release, boilerplate, subject lines, open facts. Joaquin sends. | `execution/press_check.py` |
| Maya | Course creator: client training and courses | Install build phase or delivery, or Joaquin request | Six core module scripts, shot lists, reference materials. Joaquin records on Loom. | `execution/course_check.py` |

Phase 3 rules: shadow from the first run; nothing is published, sent or shared; Joaquin approves and sends. Playbooks: `spanish-outreach` (Angelina > Patty) and `client-training` (Maya > Angelina when Spanish is needed > Chief of Staff recording package). Open items: venture for scripture content, approved scripture translation and verse source, Spanish opt-out wording, native-speaker reviewer, approved boilerplate and media contact, whether courses are sold as a product.

## Chief of Staff (head of agents)

The Chief of Staff conducts the team from the main session with `/cos <goal>`. It is not a subagent (subagents cannot call subagents) and it does not use the Workflow tool. Directive: /sops/chief-of-staff-sop.md. Note: "Chief of Staff" is also the outbound email signature (/config/footer.md); that is a different thing.

```
Joaquin > Chief of Staff > [Aaron, Cody, Patty, Frannie, Mark, Dolly, + Phase 3 when built]
```

Conducting loop: intake > classify (`route_request.py`) > pre-flight (authority, phase, inputs) > plan (`plan_run.py`) > delegate in waves (max 6 parallel) > gate each handoff (`check_handoff.py`, one rework, then halt and escalate) > consolidate one report to Joaquin > learn.

Decision rights are in /config/decision-rights.md: the Chief of Staff decides routine operations; Joaquin decides authority flags, phase, prices and terms, contracts, anything external, spend, brand, adding or retiring agents, critical-error resets, anything outside the menu.

Playbooks (/config/playbooks.md): `daily-outbound`, `post-call`, `weekly-review`, `pre-call-brief`, `escalation`; stubs for the other ventures until Joaquin fills /config/ventures.md. The registry (/config/agent-registry.md) lists ten agents; Vicky, Angelina, Jerry and Maya are registered as not built, so requests for them escalate. To add one, follow /docs/adding-an-agent.md.

Records: `logs/cos-runs/<run_id>.json`, `logs/cos-log.csv`; consolidated reports in `outputs/shadow/<date>/chief-of-staff/`.

Shadow: the Chief of Staff is in shadow from its first run. Proposed row for /config/authority.md (Joaquin adds it): `| Chief of Staff | 0 | shadow | 2026-10-08 | 0/10 | 0 | NO |`. Exit test: item-based like Phase 2 (10 real approved run reports, >=95% approved with no edits, zero critical errors).

## Handoff contracts

- **Aaron > Cody**: Apollo record ID, name, title, org, city, size, niche, tier, trigger line, verified email status.
- **Cody > Patty**: JSON `{prospect_id, emails[3], linkedin_note, sender, footer_ref, sources_assumptions}`. Footer always read from /config/footer.md.
- **Patty > Aaron**: `capacity_tomorrow`, inbox health, per-day metrics.
- **Everyone > Joaquin**: items carry a Sources / Assumptions note.

## Shadow mode (first 10 business days per agent)

1. Agent writes drafts to /outputs/shadow/YYYY-MM-DD/<agent>/ and appends one row per item to /logs/shadow-log.csv (`date,agent,item,approved,edits,error_severity`).
2. Joaquin marks each item approved / edited / rejected. Nothing external happens: no sends, no Apollo sequence activation, no outbound notifications about prospects.
3. Day 10 test: >=95% approved with no edits AND zero critical errors. Critical error resets that agent's clock.
4. Joaquin sets `send-authorized` in /config/authority.md. Agent output then goes to /outputs/live/.
5. Patty ramp: 100/day week 1, 200/day week 2, 350/day week 3+.

During shadow, notifications to Slack + Telegram are limited to "N drafts ready for review"; no prospect data leaves the system.

## Escalations (to Slack + Telegram, immediately)

- List quality <90% verified
- Positive reply rate <1% for 3 days
- Bounce >3% or any spam complaint on an inbox (Patty pauses that inbox)
- A domain-level pause: flag it and recommend a spare domain at that point
- Aaron: if Modes 1-3 crowd Mode 4, recommend splitting sourcing into its own agent in the Monday memo (never split unilaterally)

## Joaquin's daily touchpoints

1. Approve shadow items (target: under 15 minutes).
2. Review Patty's 17:30 dashboard.
3. Take booked calls (20-min structure). After each call, review Frannie's note and any Mark outline.

## Domain and mailbox setup (per sending domain; Joaquin does these, 12 mailboxes total)

DOMAIN_1-3 are in /config/business.md. For each domain:
1. Confirm it is registered. Point its website to https://www.theaiagencyblueprint.com (redirect) so recipients who visit it land on the real site.
2. DNS: SPF, DKIM and DMARC (start DMARC at `p=none`, tighten after 2 clean weeks). Verify with a free checker before warming.
3. Create 4 mailboxes (suggested names chiefofstaff1 to chiefofstaff4). Display name "Chief of Staff, The AI Agency Blueprint". Add the Chief of Staff signature from /config/footer.md.
4. Connect each mailbox to Apollo (Settings > Mailboxes), turn Mailwarming on, and keep the daily send limit at or below 30.
5. Tell Patty. She counts a mailbox toward capacity only when Apollo shows it connected, warmed and healthy (~14 days).
6. Warm-up can start per domain as soon as its mailboxes exist; do not wait for the other domains.

## Brand scrub

Run `python execution/brand_scrub.py` before any commit and before any template goes live. Zero hits required.

## Folder map

```
.claude/agents/   one subagent per agent
sops/             one SOP per agent (directive layer)
config/           business.md, sales.md, brand.md, authority.md, footer.md
runbook/          this file
execution/        deterministic scripts (brand_scrub.py, assemble_sequence.py, call_analyzer.py, roi_calc.py, dolly_build.py, asset_check.py)
outputs/shadow/   drafts awaiting approval
outputs/live/     post-authorization outputs
logs/             shadow-log.csv
docs/             use-case write-up
```
