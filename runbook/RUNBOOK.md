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

Phase 2/3 agents (Frannie, Mark, Dolly, Vicky, Jerry, Maya, Angelina) run on demand only. Aaron also produces pre-call briefs on request.

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

During shadow, notifications to Slack + Telegram (live via `execution/notify_telegram.py`) are limited to "N drafts ready for review"; no prospect data leaves the system.

## Escalations (to Slack + Telegram, immediately)

- List quality <90% verified
- Positive reply rate <1% for 3 days
- Bounce >3% or any spam complaint on an inbox (Patty pauses that inbox)
- A domain-level pause: flag it and recommend a spare domain at that point
- Aaron: if Modes 1-3 crowd Mode 4, recommend splitting sourcing into its own agent in the Monday memo (never split unilaterally)

## Joaquin's daily touchpoints

1. Approve shadow items (target: under 15 minutes).
2. Review Patty's 17:30 dashboard.
3. Take booked calls (25-min structure).

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
config/           business.md, authority.md, footer.md
runbook/          this file
execution/        deterministic scripts (brand_scrub.py)
outputs/shadow/   drafts awaiting approval
outputs/live/     post-authorization outputs
logs/             shadow-log.csv
docs/             use-case write-up
```
