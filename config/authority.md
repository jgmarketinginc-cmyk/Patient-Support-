# Authority Flags

**Only Joaquin edits this file.** An agent never flips its own flag, and never edits this file.

Default is `shadow`: the agent writes DRAFTS to /outputs/shadow/ and logs each to /logs/shadow-log.csv. Nothing external happens (no sends, posts, publishes, spend, or Apollo writes that touch prospects).

## Shadow exit test (per agent)

Over 10 business days: >=95% of items approved with no edits AND zero critical errors.

Critical errors: wrong recipient; wrong name/city; fabricated fact; wrong brand or footer; off-phase service pitch. Any critical error resets that agent's 10-day clock.

## Phase 2 exit test (Frannie, Mark, Dolly): item-based (Joaquin, 2026-10-08)

Phase 2 agents run on demand, so the test counts items, not days.
- Each agent needs **10 real approved items** (Frannie: calls; Mark: proposals; Dolly: assets). Synthetic dry-run items do not count.
- >=95% approved with no edits AND zero critical errors.
- A critical error restarts that agent's item count at 0.
- Joaquin then sets `send-authorized: YES` himself.
- In the Status table, the "Day" column for Phase 2 agents means items counted (x/10), starting at the first real item.

## Status

| Agent | Phase | Status | Shadow start | Day | Critical errors | send-authorized |
|---|---|---|---|---|---|---|
| Aaron | 1 | shadow (not started) | - | 0/10 | 0 | NO |
| Cody | 1 | shadow (not started) | - | 0/10 | 0 | NO |
| Patty | 1 | shadow (not started) | - | 0/10 | 0 | NO |
| Frannie | 2 | shadow | 2026-10-08 | 0/10 | 0 | NO |
| Mark | 2 | shadow | 2026-10-08 | 0/10 | 0 | NO |
| Dolly | 2 | shadow | 2026-10-08 | 0/10 | 0 | NO |
| Vicky | 3 | shadow | 2026-10-08 | 0/10 | 0 | NO |
| Jerry | 3 | shadow | 2026-10-08 | 0/10 | 0 | NO |
| Maya | 3 | shadow | 2026-10-08 | 0/10 | 0 | NO |
| Angelina | 3 | shadow | 2026-10-08 | 0/10 | 0 | NO |
| Chief of Staff | 0 | shadow | 2026-10-08 | 0/10 | 0 | NO |

## Patty post-exit ramp

| Stage | Daily send cap | Starts |
|---|---|---|
| Week 1 after exit | 100 | (set by Joaquin) |
| Week 2 | 200 | |
| Week 3+ | 350 (or healthy capacity if lower) | |

Current cap while shadow: 0 external sends.

## Standing rules while send-authorized

- Replies to "interested" prospects: still Joaquin-approved until he states otherwise here.
- Unsubscribes and bounces: Patty may suppress in Apollo within the hour once Patty is send-authorized.
- Any critical error after authorization: Joaquin sets the flag back to NO; the 10-day clock restarts.

## Notes

- Joaquin can flip a flag only after the shadow log shows the exit test met. The log is /logs/shadow-log.csv.
