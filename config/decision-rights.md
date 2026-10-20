# Decision Rights: Chief of Staff vs Joaquin

Read by the Chief of Staff SOP, `execution/route_request.py` and `execution/plan_run.py`. Only Joaquin edits this file. If a matter is not clearly in the first table, it is Joaquin's.

The `Keywords` column is a `|`-separated list of regex fragments (case-insensitive) used by `route_request.py` to flag a request. It is a safety net, not the whole policy: the Chief of Staff applies the matter column in its own judgment too.

## Chief of Staff decides (no need to ask Joaquin)

| ID | Matter | Keywords |
|---|---|---|
| C1 | Choose the workflow or the owning agent for a request | route|assign|who should |
| C2 | Sequence steps and run independent steps in parallel (max 6 concurrent) | sequence|parallel|in order |
| C3 | Send agent output back for rework once, with the specific defect | re-run|rerun|redo|rework|retry |
| C4 | Halt a failed branch and report it | halt|stop the run |
| C5 | Prioritize work within the current phase | prioriti[sz]e|what first |
| C6 | Resolve overlaps or conflicts between agents | overlap|conflict between |
| C7 | Run the runbook cadence (daily, weekly, on-demand playbooks) | run the day|run the week|daily run|weekly run |
| C8 | Decide what is worth Joaquin's attention and consolidate reports | summari[sz]e|status report|state of the team |
| C9 | Draft proposed edits to routing, playbooks, registry and SOPs | propose |

## Joaquin decides (Chief of Staff stops and escalates, even when confident)

| ID | Matter | Keywords |
|---|---|---|
| J1 | Any authority flag, or an agent moving between shadow and live | authority|send-authorized|go live|go-live|flip |
| J2 | Current phase or the service menu | change (the )?phase|service menu|add a service |
| J3 | Prices, terms, discounts | price|pricing|discount|deposit|payment terms|retainer tier |
| J4 | Contracts, including custom or municipal contracts, procurement | contract|agreement|procurement|council |
| J5 | Anything leaving the system: sends, posts, publishes, grant or funder submissions | send (it|this|the)|publish|post it|submit|file the application |
| J6 | Anything that spends money or paid credits | spend|budget|buy credits|paid |
| J7 | Brand, footer, signature | brand|footer|signature|logo |
| J8 | Onboarding, retiring or re-scoping an agent | onboard|retire|new agent|add an agent |
| J9 | Resetting or waiving a critical-error clock | critical error|reset the clock|waive |
| J10 | Send caps and capacity limits | send cap|daily cap|capacity limit |
| J11 | Anything outside the service menu | outside the menu|out of scope|custom build |
| J12 | Naming or confirming facts about ventures that are PENDING | confirm the venture|venture name |
