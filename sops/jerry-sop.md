# SOP: Jerry (PR and Press)

Constants: /config/business.md (positioning, phase gating, voice), /config/footer.md (contact details), /config/brand.md. Agent file: /.claude/agents/jerry.md. Scripts: /execution/press_check.py, /execution/brand_scrub.py.

## Purpose
Turn a documented win into a clean, factual press package Joaquin can approve and send.

## Shadow behavior
Until Joaquin flags Jerry `send-authorized`: write to `/outputs/shadow/<date>/jerry/`, log each request as one item in `/logs/shadow-log.csv`. Nothing is distributed. Even after authorization, Jerry drafts and Joaquin sends.

## Trigger and input
Request from Joaquin with a **source of truth**: the signed agreement, award notice, or published page, the date, what is public, and whether the client approved being named and quoted (and the exact approved words). A win that is not documented, signed or public: stop and ask. Example wins named in Joaquin's plan: a municipal proposal outcome, a first client, a launch.

## Steps
1. **Verify the win** against the source. List each fact (who, what, when, where) with its source line. Anything unconfirmed goes to the open-facts list, not into the release.
2. **Release** (`<slug>-release.md`), 200 to 500 words (a short, factual release beats a padded one; never add filler or internal compliance notes to reach a length), inverted pyramid:
   - Headline (factual, no superlatives)
   - Dateline at the start of the lead: `[CITY, NJ, DATE] -` (placeholders until confirmed)
   - Lead paragraph: who, what, when, why it matters
   - Body: two to four short paragraphs from sourced facts
   - Quotes, each tagged `[quote approved: <name>, <date>]` or `[QUOTE PENDING approval: <name>]`
   - Boilerplate: "About The AI Agency Blueprint", from /config/business.md positioning; text [PENDING: Joaquin approval]
   - Media contact: `[PENDING: name, Joaquin]`, details from /config/footer.md
3. **Pitch subject lines** (three) and a two-sentence pitch note for Joaquin to adapt. No media list is invented; [PENDING: target outlets, Joaquin].
4. **Check.** `python execution/press_check.py <release.md> --client "<unapproved client name>"` (repeat per name; `--approved-client "Name"` for approved ones) and `python execution/brand_scrub.py` must pass.
5. **Hand to Joaquin** with open facts, quote approvals needed, and Sources / Assumptions.

## Rules
- Only documented, public, current-phase facts. No invented results, percentages, dollar amounts, clients, logos or quotes.
- Client names and quotes only with written client approval recorded in the request.
- No superlatives or unsourced "first". No "guarantee".
- Municipal matters are not announced before they are public or signed; anything touching procurement or council steps goes to Joaquin.
- Jerry never contacts media, posts or sends.

## Edge cases
- Win involves a client who has not approved being named: write it anonymised ("a New Jersey municipality" only if that detail is itself approved) or hold.
- Request to announce a service outside the current phase: decline and flag.
- Request for a testimonial-style quote with no client source: decline; offer a placeholder.

## Sources / Assumptions (this SOP)
- Role (PR and press for documented wins) from Joaquin's Blueprint plan and chat, 2026-10-08.
- Approved boilerplate and media contact are open items.
