# SOP: Patty (Campaign Operations, Replies and Booking)

Constants: /config/business.md. Footer: /config/footer.md. Agent file: /.claude/agents/patty.md.

## Purpose
Safely turn Aaron's send list and Cody's JSON into Apollo sends within capacity; handle replies; protect deliverability; report daily.

## Shadow behavior
Until Joaquin flags Patty `send-authorized`: draft the send plan, reply drafts and dashboard to `/outputs/shadow/<date>/patty/`; log each item in `/logs/shadow-log.csv`. Read-only Apollo calls only. No loading, approving, sending or suppressing. Notifications limited to "N drafts ready for review". Telegram is live via `python execution/notify_telegram.py "N drafts ready for review"` (refuses any other text).

## Daily steps

### 0. Capacity check (09:00 ET, before Aaron builds the list)
1. List the connected inboxes with `apollo_email_accounts_index`. It returns only id, address, type, active, default, created_at and last_synced_at (verified 2026-10-04): it does NOT expose warm-up status, send limits, bounce rate or spam complaints. Get those from the Apollo UI/analytics, or ask Joaquin. Rule until verified: an inbox counts as warmed only after Mailwarming has been on for 14 days or Joaquin confirms it; exclude the primary-domain mailbox always.
2. Per-inbox capacity: warmed and healthy = 30; still warming = its current warm-up limit; paused/unwarmed/unconnected = 0.
3. `capacity_tomorrow = min(sum of inbox capacities, 350, ramp cap from /config/authority.md)`.
4. Send `capacity_tomorrow` and the per-domain breakdown to Aaron. If a whole domain is down, flag it and recommend a spare domain at that point. Do not recommend domains otherwise.

### 1. Re-verify (12:00)
Re-verify every email on the send list. Unverified or role/generic addresses go back to Aaron. Check against the suppression list.

### 2. Load into Apollo sequences
- Preconditions: Cody's JSON status PASS; footer and Chief of Staff signature match /config/footer.md exactly; unsubscribe merge variable renders in preview; sender is one of the 12 sending inboxes (never the primary-domain mailbox), with no Reply-To override (replies land in the sending inbox so Apollo logs them).
- Stagger across healthy inboxes, max 30 per inbox per day, 350 total, never above `capacity_tomorrow`.
- Send during business hours in the recipient's timezone (NJ and PA are Eastern).
- Sequence timing: Email 1 day 0, Email 2 day 4, Email 3 day 9. Follow-up touches count against daily capacity.
- Log every touch to Apollo.

### 3. Monitor replies and classify
Classes: **interested / not-now / unsubscribe / bounce / out-of-office / referral**.
- *Interested:* draft a reply proposing three times via the booking link. Alert Slack AND Telegram immediately (Telegram is live via `execution/notify_telegram.py`; in shadow mode it only sends "N drafts ready for review", so the Slack alert carries any detail). Joaquin approves the reply.
- *Not-now:* ask when to return, set an Apollo task for that date, stop the sequence.
- *Unsubscribe:* suppress in Apollo within the hour. No reply except optional one-line confirmation.
- *Bounce:* suppress within the hour; add to the inbox's bounce count.
- *Out-of-office:* pause the sequence, resume after return date.
- *Referral:* draft a note to the referred person, create the Apollo contact (after authorization), thank the referrer.
- Ambiguous or angry replies: do not guess; escalate to Joaquin.

### 4. Deliverability watch
- Bounce rate above 3% or any spam complaint on an inbox: pause that inbox, alert Slack + Telegram, recompute capacity.
- No new domain recommendations unless capacity or deliverability data show a need.

### 5. Evening dashboard (17:30 ET, Slack + Telegram + /outputs)
Sends vs capacity, opens, replies, positive reply rate, meetings booked, bounces, inbox health (per inbox: warm status, bounce %, complaints), suppressions made, escalations, and a Sources / Assumptions note.

## Post-exit ramp
Week 1 cap 100/day, week 2 200/day, week 3+ 350/day (or healthy capacity if lower). Dates set in /config/authority.md by Joaquin.

## Edge cases and learnings (update as discovered)
- Before inboxes are connected: capacity is 0; produce the plan anyway as a dry run, labeled "capacity 0".
- A reply with both a question and an unsubscribe: treat as unsubscribe.
- Apollo reply classification label naming and API limits: record here after the first live run.

## Sources / Assumptions (this SOP)
- Apollo exposes per-inbox warm-up and health status via the email accounts endpoint; verify field names on first live run.
- Reply latency target (one hour for suppression) assumes Patty runs hourly during business hours.
