# Handoff Contracts (machine-checkable)

Read by `execution/check_handoff.py`. These turn the prose contracts in `/runbook/RUNBOOK.md` into field checks. The `any` contract is always applied on top of the named one. Failing a `Required = Y` field fails the gate; `N` fields only warn.

Kinds:
- `regex`: the pattern must match somewhere in the output text (case-sensitive unless the pattern starts `(?i)`)
- `absent`: the pattern must NOT match in the output body (the Sources / Assumptions note is excluded)
- `json_key`: the output must be a JSON object containing this key
- `json_len`: spec `key=N`, the JSON list at `key` must have exactly N items
- `max_price`: every dollar amount in the output body (Sources / Assumptions excluded) must be at or below the spec (the $1,500 entry offer; anything above is written-proposal only)

Cell delimiter is ` | ` (with spaces); a bare `|` inside a cell is regex alternation.

| Contract | Field | Kind | Spec | Required |
|---|---|---|---|---|
| any | sources_assumptions | regex | (?i)sources\s*/\s*assumptions | Y |
| frannie-mark | apollo_contact_id | regex | Apollo\s+[A-Za-z0-9-]*\d | Y |
| frannie-mark | qualified_flag | regex | (?i)qualified|ready to buy | Y |
| frannie-mark | pain_with_timestamps | regex | \(\d{1,2}:\d{2}\) | Y |
| frannie-mark | hours_and_wage | regex | (?i)\d+\s*(hrs|hours) | N |
| frannie-mark | decision_maker | regex | (?i)decision-?maker | Y |
| frannie-mark | objections | regex | (?i)objection | Y |
| frannie-mark | escalation_items | regex | (?i)escalat|flags | Y |
| frannie-cody | no_price_above_entry | max_price | 1500 | Y |
| frannie-cody | no_discount | absent | (?i)discount|% off|percent off | Y |
| mark-cody | option_structure | regex | (?i)three options|3 options|option | Y |
| mark-cody | rationale_in_prospect_words | regex | "[^"]{8,}" | Y |
| mark-cody | no_result_claims | absent | (?i)guarantee[d]? (savings|results)|case study | Y |
| mark-dolly | format | regex | (?i)cover|diagram|one-pager|social graphic | Y |
| mark-dolly | in_scope_workflow_steps | regex | (?i)workflow|intake|steps? | Y |
| mark-dolly | client_name_gate | regex | (?i)client name|joaquin approves | Y |
| aaron-cody | apollo_id | json_key | apollo_id | Y |
| aaron-cody | name | json_key | name | Y |
| aaron-cody | title | json_key | title | Y |
| aaron-cody | org | json_key | org | Y |
| aaron-cody | city | json_key | city | Y |
| aaron-cody | niche | json_key | niche | Y |
| aaron-cody | tier | json_key | tier | Y |
| aaron-cody | trigger_line | json_key | trigger_line | Y |
| aaron-cody | email_status | json_key | email_status | Y |
| cody-patty | prospect_id | json_key | prospect_id | Y |
| cody-patty | emails | json_len | emails=3 | Y |
| cody-patty | linkedin_note | json_key | linkedin_note | Y |
| cody-patty | sender | json_key | sender | Y |
| cody-patty | footer_ref | json_key | footer_ref | Y |
| cody-patty | sources_assumptions | json_key | sources_assumptions | Y |
| patty-aaron | capacity_tomorrow | regex | capacity_tomorrow | Y |
| angelina-patty | prospect_id | json_key | prospect_id | Y |
| angelina-patty | emails | json_len | emails=3 | Y |
| angelina-patty | linkedin_note | json_key | linkedin_note | Y |
| angelina-patty | sender | json_key | sender | Y |
| angelina-patty | footer_ref | json_key | footer_ref | Y |
| angelina-patty | sources_assumptions | json_key | sources_assumptions | Y |

Assumption: the `aaron-cody` JSON key names follow the runbook's field list (Apollo record ID, name, title, org, city, size, niche, tier, trigger line, verified email status). Joaquin or Aaron's SOP may use different key spellings; adjust here if so.
