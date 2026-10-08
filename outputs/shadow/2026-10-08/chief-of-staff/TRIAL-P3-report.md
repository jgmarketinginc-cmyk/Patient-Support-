# Chief of Staff trial report: TRIAL-P3 (Phase 3 first runs)
Venture: aiab | SHADOW, synthetic briefs, nothing published, sent, posted or shared | Date: 2026-10-08

## Results (all four agents called in parallel, one call each, gates re-run by the Chief of Staff)
| Agent | Output | Checker | Chief of Staff verdict |
|---|---|---|---|
| Vicky | `outputs/shadow/2026-10-08/vicky/trial-psalm-23-1-script.md` | scripture_check PASS (89 words, ~36 s), 2 expected WARNs (KJV unconfirmed, verse UNVERIFIED) | Pass. Only the supplied verse is in quotation marks. David background lines are unverified general knowledge (flagged by Vicky). |
| Angelina | `outputs/shadow/2026-10-08/angelina/trial-email-es.txt` (+ source extract, glossary and flags) | translation_check PASS, 2 expected WARNs (not certified; footer left in English) | Pass. Price, dates, names, footer exact; idioms replaced and flagged with back-translations. |
| Jerry | `outputs/shadow/2026-10-08/jerry/trial-release.md` (+ pitch and open facts) | press_check PASS at 331 words, then FAIL after two rules were added from this review | **Rework needed.** (1) "Mr. Garcia" assumes gender; use "Garcia". (2) Two paragraphs are internal compliance notes written as public copy ("no case studies ... no claims about results", "the municipality has not approved being named"). They pad the release past 300 words. Removing them leaves about 250 words, under the 300 floor. |
| Maya | `outputs/shadow/2026-10-08/maya/trial-module-1.md`, quick-reference card, recording notes | course_check PASS (506 words, ~3.9 min) | Pass. Teaches only the five in-scope steps; placeholders for client names. Cannot name out-of-scope items (checker bans the words), so the "does not do" list is generic. |

## Changes made because of this review
- `press_check.py`: FAIL on honorifics (Mr./Ms./Mrs./Miss); WARN on internal compliance language in public copy. Tests added (53 pass).

## Decisions for Joaquin
1. **Press release length floor.** The 300-word floor (my default, not a rule you set) pushed Jerry to pad a thin-fact announcement. Lower it to 200 (recommended), or keep 300 and accept that small wins need more facts?
2. **Out-of-scope items in training.** Maya's checker rejects the words "inspection" and "scheduling" anywhere, so she cannot tell staff what the system does NOT handle by name. Allow those words inside a "does not do" list, or keep generic?
3. Scripture: confirm KJV and/or WEB, approve a verse text source, name the venture, who records, platforms and cadence; keep the David background lines?
4. Spanish: native-speaker reviewer, approved Spanish opt-out wording, whether Spanish is wanted for this contact; keep "CEO" or use "director ejecutivo"?
5. Press: may a release say "a New Jersey municipality" before the client approves being named; is the signing public or any council step involved; approve the quote; media contact, boilerplate, target outlets; confirm "begins each engagement with the AI Audit" and "does not commit the municipality to later work".
6. Training: should the named human operator be named on screen; slide-only recording for Module 1; point to the quick-reference card as a handout?

## Sources / Assumptions
- Agents' own reports and files, re-checked with `scripture_check.py`, `translation_check.py`, `press_check.py`, `course_check.py`, `brand_scrub.py` run by the Chief of Staff.
- Verse text for the Vicky trial was supplied by the Chief of Staff from memory of the KJV for testing only; it is UNVERIFIED.
- All inputs are synthetic; none of this counts toward any exit test (real approved items only).
