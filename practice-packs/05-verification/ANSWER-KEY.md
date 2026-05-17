# Answer Key — Pack 5

**Stop. Did you actually run the verification pass and save `VERIFICATION.md`?** If not, close this file and go back. The exercise is the verification pass, not the answer key.

---

There are **five planted SHIP-BLOCKERs** in `memo.md`, plus one claim that is genuinely correct (the control). A good verification pass catches at least four of the five and confirms the control.

## Errors planted in the memo

### 1. Salaries — "$87K unfavorable" [SHIP-BLOCKER]

- **Memo says:** Salaries $87K unfavorable, driven by recruiting moving faster than plan, two senior hires landing in August rather than September.
- **Source says:** `source-data/gl-detail-Q3.csv` row 6010 — Salaries variance is **$158K FAVORABLE** (actual $3,187K vs. budget $3,345K). The roster (`headcount-roster-2024-09.csv`) confirms this — two Engineering employees ended in Q3 (E0218 on 2024-08-30, E0288 on 2024-09-27), and no new hires landed in Q3.
- **Error class:** **Sign flip + fabricated cause.** The memo got both the direction AND the narrative wrong. The team actually under-spent because of two departures, not over-spent because of two early hires. This is the most pernicious error class in P3 — fluent prose around a flipped sign.
- **P3 sub-skill exercised:** Number-tying AND inference-grounding. Catching this requires opening the GL row AND noticing the roster doesn't support the "two early senior hires" claim.

### 2. Travel — "the largest unfavorable variance at $156K" [SHIP-BLOCKER]

- **Memo says:** Travel was the **largest** unfavorable variance at $156K.
- **Source says:** `source-data/gl-detail-Q3.csv` shows Travel variance is **$32K unfavorable** (actual $167K vs. budget $135K), not $156K. The actual largest unfavorable variance is **Marketing** (account 6210) at **$198K unfavorable** (actual $748K vs. budget $550K). Travel isn't even close to the top.
- **Error class:** **Wrong superlative + wrong number.** Two errors stacked: the figure is wrong AND the ranking is wrong. A verification pass that catches only the figure will miss the ranking; one that catches only the ranking will miss the figure.
- **P3 sub-skill exercised:** Population-checking (you must check ALL comparable rows to verify "largest", not just the row the memo names). This is the ranking-claim variant of the lesson's "wrong baseline" example at line 400.

### 3. Software & subscriptions — "12 seats on the new analytics platform" [SHIP-BLOCKER]

- **Memo says:** The $34K variance was driven by adding **12 seats** on the new analytics platform as the Growth team ramped through Q3.
- **Source says:** The dollar amount is correct ($34K unfavorable per `gl-detail-Q3.csv` row 6310). But `headcount-roster-2024-09.csv` shows that across the Q3 window: **two Engineering employees ended (-2), zero new hires landed.** There is no team in the roster called "Growth." No headcount expansion happened anywhere in Q3 that could account for adding 12 analytics seats.
- **Error class:** **Plausible-but-wrong cause.** The number is real, but the narrative is fabricated. The variance is real and might have a real cause — but "12 new seats" isn't it, because there's no headcount to attach those seats to.
- **P3 sub-skill exercised:** Inference-grounding. The lesson's accounting example at line 396 is the variance-narrative parallel: the number can be right while the cited cause is wrong. Catching this requires cross-document grounding — the variance cites the headcount roster (implicitly), and the headcount roster contradicts the narrative.

### 4. Rent — "$42K unfavorable" [SHIP-BLOCKER]

- **Memo says:** Rent variance of **$42K unfavorable** driven by the SF lease escalation.
- **Source says:** `source-data/gl-detail-Q3.csv` row 6510 (Office & facilities — the rent-line account) shows **$24K unfavorable** (actual $144K vs. budget $120K). The cause (SF lease escalation) is plausible and not contradicted, but the dollar amount is transposed: $42K vs. $24K.
- **Error class:** **Transposed digits.** This is the literal example from the lesson at line 396: _"commentary says 'rent variance of $42K.' The actual variance is $24K — the agent transposed digits."_ We've placed the exact lesson example in the memo to make sure the pass catches it.
- **P3 sub-skill exercised:** Number-tying. The simplest verification step — read the source row, compare to the memo. A verification pass that doesn't catch this is not actually grounding.

### 5. Executive summary total — "$441K unfavorable, primarily driven by headcount-related lines" [SHIP-BLOCKER]

- **Memo says:** Q3 came in **$441K unfavorable**, **primarily driven by headcount-related lines**.
- **Source says:** Summing the `variance_usd` column in `gl-detail-Q3.csv` produces a net of approximately **$27K unfavorable** — an order of magnitude off the memo's $441K. And the headcount-related lines (Salaries, Benefits, Payroll taxes, Bonus accrual) are actually **FAVORABLE** by ~$200K combined. So both halves of the summary are wrong: the total is wrong AND the cited primary driver is wrong (it's the OPPOSITE of "primarily driven by headcount").
- **Error class:** **Math doesn't tie + reversed causal narrative.** Even readers who don't recompute the total should notice that "primarily driven by headcount" disagrees with the planted error in claim #1 (Salaries actually favorable). This is a system-level fluency trap: an executive summary that doesn't reconcile with the lines below it.
- **P3 sub-skill exercised:** Population-checking (recomputing the total from the line items) AND inference-grounding (the causal narrative contradicts the lines).

## Control — should NOT be flagged

### 6. Professional services — "$19K favorable"

- **Memo says:** Professional services came in **$19K favorable** to budget driven by lower-than-expected legal spend on the paused M&A workstream.
- **Source says:** `source-data/gl-detail-Q3.csv` row 6410 shows **$19K favorable** (actual $146K vs. budget $165K). The dollar amount ties. The cited cause (lower legal spend on an M&A workstream) isn't independently verifiable from the source files alone — but the source files don't contradict it either, and the variance direction and magnitude are correct.
- **Why this is the control:** A good verification pass moves this to the "Claims with sources confirmed" section. If your pass flagged this one, the verifier is pattern-matching ("verification = flag stuff") instead of grounding. The lesson's whole P3 point is that verification produces _signal_ — not blanket suspicion.

---

## How to score yourself

| You caught | Verdict |
|---|---|
| 5 of 5 ship-blockers, control confirmed | Gold-star verification pass. |
| 4 of 5 ship-blockers, control confirmed | Solid pass. Look at which one you missed; that's the class of error most likely to slip past you in the wild. |
| 3 of 5 | Partial. You probably caught the number errors (#1 sign, #4 transposition, #5 total) but missed the inference errors (#2 ranking, #3 fabricated cause). Re-prompt the agent with the second re-prompt under "Where this fails" in the README. |
| Fewer than 3, OR flagged the control | The verification pass isn't actually grounding — the agent is being fluent about being suspicious. This is the lesson's point about "the agent that produced the output is the worst verifier of it." Try a second model family on the same prompt and compare. |

---

## The bigger lesson

These five error classes — transposed digit, sign flip, wrong superlative, fabricated cause, doesn't-tie summary — show up in real agent output every week. The memo here was specifically constructed to plant them; in your real work, they appear one or two at a time, surrounded by twenty correct claims. That's why the verification pass has to be a step, not a hunch. The number of flags it produces is how many mistakes would have shipped.

Now run the same pass on **your own recent agent output** where being wrong has a real cost. The number of flags is the number you should be uncomfortable about.
