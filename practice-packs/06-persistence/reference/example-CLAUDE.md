# Hiring loop: Senior PM, Growth team

## Job spec

Lives at `job-spec.md`. Required qualifications are the must-haves; preferred are signals weighted per `weighting.md`.

## Panel calibration

- Required-qualification gaps: hard fail, no further review.
- Preferred-qualification matches: count and weight per `weighting.md`.
- Credential discrepancies (school, dates, title): flag for human verification — never auto-accept.

## Where things live

- `/inbound`: incoming résumés as markdown
- `/shortlist`: candidates advanced to phone screen (one file per candidate, named `shortlist-CANDIDATE.md`)
- `/scorecards`: panel scorecards as `scorecard-CANDIDATE-INTERVIEWER.md`

## Critical rules

- Never include candidate names in scheduled-task outputs (privacy).
- Always flag credential claims (school dates, degree dates, title chronology) for human verification before advancing.
- Never auto-advance a candidate with a required-qualification gap. Required gap = hard fail, regardless of strength elsewhere.
- Tone in scorecards: factual, no subjective adjectives. "Shipped X with Y result" beats "great PM."

## Recurring task: inbound screen

When asked to screen `inbound/`, return one recommendation per candidate (ADVANCE / HOLD / DECLINE) with a one-sentence rationale that cites required-quals status and any credential flags. Save as `inbound-screen-YYYY-MM-DD.md`. Never modify résumés in `/inbound/`.
