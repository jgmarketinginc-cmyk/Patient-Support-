# ROI table: Reyes Property Management (sample) | RUN-20261008-001 s2

SYNTHETIC SAMPLE, SHADOW MODE. Output of `python execution/roi_calc.py` on `cos-RUN-20261008-001-s2-roi-inputs.json`. Target range, not a guarantee. No client results exist yet.

Inputs, from the prospect's own words:
- Hours: 15 per week, office manager answering tenant questions (transcript 00:48: "about 15 hours a week just answering those").
- Wage: $28 per hour (transcript 00:48: "I pay her $28 an hour").
- Loaded-cost multiplier 1.0 (wage only, config/sales.md, SET). Weeks per year 52 (SET).
- Share of hours replaced: 50% and 70% (positioning target range, config/business.md).

| Option | Replaced | Hrs/wk | Annual savings | Net monthly | Payback (months) |
|---|---|---|---|---|---|
| Option 1: AI Audit ($1,500) | n/a | n/a | n/a | n/a | n/a (diagnostic, no hours replaced; no savings claimed) |
| Option 2: AI Operations Install ($18,000) | 50% | 7.5 | $10,920 | $910 | 19.8 |
| Option 2: AI Operations Install ($18,000) | 70% | 10.5 | $15,288 | $1,274 | 14.1 |
| Option 3: Install + Managed Operations, 1-workflow tier ($18,000 + $2,400/mo) | 50% | 7.5 | $10,920 | -$1,490 | no payback on labor savings alone |
| Option 3: Install + Managed Operations, 1-workflow tier ($18,000 + $2,400/mo) | 70% | 10.5 | $15,288 | -$1,126 | no payback on labor savings alone |

Plain reading:
- The Audit is a diagnostic. It replaces no hours, so no savings are claimed. Its fee is not credited toward the Install.
- The Install pays back on labor savings alone in about 14 to 20 months across the 50-70% range, at the stated 15 hours and $28.
- Option 3 does NOT pay back on labor savings alone. The $2,400/mo retainer exceeds monthly labor savings ($910 at 50%, $1,274 at 70%). Its case rests on things this table does not price (operator oversight, urgent items not buried), which are not quantified here.
- The table counts wage only. It does not price the missed leak ticket (01:31) or the avoided second hire (06:46); neither has a figure from the prospect.

Sources: cos-RUN-20261008-001-s2-roi.json; S1-transcript.txt 00:48; config/sales.md; config/business.md.
