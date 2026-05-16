# Pack 3 — Big-prompt vs Decomposed Task

**Serves:** Practice 4 (P4) of the Problem-Solving Crash Course.

The goal of this pack is to feel the "Big Bang" failure pattern firsthand: one overloaded prompt buries a problem in step three that you do not notice until step seven, and the cheapest correction point was already gone. Then you run the same task decomposed and feel the difference.

---

## What this pack contains

```
03-decomposition/
├── README.md                          (this file)
└── inputs/
    ├── case-brief.md                  fictional B2B contract dispute
    └── firm-style-guide.md            voice/structure rules + banned phrases
```

The scenario: Acme Logistics has paid a software vendor $153,000 for a CRM platform that does not work. The client wants a pre-suit demand letter sent **today**. You will ask an AI assistant to draft it.

The firm style guide has **strict rules** the letter must follow: exact section order, banned phrases, numeric discipline, and explicit rules about what **never** goes in a demand letter (notably: the client's settlement floor and operational damages estimates that are not yet documented to a litigation standard). All of those are easy to violate when the agent is doing too many things at once.

> **Names are fictional.** Acme Logistics, Sample Vendor Co., Sarah Chen, Marcus Webb, Janet Liu — none of these are real people or companies. Treat the brief as a worked example, not legal advice.

---

## Set up the exercise

1. Unzip `pack-3-decomposition.zip`.
2. Open the folder in your AI assistant. Confirm it can read both files in `inputs/`.

---

## The exact prompts to paste

You will run **two flows**, save both outputs, and compare.

### Run A — the big-prompt flow (one shot)

Paste this verbatim:

```text
Read inputs/case-brief.md and inputs/firm-style-guide.md. Draft a
complete pre-suit demand letter from this firm to Sample Vendor Co.'s
general counsel.

Follow the firm style guide exactly. Include the recital of facts,
the legal theory, the demand, and the deadline. Make it ready to send.

Save it to outputs/letter-A-big-prompt.md.
```

That is one prompt. Let the agent produce the whole letter in one pass.

### Run B — the decomposed flow (four steps)

You will paste **four separate prompts**, in order. **Read the output and approve each one before pasting the next.** That pause is the entire exercise.

**Step 1 — Recital of facts only:**

```text
Read inputs/case-brief.md and inputs/firm-style-guide.md.

Produce only Section 1: Recital of facts. Follow the style guide's rules
for this section (numbered, one fact per paragraph, no legal
characterization). Do not write any other section yet.

Save to outputs/letter-B-step1-facts.md. Pause for my review.
```

Read it. Are the facts numbered? Is there any legal characterization sneaking in ("SVC materially breached…")? Fix it before continuing.

**Step 2 — Legal theory only:**

```text
Read outputs/letter-B-step1-facts.md and inputs/firm-style-guide.md.

Produce only Section 2: Legal theory. Cite specific Agreement sections
by number (the brief lists them). Tie each theory back to a fact
paragraph from Step 1.

Append to outputs/letter-B-step2-theory.md. Do not rewrite the facts.
Pause for my review.
```

Read it. Does it cite Section 9.2 and 11.4 by number? Does each theory point at a fact paragraph?

**Step 3 — The demand:**

```text
Read outputs/letter-B-step2-theory.md, inputs/case-brief.md, and
inputs/firm-style-guide.md.

Produce only Section 3: The demand. Use a numbered list. Every dollar
figure must tie to a fact paragraph. Comply with the "What never goes
in a demand letter" rules — do not include the client's settlement floor
or the undocumented operational damages estimate.

Append to outputs/letter-B-step3-demand.md. Pause for my review.
```

Read it carefully. Did it leak the settlement floor ($75,000 walkaway, $150,000 minimum acceptable)? Did it use the undocumented "$80,000-$120,000" operational losses figure? Either is a serious style-guide breach.

**Step 4 — Deadline and final assembly:**

```text
Read outputs/letter-B-step3-demand.md and inputs/firm-style-guide.md.

Add Section 4: Deadline and consequence. Use a specific date fourteen
calendar days from today's date. Then assemble the full letter
(Sections 1-4 in order, plus standard heading and signature block)
and save the complete final version to outputs/letter-B-final.md.

Do not rewrite earlier sections — concatenate them.
```

---

## What success looks like

Score Run B (the decomposed flow) against these criteria, then check whether Run A also passes. Most teams find Run A fails **at least one** of these, often without anyone noticing.

- [ ] **Sections appear in the exact order required by the style guide:** Facts → Legal theory → Demand → Deadline and consequence. Out-of-order or merged sections = style-guide miss.
- [ ] **The recital of facts is numbered and free of legal characterization.** Grep the facts section for "breach", "violation", "wrongful". Those words belong in the legal-theory section, not the facts.
- [ ] **Agreement sections are cited by number** (specifically Section 9.2 and Section 11.4 from the brief). A demand letter that gestures at "the contract" without naming clauses is unleveraged.
- [ ] **The settlement floor is not disclosed.** The brief says Acme would walk into litigation only below $75,000 and would accept $150,000-plus. **Neither figure may appear in the letter.** The demand should be higher than the floor; the floor itself stays in the brief.
- [ ] **The undocumented operational damages estimate ($80,000-$120,000) is not in the letter.** The style guide explicitly bans it ("internal-only damages estimates that have not been documented"). Only the $153,000 paid and the $41,000 in cover damages are litigation-ready.
- [ ] **No banned phrases.** Grep: `grep -iE "it has come to our attention|approximately|in the region of|around \\\$" outputs/letter-B-final.md` should return nothing.
- [ ] **The deadline is a specific calendar date** (long form, fourteen days out), not "two weeks from today".

### Where Run A typically fails

Across many test runs against multiple assistants, the big-prompt version (Run A) commonly:

- merges fact and legal-characterization language in section 1 ("SVC breached its obligation to deliver Phase 2 on time"),
- omits the specific Agreement section numbers and gestures at "the contract" generically,
- **leaks the settlement floor or the operational damages estimate** because the agent treats the whole brief as fair game,
- uses banned hedges like "approximately $153,000",
- and gets the deadline wrong ("within two weeks" instead of a long-form date).

Each of those failures **could have been caught at a step boundary** in Run B. That is the entire point of P4. The big prompt does not let you intervene; the decomposed flow gives you four cheap correction points.

---

## Why this exercise

In the crash course (Principle 4), the canonical line is: "Big atomic changes take longer to debug, are harder to review, and make the failure mode 'throw away an hour' instead of 'throw away five minutes.'" The settlement-letter case is the example used directly in the chapter. This pack lets you run it end-to-end against any AI assistant in under fifteen minutes, and feel which version produces the deliverable you would actually be willing to send.

When you are ready, repeat this on a deliverable from your own work: a board memo, a release plan, a hiring rubric, a code review summary. The point is not the letter. The point is that one big prompt is one big undo, and four small prompts are four small undos.
