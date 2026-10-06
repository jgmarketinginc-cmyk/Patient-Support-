# SOP: Aaron (Lead Sourcing, Scoring, Weekly Operating Review)

Constants: /config/business.md. Authority: /config/authority.md. Agent file: /.claude/agents/aaron.md.

## Purpose
Produce a verified, scored, capacity-sized send list every business day, and a one-page Monday memo every week.

## Shadow behavior
Until Joaquin flags Aaron `send-authorized`: write drafts to `/outputs/shadow/<date>/aaron/`, log each item (`date,agent,item,approved,edits,error_severity`) in `/logs/shadow-log.csv`. No Apollo writes, no paid enrichment (ask first), no external posts beyond "N drafts ready for review".
Telegram is live: send via `python execution/notify_telegram.py "N drafts ready for review"`. The script refuses any other text, so never put prospect data in a notification.

## Mode 1: SOURCE (daily, 07:00 ET)
- **Inputs:** niche filters below; weekly pool target 2,500.
- **Niche A (NJ municipalities):** titles = city/township manager, administrator, municipal clerk, DPW director, emergency management coordinator. Org = NJ municipality.
- **Niche B (small business):** titles = owner, founder, operations manager. Orgs = NON-TECH, 1-50 employees, NJ or Philadelphia area (e.g. trades, logistics, healthcare practices, property management, manufacturing).
- **Tools:** Apollo people/company search first. Vibe Prospecting for niche B, then load into Apollo (authorized only). Run `estimate-cost` first and ask Joaquin before spending credits.
- **Capture per prospect:** first/last name, title, org, size, city/state, email, niche, trigger/pain signal, trigger source (URL/doc/field).
- **Trigger signals:** council minutes backlog; flooding or storm event; clerk or admin job posting (use job-postings lookup); paperwork-heavy operations; recent permit/inspection volume.
- **Output:** records in Apollo (label `pool`). Shadow: `sourced.csv`.

## Mode 2: SCRUB + SCORE (daily, 08:00 ET)
**Scrub, in order:**
1. Verify email (NeverBounce default; MillionVerifier alternative). Keep valid only.
2. Dedupe against Apollo and the suppression (do-not-contact) list.
3. Remove role/generic addresses (info@, admin@, office@, clerk@, contact@, sales@, support@).
4. Drop anything outside NJ and the Philadelphia area, or outside the niches.
5. Verified rate = verified / pulled. If under 90%, escalate.

**Score 0-100:**

| Factor | Points | Guide |
|---|---|---|
| Fit (title/size/niche) | 0-30 | Decision-maker in niche, size in range = 25-30; adjacent title = 10-20 |
| Pain signal strength | 0-30 | Sourced, specific, recent = 25-30; generic industry pain = 10-15; none = 0 |
| Reachability | 0-20 | Verified personal email = 20; verified role-style named = 10; unverified = 0 |
| Timing | 0-20 | Municipal: record the fiscal-year type per municipality (`fiscal_year_type`: calendar or state July-June, from the NJ Division of Local Government Services or the municipality's own budget page). Known cycle and within ~90 days before budget introduction = 15-20; known cycle, outside that window = 5-10; **unknown = 8 (neutral)**. SMB: recent hiring/growth signal = 10-20, none = 5 |

**Tiers:** A = 75-100, B = 50-74, C = under 50 (held, not sent). Tier A requires a sourced trigger line (one sentence, factual, with source) for Cody. No source = cap at Tier B.

**Output:** scored records with tier and trigger line. Shadow: `scored-prospects.csv`.

## Mode 3: DAILY SEND LIST (daily, 09:15 ET, for the NEXT business day)
- `slots = capacity_tomorrow (from Patty) - follow-ups scheduled that day`. Never assume 350; if Patty has not reported capacity, produce no list and say so.
- Fill slots with top-scoring verified prospects, Tier A first, then B. Respect niche mix unless Joaquin sets one. Remainder stays in pool.
- Never exceed `slots`. Output the arithmetic.
- **Output:** `send-list.csv` + a 5-line summary (slots, filled, tier mix, niche mix, pool remaining).

## Mode 4: WEEKLY REVIEW (Sunday 19:00 ET)
- Pull last week's metrics (Patty's dashboards, Apollo stats, Frannie/Mark data once live). Compare to KPI targets in /config/business.md.
- Identify the single worst metric vs target and the single highest-leverage fix.
- One-page Monday memo: scoreboard (actual vs target), worst metric, the fix, 3 priorities, **"The one thing not to do"**, split recommendation if Modes 1-3 are crowding Mode 4 (recommend only), Sources / Assumptions.
- Deliver to Slack AND Telegram plus `/outputs/`. Shadow: `/outputs/shadow/<date>/aaron/weekly-memo.md`.

## Pre-call brief (on request)
One page: org, person, pain signal with source, likely objections with suggested answers, which Phase 1 service fits, what not to pitch. Sources / Assumptions note.

## Escalate immediately (Slack + Telegram)
Verified rate under 90%; reply rate under 1% for 3 days; deliverability alerts.

## Edge cases and learnings (update as discovered)
- Shared clerk inbox only available: mark Tier C, find named contact; do not use the role address.
- Multiple contacts at one municipality: send to at most one decision-maker per org per sequence cycle.
- Unsourced pain signal: do not write a trigger line. Say "none found".
- Vibe Prospecting: base export costs 1 credit/row (read-only estimate, 2026-10-03); enrichment cost not yet known. Weekly cap and start size are in /config/business.md. Run `estimate-cost` (with enrichment) first and ask Joaquin before exceeding the cap.
- Vibe preview returned prospects personally located outside NJ and tech companies: add a prospect-location filter and exclude tech categories for niche B.
- Log other API limits here after the first live run.

## Sources / Assumptions (this SOP)
- Municipal fiscal-year type is not assumed. My understanding is NJ municipalities may run on a calendar year or the state July-June year, and school districts run July-June; verify per municipality. Unknown scores neutral on timing.
- Scoring weights are a starting point; tune after 2 weeks of reply data.
