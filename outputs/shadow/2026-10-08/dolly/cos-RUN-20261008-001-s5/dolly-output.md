# Dolly output: proposal visual pack | RUN-20261008-001 s5

SHADOW MODE, SYNTHETIC SAMPLE. Local files only. Nothing sent or shared. Not logged in shadow-log.csv (per CoS brief).

## Files
| Asset | Primary | Alternate |
|---|---|---|
| Options comparison table (3 columns) | options_table-primary.svg | options_table-alternate.svg |
| Workflow diagram (5 in-scope steps) | process_diagram-primary.svg | process_diagram-alternate.svg |

Primary = white background, navy header and footer bands. Alternate = navy background, gold header and footer bands, white text.
Editable source: the SVGs themselves (open in Figma, Canva or a browser) plus options_table-spec.json and process_diagram-spec.json. Build reports: *-build-report.json.
Builders: execution/dolly_build.py (diagram); NEW execution/dolly_table.py (table; dolly_build.py has no table format; it reuses that script's brand and footer readers).

## Brand
Colors and fonts SET (config/brand.md). Footer read from config/footer.md. Wordmark is text only. PLACEHOLDER settings used: none. Logo: PENDING Joaquin (not used, not invented).

## Checks
- asset_check.py (with --client Reyes --client Dana): PASS on all 4 SVGs.
- brand_scrub.py: PASS, 0 hits.
- Not verified visually: no SVG renderer in this environment. Step 4 box text runs 6 lines, close to the box bottom; open in a browser before use.

## Deviations from the brief (forced by the SOP and checker; Mark's figures are unchanged where shown)
- Prices: SOP says prices do not appear on assets, and asset_check fails any amount above $1,500. Table shows $1,500 (Audit) and "See written proposal" for the $18,000 Install and the $2,400/mo retainer. Deposit/balance amounts ($9,000) are likewise omitted.
- Payment for Option 2 reads "Half at signing (deposit); balance at 21-day delivery" because the checker rejects percentage text.
- Payback label: the exact wording "target range, not a guarantee" fails the checker (the word "guarantee"). Used "Target range; no results are promised." Payback figure "About 14.1 to 19.8 months" kept as given; the 70%/50% replacement shares are omitted (percent rule).
- Checker, SOP and brand files were not edited.

## Excluded
No client name, unit count, town or contact name ("Your business" used). No testimonials, stats or results imagery. No inspections, scheduling, work-order handoff, document intake or platform. Diagram shows only Mark's five steps.

## Sources / Assumptions
Sources: Mark's outline (Three options section and To Dolly brief) cos-RUN-20261008-001-s2-proposal-outline.md; cos-RUN-20261008-001-s2-roi-table.md (payback 14.1 to 19.8; Option 3 no payback); config/brand.md, footer.md, business.md, authority.md (Dolly shadow, send-authorized NO); sops/dolly-sop.md.
Assumptions: scope text condensed from Mark's wording with the client name and timestamps removed; "tenant questions" kept as the workflow description; Option 3 payback line taken from Mark's table; format (table plus diagram) is Mark's suggestion, not confirmed.

## Questions to Joaquin
- Format: confirm table plus diagram as the pack (Mark noted no format is fixed).
- Prices above $1,500 and the percent-based payment split: keep them off assets (SOP/checker), or authorize an exception for a proposal-only table (needs a rule change, which only you can make)?
- Payback label: approve "Target range; no results are promised" in place of "target range, not a guarantee", or relax the checker's "guarantee" rule for this label?
- Client name: approve use of one, and in what form? Until then assets show "Your business".
- Logo: still pending.
