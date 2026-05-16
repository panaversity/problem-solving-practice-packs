# Pack 4 — Four-Phase Worked Example

**Serves:** Part 10 capstone of the Problem-Solving Crash Course.

The goal of this pack is to run the full **Explore → Plan → Implement → Commit** loop once, consciously naming which principle each phase invokes. You will produce a real artifact at every phase, in order, and the final output will be a redline review of an inbound vendor MSA.

This is the **capstone exercise** for the crash course. Budget 30-40 minutes the first time.

---

## What this pack contains

```
04-worked-example/
├── README.md                           (this file)
├── CLAUDE.md                           folder-level rules for the agent
├── inbound/
│   └── vendor-msa-v1.md                ~1,100-word vendor MSA (12 clauses)
└── redline-standard.md                 firm's redline standard (11 sections)
```

The scenario: a vendor (Sample Vendor Co.) has sent an MSA. You need to produce a redline review memo identifying every deviation from your firm's redline standard, with severity, with quoted text from both documents, and with proposed counter-language.

Both files are fictional. The vendor MSA contains **at least eight deviations** from the standard, ranging from `HIGH` (three-month liability cap with no carve-outs) to `LOW` (Net 15 instead of Net 30). The decomposition into four phases will surface them in a controlled way.

---

## Set up the exercise

1. Unzip `pack-4-worked-example.zip`.
2. Open the folder in your AI assistant. Confirm it can read `CLAUDE.md`, `inbound/vendor-msa-v1.md`, and `redline-standard.md`.
3. Note that **`CLAUDE.md` is loaded automatically** by Claude Code and many other assistants when present in the working directory. If your assistant does not auto-load it, paste its contents at the start of your session.

---

## The four phases — exact prompts

Paste each phase **as a separate prompt**, in order. **Read each output and pause before the next.** The pause is the entire point of P4.

### Phase 1 — Explore (P1 + P7)

```text
Don't draft anything yet. Read inbound/vendor-msa-v1.md and
redline-standard.md. Summarize:
  - What this MSA is for (one paragraph)
  - The clause structure of the MSA (numbered outline, by section number)
  - Any obvious deviations from our redline standard (bullets, max 7)
Save the summary to vendor-msa-explore.md. No drafting yet.
```

**What to check** before moving on:

- A saved `vendor-msa-explore.md` exists.
- The MSA outline lists all twelve sections by number, not paraphrased.
- The deviations list quotes both documents (per `CLAUDE.md` rule 2). If the agent's deviations are paraphrased, send it back: _"Re-do the deviations list with exact quotes from both documents."_

### Phase 2 — Plan (P2 + P5)

```text
Read vendor-msa-explore.md. Produce a redline plan with the following
structure exactly:

  ## Redline plan
  - Clauses to review in depth (max 6, by MSA section number)
  - Deviations to flag (numbered, severity HIGH / MED / LOW,
    one line per deviation)
  - Counter-proposals (numbered, parallel to deviations,
    one line per counter)
  - Open questions for the vendor (numbered, max 3)

Save to msa-plan.md. Pause for my approval before continuing.
```

**What to check** before moving on:

- Severity labels are exactly `HIGH`, `MED`, `LOW` (per `CLAUDE.md` rule 3). Anything like "Critical" or "P1" means the agent ignored the rules file.
- At least one `HIGH` is identified. The MSA's three-month liability cap (Section 7.1) and the auto-renewal with 90-day notice (Section 2) are both `HIGH`. If neither is flagged HIGH, the plan is wrong — send it back.
- The plan is saved to a file (per `CLAUDE.md` convention), not just chat output.

### Phase 3 — Implement (P4 + P3)

```text
Execute the plan from msa-plan.md one deviation at a time. For each
numbered deviation:

  1. Produce a one-page deviation memo with:
       - Section header: "Deviation N — <short title>"
       - Exact MSA quote (in a quote block, with section cite)
       - Exact redline-standard quote (in a quote block, with section cite)
       - Severity (HIGH / MED / LOW)
       - Why this matters (3-5 lines)
       - Counter-language (a redline draft of the clause, marked as
         additions/deletions)
  2. Save it to stepN.md (step1.md, step2.md, ...)
  3. Wait for my OK before moving to deviation N+1.

If you cannot quote the source text for a deviation, flag it instead of
drafting counter-language.
```

**What to check** after each step:

- Both quotes are real. Grep the source: `grep -F "<MSA quote>" inbound/vendor-msa-v1.md` should hit. Same for the redline-standard quote.
- Severity matches the rules-file definitions in `CLAUDE.md`. A unilateral cap with no carve-outs is `HIGH`, full stop.
- Counter-language is **specific text**, not just "negotiate down". A redline that says "the parties should discuss this" is not a redline.

### Phase 4 — Commit (P6 + P7)

```text
Final verification pass:
  - Every flagged deviation has matching quotes from both documents
  - Every counter-language proposal is specific text, not commentary
  - Severity labels are exactly HIGH / MED / LOW
  - Tone matches CLAUDE.md (cite both section numbers, no paraphrase)

Then assemble vendor-msa-final.md containing:
  - A 3-line executive summary
  - The deviation memos (step1.md through stepN.md) in order
  - A "What I should review by eye before sending" list (max 5 items)
  - A "Rules-file proposals" section: if anything in this review
    suggests a rule we should add to CLAUDE.md, propose the exact lines.

Do not modify CLAUDE.md yourself — propose the lines in the final file
and let me decide.
```

---

## What success looks like

This is the capstone, so the bar is higher than the individual packs.

### Phase-by-phase checks

- [ ] **Each phase produced its own saved artifact.** Files exist for `vendor-msa-explore.md`, `msa-plan.md`, `step1.md`, `step2.md`, …, and `vendor-msa-final.md`.
- [ ] **The plan was read and edited before Phase 3 began.** If you paste all four prompts back-to-back with no pause, you ran a big-prompt, which is what Pack 3 is for, not this one.

### Content checks (these are why the pack exists)

- [ ] **At least eight deviations are identified.** The MSA contains, at minimum: 3-year Initial Term + 90-day non-renewal (Sec 2), Net 15 (Sec 3.2), 15% annual escalator (Sec 3.3), aggregated-data free use (Sec 5.2), 2-year confidentiality (Sec 5.3), workmanlike-only warranty (Sec 6), 3-month liability cap with no carve-outs (Sec 7.1), modify-procure-refund only IP indemnity (Sec 8.1), no termination for convenience (Sec 9.2), Vendor-only assignment (Sec 12.2). Missing more than two of these = the review is not shippable.
- [ ] **At least two `HIGH` severities are assigned**, and they include the liability cap (Sec 7.1) and either the auto-renewal terms (Sec 2) or the assignment asymmetry (Sec 12.2-12.3).
- [ ] **Quotes from both documents appear in every deviation memo.** Pick three deviations at random and grep the source files — both quotes must hit.
- [ ] **Counter-language is specific redline text** (additions, deletions, replacement clause), not procedural commentary.
- [ ] **The Rules-file proposals section is non-empty** and contains at least one proposed line. Examples a strong run produces: "Initial Term ≤ 1 year is firm policy; flag any deviation as HIGH automatically" or "Aggregated-data clauses default to HIGH unless opt-in language is present."

### Where this fails

- **The agent skipped Phase 2 and went straight to drafting.** That is the most common failure on capstone runs: the model wants to be helpful. Re-anchor: _"Stop drafting. Produce only the plan first and pause."_
- **All deviations are flagged the same severity.** That means severity discipline was not applied. Re-read `CLAUDE.md` rule 3 to the agent and re-run Phase 3.
- **Paraphrased quotes.** If `grep -F "<quoted phrase>" inbound/vendor-msa-v1.md` does not hit, the quote is invented or summarized. That fails P3 (verification) regardless of how the rest of the memo looks.

---

## Five questions to journal after

Per the crash course Part 11 Capstone Exercise:

1. **Total time** vs. how long this review would have taken without the four-phase decomposition.
2. **Which phase was hardest** to actually stop after? (Most people fail to stop after Phase 2.)
3. **What got added to the rules file?** What rule would have caught the most expensive error you saw?
4. **What constraint did you tighten** in `CLAUDE.md` as a result?
5. **Which failure pattern showed up** in your run: Drift / Confident Wrong / Big Bang / Scope Creep / Black Box?

---

## The compounding step

Re-run a redline review next week using the rules file you produced. The second run is usually 40-60% faster because the rules file does the work that was previously in your prompt. That is the whole point of P5 (persistence) graduating P4 (decomposition).
