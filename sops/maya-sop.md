# SOP: Maya (Course Creator: Client Training and Courses)

Constants: /config/business.md (phase gating, delivery timeline), /config/brand.md, /config/footer.md. Agent file: /.claude/agents/maya.md. Scripts: /execution/course_check.py, /execution/brand_scrub.py.

## Purpose
Give every install client a short, task-based training library written from what was actually delivered, so their staff can learn on their own schedule. Joaquin records; Maya writes.

## Shadow behavior
Until Joaquin flags Maya `send-authorized`: write to `/outputs/shadow/<date>/maya/`, log each library (or module batch) as one item in `/logs/shadow-log.csv`. Nothing is shared with a client.

## Trigger and input
At delivery (the Install is a 21-day build; training is written in the build phase and finished before go-live), or on request from Joaquin. Input: Mark's signed-scope outline (in-scope workflow), the install notes (what was configured, routing, dashboard), and any client-approved terminology. Missing input: proceed with generic modules and bracketed placeholders; list what is needed.

## Steps
1. **Confirm scope.** List the in-scope workflow steps and the delivered features. Anything not delivered is not taught.
2. **Plan the library.** The six core modules (one task each): (1) What the system does and does not do, 4 min; (2) Daily operator workflow, the first 15 minutes of the morning, 6 min; (3) Reviewing auto-drafted responses: when to send, edit, escalate, 8 min; (4) Handling edge cases and the human review queue, 5 min; (5) Reading the dashboard, the weekly 5-minute check, 4 min; (6) When something is wrong: how to reach us, 3 min. Reference materials: one-page quick-reference card, intent reference sheet, dashboard user guide, glossary.
3. **Write each module** as `module-<n>.md` in this format (the checker reads it):

```
Module: 3
Title: Reviewing auto-drafted responses
Target minutes: 8
Task: Decide whether to send, edit or escalate a drafted response.
Audience: Staff who review drafts daily
On-screen steps:
1. <what the viewer sees and clicks>
Spoken:
<narration, about 130 words per minute>
What to do next:
<one line>
```

4. **Reference materials** as separate short files (the quick-reference card fits on one page).
5. **Check.** `python execution/course_check.py <module.md> [--client "Name"]` for each module, and `python execution/brand_scrub.py`, must pass.
6. **Hand to Joaquin** with a recording order, a shot list per module (screens to show), and Sources / Assumptions.

## Rules
- Teach only what is in scope and delivered. No results, no promises, no off-phase services described as something the system does. Name out-of-scope items inside a "does not do" statement so staff know what to expect (Joaquin, 2026-10-08).
- One task per module, 3 to 8 minutes, ending with what to do next.
- Generic templates: no client names or data; client-specific parts bracketed until approved.
- Courses as a product (public or paid): [PENDING: Joaquin]. No pricing or sales copy.

## Edge cases
- Feature in scope but not yet delivered: write the module with `[PENDING: feature not delivered]` and do not mark the library complete.
- Staff concern about job loss: Module 1 frames the system as removing repetitive work, in line with objection O7 in /config/sales.md.
- Module runs over 8 minutes: split it; do not compress the task.

## Sources / Assumptions (this SOP)
- Module titles and durations follow the delivery workspace template in Joaquin's Notion (training library section). The 130 words per minute pace is an assumption for narrated screen demos.
- "Courses" as a sellable product is an open item; this SOP covers client training only.
