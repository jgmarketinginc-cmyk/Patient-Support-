# TRIAL-P3 Jerry: pitch, open facts, approvals (SHADOW, synthetic win, nothing sent)

## Subject lines (pick one)
1. New Jersey municipality signs AI Audit to map how resident questions are handled
2. AI Audit agreed: seven business days to document what a response system would and would not handle
3. Before anything is built: a New Jersey municipality starts with a written AI Audit

## Pitch note (two sentences, for Joaquin to adapt)
A New Jersey municipality has signed an AI Audit agreement with The AI Agency Blueprint, covering how it handles routine resident questions by email and phone, with no build included. Our CEO Joaquin Garcia is available to discuss the approach, and the full release is attached. Target outlets: [PENDING: target outlets, Joaquin].

## Open facts (not in the release as facts, or placeholders)
- Signing date [DATE] and dateline city [CITY, NJ]: unconfirmed.
- Client name and municipality type (brief says township): client has NOT approved being named. Release says "a New Jersey municipality"; confirm that detail itself may be stated.
- Whether the signing is public, and whether any council or procurement step is involved (SOP: municipal matters not public are not announced). Needs Joaquin.
- Whether the agreement states it carries no commitment to later work (release says so, inferred).
- Whether "begins each engagement with the AI Audit" and "serves New Jersey municipalities and small businesses" may be stated.
- Boilerplate text: [PENDING: Joaquin approval]. Media contact name: [PENDING: name, Joaquin].
- Word count: the release is 331 words. It reaches 300 without invented facts, but the body is thin and partly restates the scope; I did not add more.

## Quote approvals needed
- Joaquin Garcia: drafted quote in the release, tagged [QUOTE PENDING approval: Joaquin Garcia]. Not final.
- Municipality: no quote exists and none was written. Needs written client approval for both naming and any quote.

## Checks
- press_check.py with --client "Township": PASS (331 words), no WARN.
- brand_scrub.py: PASS, 0 hits.
- Note: the word "township" is kept out of the whole file, because the checker flags it as a client name. If the real name is later approved, run with --approved-client.

## Questions for Joaquin
- May the release say "a New Jersey municipality" before the client approves being named?
- Is the signing public, and is any council or procurement step involved?
- Do you approve the drafted quote wording, or want to supply your own?
- What is the media contact name, and the approved boilerplate?
- Which outlets should the pitch target?

## Sources / Assumptions
- Win facts: Chief of Staff synthetic brief TRIAL-P3, 2026-10-08 (synthetic; no signed document seen).
- Positioning, phase, niches: /config/business.md. Contact: /config/footer.md. Rules: /sops/jerry-sop.md. Authority: /config/authority.md (Jerry shadow, send-authorized NO).
- Assumed: no prices, percentages, install or off-phase services stated; shadow log not appended, per brief.
