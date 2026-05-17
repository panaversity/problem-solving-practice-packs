# Pack 5 — Q3 Variance Memo Verification

**Serves:** Practice 3 (P3) of the Problem-Solving Crash Course.

The goal of this pack is to practice **grounding output to source**: take a finished-looking deliverable, run a verification pass against the underlying files, and count the flags the agent finds. The number itself is the punchline — that is how many mistakes would have shipped.

---

## What this pack contains

```
05-verification/
├── README.md                          (this file)
├── deliverable/
│   └── Q3-variance-memo-DRAFT.md      A one-page variance memo, ready to forward
└── sources/
    ├── gl-detail-Q3.csv               GL line-item detail the memo cites
    ├── budget-Q3.csv                  Original Q3 budget
    └── headcount-roster-2024-09.csv   Headcount roster the memo cites for one claim
```

You are the controller at a mid-size SaaS company. Your FP&A analyst dropped the Q3 variance memo in your shared folder. You are supposed to forward it to the CFO this afternoon. Before you do, you want to confirm every cited number ties to the underlying GL detail, and that every named cause is actually supported by the source.

The memo reads professionally. The errors only surface when you cross-reference against the CSVs.

---

## Set up the exercise

1. Unzip `pack-5-verification.zip` into a fresh folder.
2. Open that folder in your AI assistant of choice (Claude Code, OpenCode, Cowork, OpenWork — anything with file access).
3. Make sure the assistant has read access to both `deliverable/` and `sources/`.

No installs, no accounts. The inputs are read-only.

---

## The exact prompt to paste

```text
The file deliverable/Q3-variance-memo-DRAFT.md is a draft variance memo
that is about to go to the CFO. Your job is to verify it before it ships.

Run a verification pass:

  1. List every factual claim in the memo. A "factual claim" is any
     specific dollar amount, percentage, ranking ("the largest", "the
     primary driver"), causal statement, or count of people / items.

  2. For each claim, identify the source file (sources/gl-detail-Q3.csv,
     sources/budget-Q3.csv, sources/headcount-roster-2024-09.csv) and
     the specific row(s) that should support it.

  3. Quote or compute the supporting value from the source. If the
     source disagrees with the memo, or if no row supports the claim,
     FLAG it.

Save the result as VERIFICATION.md in the current directory, with
two sections:

  ## Claims with sources confirmed
  | Claim | Source file:rows | Memo value | Source value | Status |

  ## Flags — claims that did not survive verification
  For each flag:
    - The claim, verbatim from the memo
    - The source rows you checked
    - What the source actually says
    - Severity: SHIP-BLOCKER (number wrong / ranking wrong / cause unsupported)
                or MINOR (immaterial / cosmetic)

Constraints:
  - Read-only. Do not edit the memo or any source file.
  - Output must be a saved file (VERIFICATION.md), not just chat.
  - If a claim involves a ranking ("largest", "primary driver"), you
    must check every comparable row, not just the one the memo names.
```

---

## What success looks like

A good run produces a saved `VERIFICATION.md` that catches **at least four of the five planted errors as SHIP-BLOCKERs**. Score yourself on these:

- [ ] **The agent saved a file.** No `VERIFICATION.md` on disk is the same P3 failure as P1: must produce an artifact, not narrate in chat.
- [ ] **The Rent transposition is flagged.** The memo says rent variance is $42K; the GL detail says $24K. This is the lesson's literal "transposed digits" example. If the agent misses this, the verification pass is not working.
- [ ] **The Salaries sign-flip is flagged.** The memo says salaries are unfavorable by $87K. The GL detail sums to a favorable $63K. Tests whether the agent computed the variance from the source instead of taking the memo's word for it.
- [ ] **The wrong superlative is flagged.** The memo calls Travel ($156K) "the largest single unfavorable variance." Marketing is the actual largest at roughly $270K, and Travel's true variance is around $52K, not $156K. Tests whether the agent checked the ranking claim against all comparable rows.
- [ ] **The fabricated cause on Software & subscriptions is flagged.** The $34K variance is real, but the memo attributes it to "adding 12 seats of the new analytics tool." The headcount roster shows the team shrank net 2 over Q3, with no analytics-team additions. Tests cross-document grounding: claim cites the roster, roster doesn't support it.
- [ ] **The "$441K total / primarily headcount" summary is flagged.** Recomputing from the six line variances actually gives roughly $298K, not $441K. And because Salaries are favorable, "primarily driven by headcount" is doubly wrong. Tests whether the agent recomputed the total from the listed lines.
- [ ] **Professional services is in the "Confirmed" section, not flagged.** The memo says favorable by $19K; the GL detail agrees. This is the control. If everything gets flagged, the verification pass produces noise, not signal.
- [ ] **Each flag cites specific row(s) of a specific source file.** "The memo is wrong about rent" is not a verification. "gl-detail-Q3.csv rows 2-4: Rent variance sums to $24K; memo claims $42K" is. P3 is about *grounding to source*, not about plausibility.

### Stretch (gold-star)

If the agent also notes it cannot independently verify the EMEA-expansion narrative — "the source files don't tell me whether this is a real cause or back-fill" — that is exactly the litigation-style observation P3 wants. Worth calling out as the highest-quality outcome.

### Where this fails

- **Agent over-flags everything,** including Professional services. That means it is pattern-matching ("verification pass = flag stuff") instead of grounding. Re-prompt: _"For each flag, paste the source row. If you cannot paste a contradicting source row, move it to Confirmed."_
- **Agent flags only the obviously-wrong numbers and misses the sign-flip / wrong-superlative / fabricated-cause.** That means it is doing *surface* verification (does the number look weird?) instead of *grounding* (what does the source actually say?). Re-prompt: _"For every ranking claim, list the top three comparable rows in the source and show that the memo's named row is in fact the top."_
- **Agent invents source rows.** This is the meta-failure: the verifier hallucinating sources. You can spot this by opening the cited CSV and searching for the row. If a "cited" row doesn't exist, the verifier itself failed P3 — which is the lesson's point about "the agent that produced the output is the worst verifier of it." This is the moment to switch to a different model family and re-run.

---

## Why this exercise

In the crash course (Practice 3), the variance-memo vignette is one of the two canonical examples of "the output looks right but breaks in production." This pack lets you run that vignette **with a deliverable that actually fails verification** — not a thought experiment, an artifact you can flag claim-by-claim against real source files. The skill you are training (asking the agent to ground every claim to a source, before the deliverable ships) is the highest-leverage habit in P3.

When you are ready, repeat this on a real deliverable from your own work: a memo, a brief, a report you are about to send. Save the verification file. The number of flags is your answer to "would this have shipped clean?"

---

## Optional engineering extension

For readers who want the SQL angle from the lesson:

> The `gl-detail-Q3.csv` is small enough to load into the free tier of any Postgres or SQLite session. Ask the agent: _"Load gl-detail-Q3.csv into a SQL table. Then, before running it, show me the query you'd write to find the single largest unfavorable variance."_ Read the query. Predict the answer. Then run it. That is exactly the boss-finance discipline from the lesson — verify the query before trusting the number.

We don't ship the SQL setup in the pack — it would balloon scope. Just point at it when you are ready.
