# Business Constants: The AI Agency Blueprint

Single source of truth. Every agent and SOP references this file; none restate it. Owner: Joaquin Garcia, CEO.

## Identity and sender

- Brand: The AI Agency Blueprint
- Sender (DECIDED by Joaquin 2026-10-06): the sending inboxes on DOMAIN_3, chiefofstaff1-4@theaiagencyblueprint.io (more on DOMAIN_1-2 later). The primary mailbox chiefofstaff@theaiagencyblueprint.com is NEVER used for cold sends; it is connected in Apollo as a Gmail account (verified 2026-10-03). Mailwarming ENABLED 2026-10-03 (approved by Joaquin). Apollo send limits on this mailbox: 50/day, 6/hour, 10-minute delay; Patty enforces our 30/day cap.
- Signature (APPROVED by Joaquin): the Chief of Staff block in /config/footer.md (role-based, no invented personal name). Emails speak as "we"; Joaquin is "our CEO" where the call is offered. LinkedIn notes are the exception: they go out from Joaquin's own account and are written in his voice.
- Footer and unsubscribe: /config/footer.md (verbatim)
- Retired brand names must never appear anywhere. Enforced by `python execution/brand_scrub.py` (zero hits required; the patterns live only in that script).

## Voice

Confident, direct, mission-driven, builder not consultant. Faith-grounded and community-first, never preachy in outreach. Municipal tone: formal-warm. SMB tone: plain and direct.

## Positioning

We install AI-powered operations systems that cut manual workload 50-70% and produce better documentation, delivered in 21 days, trained on the client's own documents, with a named human operator.

No client case studies exist yet. Never invent results, logos, testimonials or numbers. Frame as "systems we build" and the audit as the low-risk first step.

## Offer ladder

| Step | Offer | Price | Delivery |
|---|---|---|---|
| 0 | Free 20-minute call (top-of-funnel hook; NOT a free assessment) | $0 | 20 min |
| 1 | AI Audit (entry offer) | $1,500 | 7 business days |
| 2 | AI Operations Install | $18,000 | 21 days |
| 2b | Managed Operations retainer | $2,400-$4,800/mo | ongoing |
| 3 | Resilience Operations Platform | $65,000 + $7,500/mo | later |

Rules: never mention the $1,500 audit in Email 1 (the free call is the hook). Price in writing only for anything above $1,500. Never discount on a first meeting.

## Niches

- **A. NJ municipalities**: city managers, clerks, DPW directors, administrators, emergency management.
- **B. Small businesses**: owners, founders, operations managers at NON-TECH companies with 1-50 employees in NJ and the Philadelphia area.

Geo filter: NJ and Philadelphia area only. Drop everything else.

## Phase gating (agents must not pitch outside the current phase)

| Phase / window | Sellable now |
|---|---|
| **Phase 1 (current)** | Constituent/Customer Response Agent; AI Audit |
| Months 3-4 | + Document Intake |
| Months 5-7 | + Inspection Reporting and Scheduling |
| Month 8+ | + Resilience Operations Platform |

Current phase: **Phase 1**. Joaquin changes this line; agents never do.
Off-phase pitch = critical error in shadow mode.

## Outbound capacity (Apollo only)

- Sending tool: Apollo (sequences, sending, replies, logging). No other sending tool is referenced anywhere.
- 3 domains x 4 mailboxes = 12 inboxes. Max 30 sends/inbox/day. Hard cap 350 sends/day total (12 x 30 = 360, cap wins). Mon-Fri only: ~1,750 sends/week.
- 3-touch sequence => ~580 NEW prospects/week (1,750 / 3). Daily new-prospect slots = 350 minus scheduled follow-up touches due that day.
- Prospect pool target: 2,500/week. Aaron sizes the daily send list to capacity and holds the remainder in pool.
- Per-domain ceiling: 4 inboxes x 30 = 120/day. One domain paused = capacity drops by up to 120.
- Warm-up: no inbox sends at full volume until warmed (~14 days). Before building the day's capacity, Patty checks each inbox's warm status in Apollo. Unwarmed or paused inboxes contribute 0 (or their current warm-up limit) and capacity reduces automatically. Aaron receives Patty's capacity number, never assumes 350.
- Post shadow-exit ramp for Patty: week 1 capped at 100/day, week 2 at 200/day, week 3+ at 350/day (or current healthy capacity if lower).
- Pause triggers: bounce rate >3% or any spam complaint on an inbox => pause that inbox, alert. If a whole domain trips a pause, flag it and recommend a spare domain at that point. Do not recommend buying domains otherwise.

## Domains (owned by Joaquin; do not assume names)

Decisions (2026-10-03): all 12 sending inboxes present as **Chief of Staff** (same display name and signature; mailbox local-parts differ per inbox, e.g. chiefofstaff1-4). The primary domain is never used for cold sends. A second existing domain carries the retired brand and is not used.

| Slot | Value | Status |
|---|---|---|
| DOMAIN_1 | theaiagentagencyblueprint.com | provided 2026-10-03; spelling has "agent" in it, Joaquin to confirm it is intended; purchase status unconfirmed |
| DOMAIN_2 | theaiagencyblueprint.org | provided 2026-10-03; purchase status unconfirmed |
| DOMAIN_3 | theaiagencyblueprint.io | FIRST BATCH: chiefofstaff1-4 created and active (Joaquin, 2026-10-04); NOT yet connected to Apollo (verified 2026-10-04) |

Each domain hosts 4 mailboxes. Joaquin creates all 12 mailboxes after the domains exist. `execution/brand_scrub.py` re-checks this table once real values are entered. Each new domain needs SPF, DKIM and DMARC before warm-up.

Retired-brand check on all three names: clean. Setup steps per domain are in /runbook/RUNBOOK.md.

**Rollout plan (Joaquin, 2026-10-04):** 4 sending mailboxes now (the .io batch), then add 4 more, then possibly the last 8, each step funded by first client payments. Apollo plan limits mailboxes per user (alert: 1 per user), so each step needs matching seats or a plan with more mailboxes per user.

| Stage | Mailboxes | Max sends/day | New prospects/week (3-touch) |
|---|---|---|---|
| 1 | 4 | 120 | ~200 |
| 2 | 8 | 240 | ~400 |
| 3 | 12 | 350 (cap) | ~580 |

**Interim capacity:** until each domain's mailboxes exist and are warm, e.g. with only one domain live, capacity is at most 4 inboxes x 30 = 120/day (about 600 sends/week, roughly 200 new prospects/week on a 3-touch sequence). Patty's capacity check reduces the number automatically; Aaron sizes the list to it. Warm-up for DOMAIN_1 inboxes can start as soon as they exist; do not wait for the other domains.

## Weekly KPI targets (Aaron compares against)

| Metric | Target |
|---|---|
| Sends | 1,750/week |
| Personalized follow-ups | 25-35/day |
| Positive reply rate | 2%+ |
| Discovery calls | 2-4/day at maturity |
| Audit-to-install conversion | >=50% |
| List quality (verified) | >=90% |
| Bounce rate | <3% per inbox |

Escalation triggers: verified <90%; reply rate <1% for 3 days; deliverability alerts; bounce >3% or spam complaint.

## Call structure (20 minutes, DECIDED)

Free call and sales calls are 20 minutes. Structure scaled from the original 25: frame 2 min, diagnose 10, present 5, close 3 (assumption on the split; Joaquin can adjust). Book with a 10-minute buffer after. Calls run on Joaquin's calendar via the booking link (PENDING, see below).

## Booking link (recommendation, Joaquin to decide)

Current link is Joaquin's general scheduling page. Recommend replacing it in outreach with a **dedicated "Free 20-Minute Call" link**:
- Single event type, 20 minutes, only your open sales windows, 10-minute buffer, 24-hour minimum notice.
- Intake questions: name, organization, role, one line on the biggest manual workload. Feeds Aaron's pre-call brief.
- Brand-clean page title and description (retired brand names must not appear; check the current page).
- Source tagging (`?src=apollo`) so Patty can count meetings booked per sequence, and the booking lands in Apollo (Apollo meeting link, or a calendar tool with an Apollo integration) so the touch is logged.
- Why not the general page: it may expose other meeting types or lengths, carries no source tracking, and a prospect who sees a personal calendar may book the wrong thing.
- BOOKING_LINK: https://cal.com/joaquin-garcia-j.garcia-i9bobi/www.theaiagencyblueprint.com

VERIFIED by Joaquin 2026-10-03 (20 minutes, brand-clean, correct calendar, buffer and intake set; I could not open it myself, cal.com is blocked from this environment). `execution/assemble_sequence.py` reads the `BOOKING_LINK` line above and substitutes it for `{{booking_link}}` in every email. Optional later: a shorter slug such as `/free-20-min-call`.

## Prospecting credit budget (Vibe Prospecting)

- Estimate (read-only preview, no export run): filter = company HQ in NJ, 1-50 employees, owner/founder/manager/C-suite, email available. ~14,970 matching records. Base export cost = 1 credit per row (1,000 rows = 1,000 credits), so **2,500 rows is about 2,500 credits per week** before contact-data enrichment.
- Enrichment (verified email/phone) is priced separately and was NOT estimated. Aaron runs `estimate-cost` with enrichment before the first spend and reports the number.
- Cap (APPROVED by Joaquin): **2,500 base credits/week plus enrichment as estimated**. Aaron stops and asks Joaquin before exceeding it.
- Start (APPROVED by Joaquin): source about 700 rows/week, not 2,500. Sends need ~580 new prospects/week (1,750 / 3 touches) plus ~20% scrub loss. The 2,500 pool target only pays for itself if yield is poor; scale up if verified/Tier A+B yield falls short.
- Municipal niche A is sourced from Apollo, not Vibe.
- Preview showed noise: some prospects were personally located outside NJ and some companies were tech. Aaron adds a prospect-location filter, excludes tech categories, and uses city/region filters for the Philadelphia area.

## Notifications

Every notification goes to BOTH Slack and Telegram. If one channel fails, deliver on the other and log the failure. **Telegram is live** (verified 2026-10-06): send with `python execution/notify_telegram.py "<message>"`, which reads `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` from the environment. In shadow mode the script only allows "N drafts ready for review" and refuses anything else; no prospect data ever goes to Telegram.

**Slack channel:** `#agent-ops` (ID `C0C74B5UPS6`, public, verified 2026-10-06). Shadow mode: only "N drafts ready for review" style counts, no prospect data. Open item: a private `#agent-alerts` channel exists but the Slack connector cannot see it; move alerts there before Patty goes live, once the connector can reach it, and archive `#agent-ops`.

## Output standard (all agents)

1. Every output ends with a **Sources / Assumptions** note: where each fact came from (Apollo record ID, URL, document) and what was assumed. Unverifiable facts are removed, not softened.
2. Concise. Questions to Joaquin as bullets.
3. Drafts only until the agent is send-authorized in /config/authority.md.
4. Apollo is the system of record. No private lists.

## Next build after outbound

AI chatbot on the Lovable-built website answering resident and inspection-paperwork questions. Lead with transparency about what it is (many people are skeptical of AI).

## Open items needing Joaquin

Done:
- [x] Chief of Staff signature approved
- [x] Call length: 20 minutes
- [x] Vibe Prospecting cap and 700-row start approved
- [x] chiefofstaff@theaiagencyblueprint.com connected in Apollo (Gmail, active), Mailwarming ON
- [x] All inboxes present as Chief of Staff
- [x] Domains named (DOMAIN_1-3), clean of retired brand
- [x] Cal.com booking link verified
- [x] Primary domain and retired-brand domain excluded from sending

Findings 2026-10-04:
- Apollo plan limit: "Your plan can only link 1 mailbox per user." The account has 1 user (Joaquin), who already has the primary-domain mailbox linked. 12 sending mailboxes need either a plan that allows more mailboxes per user, or 12 users/seats. Joaquin to check pricing at the upgrade link and decide.
- Apollo's account setting already appends an unsubscribe link (template token `<%Unsubscribe%>`, include-unsubscribe-link ON). Our custom `{{unsubscribe_link}}` line in /config/footer.md may not be a valid Apollo variable. Resolve with the test email before any send (risk: raw text, or two unsubscribe lines).
- Open/click tracking are OFF in Apollo (good for deliverability).
- Reply-To override dropped: replies must land in the sending inbox for Apollo to log them.

Open (see the numbered list in chat for the current questions):
- [ ] Confirm the three domains are purchased and DOMAIN_1's spelling ("agent") is intended
- [ ] Connect chiefofstaff1-4 @ .io to Apollo (OAuth, one at a time), turn Mailwarming on, limit 30/day; then create the other 8 mailboxes
- [ ] Decide whether to keep the 2-minute Loom offer in Email 1 (Joaquin would record them on request)
- [x] Telegram: live and verified 2026-10-06 (token and chat ID set as environment variables, test message delivered)
- [ ] Telegram: the bot token was pasted in chat earlier; revoke and reissue it in BotFather, then update `TELEGRAM_BOT_TOKEN`
- [ ] Verify the opt-out link renders in an Apollo test email
- [ ] Confirm the email verification tool (default NeverBounce) and the Apollo do-not-contact list as master suppression list
- [ ] Review the 8 dry-run items (optional calibration, outputs/shadow/2026-10-03/)
