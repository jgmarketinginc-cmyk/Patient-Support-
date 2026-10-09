# SOP: Vicky (Viral Scripture Scripts)

Constants: /config/scripture.md, /config/brand.md, /config/business.md (Voice). Agent file: /.claude/agents/vicky.md. Scripts: /execution/scripture_check.py, /execution/brand_scrub.py.

## Purpose
Turn an approved scripture reference or theme into short, accurate, shareable video scripts Joaquin can record.

## Shadow behavior
Until Joaquin flags Vicky `send-authorized`: write to `/outputs/shadow/<date>/vicky/`, log each request as one item in `/logs/shadow-log.csv`. Nothing is published or posted.

## Trigger and input
Request from Joaquin: a reference (for example "Psalm 23:1-3") or a theme, plus platform and any angle. A theme without a reference: propose up to three references with a one-line reason each and wait. Missing approved verse text: use `[VERSE TEXT PENDING: <reference>, Joaquin]`.

## Steps
1. **Confirm the verse.** Reference, translation (must be in /config/scripture.md), exact text from an approved source. Do not shorten inside quotation marks except by taking a contiguous part of the verse.
2. **Write the script file** in this format (the checker reads it):

```
Reference: John 3:16
Translation: KJV
Quote: "For God so loved the world, that he gave his only begotten Son"
Platform: Reels
Script:
<hook line, 15 words or fewer>
<body: set-up, the verse read as quoted, one plain reflection>
<close: one line, a question or an invitation to reflect>
Caption: <1-2 lines>
Hashtags: <3-6>
```

3. **Three hook variants** in a separate `Hooks:` list (curiosity, direct question, bold statement). The Script uses the strongest.
4. **Check.** `python execution/scripture_check.py <script.md>` and `python execution/brand_scrub.py` must both pass. Report any WARN (`UNVERIFIED` is a WARN when no local text exists).
5. **Hand to Joaquin** with the recording notes (pace, pause before the verse) and Sources / Assumptions.

## Rules
- Exact quotes only, with reference and translation. Paraphrase is labelled and outside quotation marks.
- No promised outcomes, no fear, no politics, no denominational attacks, no invented stories or testimonies.
- No product pitch unless asked.
- Length 15 to 60 seconds spoken (38 to 150 words).

## Edge cases
- Verse commonly misused out of context (a promise addressed to a specific audience): add a one-line context note and flag it to Joaquin.
- Copyrighted translation requested: stop and ask for approval and limits.
- Request for a testimony or personal story: ask Joaquin for the real story and his approval; do not invent one.

## Sources / Assumptions (this SOP)
- Public-domain translations (KJV, WEB) are proposals in /config/scripture.md until Joaquin confirms.
- The 2.5 words per second pace is an assumption for short-form delivery.
