# Pack 2 — Structured Output Templates

**Serves:** Practice 2 (P2) of the Problem-Solving Crash Course.

The goal of this pack is to feel — in your own work — how much the **format constraint** changes output quality before you change a word of the content request.

You will run the same task **twice** against the same input: once with a prose prompt, once with a structured template. Then compare.

---

## What this pack contains

```
02-structured-output/
├── README.md                                  (this file)
├── inputs/
│   └── discovery-call-2024-09-12.txt          ~750-word raw call notes
└── templates/
    └── discovery-summary-template.md          1-page structured template
```

- **`inputs/discovery-call-2024-09-12.txt`** is a realistic-but-fake set of unstructured discovery-call notes for a (made-up) logistics-company sales evaluation. It contains the kind of mess a real call note has: signal mixed with chitchat, partial info, half-quoted budgets, named and unnamed competitors, and a few "do not write this down" asides.
- **`templates/discovery-summary-template.md`** is the structured artifact you want at the end: fixed sections, required fields, explicit "if missing, write `NOT IN SOURCE`" rule, banned subjective language.

---

## Set up the exercise

1. Unzip `pack-2-structured-output.zip`.
2. Open the folder in your AI assistant. Confirm it can read `inputs/discovery-call-2024-09-12.txt` and `templates/discovery-summary-template.md`.

That is the entire setup.

---

## The exact prompts to paste

You will run **two prompts back-to-back**. Save both outputs so you can diff them.

### Run A — the prose prompt (the baseline)

Paste this verbatim:

```text
Read inputs/discovery-call-2024-09-12.txt. Write a one-page discovery
summary that captures the important points for our sales team.
Save it to outputs/summary-A-prose.md.
```

That is it. No template, no fields, no banned words. This is how most people prompt the first time.

### Run B — the structured prompt

Paste this verbatim:

```text
Read inputs/discovery-call-2024-09-12.txt and templates/discovery-summary-template.md.

Produce a discovery summary that fills the template exactly:

  - Use every section heading from the template, in the same order.
  - Fill every field. If a field is genuinely not in the source,
    write "NOT IN SOURCE" — never infer or invent.
  - For every entry in "Decision criteria" and "The trigger event",
    include a short source quote (under 15 words) supporting the entry.
  - No preamble, no closing remarks, no subjective adjectives.
  - Max one page.

Save the result to outputs/summary-B-structured.md.
```

Now diff the two files (`diff outputs/summary-A-prose.md outputs/summary-B-structured.md` or open them side by side).

---

## What success looks like

Score Run B against these criteria. Run A is just the contrast — most of these will fail in Run A and that is the point.

- [ ] **All sections from the template are present**, in the same order, with the same headings. Missing or renamed sections = template was not followed.
- [ ] **Every required field is filled.** Empty `Stakeholders` table rows or a missing `Decision date` mean the agent skipped fields. That is the failure mode P2 fixes.
- [ ] **`NOT IN SOURCE` appears at least once.** The source genuinely does not name Vendor A or the EU bank — the agent should mark those `NOT IN SOURCE` rather than fabricate names.
- [ ] **No invented facts.** Spot-check: did the agent give a name to Vendor A? Did it invent a specific dollar figure not in the source? Either is a fabrication.
- [ ] **Direct quotes appear under "The trigger event" and "Decision criteria"** — short, lifted from the source, and the source actually contains them. Grep the source: `grep -F "<quoted phrase>" inputs/discovery-call-2024-09-12.txt` should return a hit.
- [ ] **No subjective adjectives** ("exciting opportunity", "great fit", "promising"). The template banned them.
- [ ] **Stakeholders.Authority is one of the allowed values** (`economic buyer`, `technical buyer`, `user`, `blocker`, `champion`). Marcus is the economic buyer; Pranav is a blocker until convinced; Sarah is the champion. If the agent labels Sarah "user" or "decision maker" (not on the allowed list), it ignored the constraint.

### What to look at in Run A

Run A will almost always:

- merge things the template would have separated (budget mixed into a narrative paragraph instead of a single line),
- skip facts the template would have surfaced (the EU office, the SOC 2 requirement, the freight system),
- include adjectives ("strong opportunity", "great call"),
- and feel **harder to verify**: there is no row-by-row check you can do.

That contrast — Run A reads fine but is hard to verify; Run B is uglier but every claim is checkable — is the whole lesson of Principle 2.

---

## Why this exercise

In the crash course (Principle 2), the move from prose to structured artifact is described as: "give the agent a structured artifact to fill in, you remove the guessing. Output quality rises sharply; disagreements appear at the interface boundary rather than buried inside the output." This pack lets you feel that on a self-contained input, in five minutes, against any AI assistant.

When you are ready, repeat this with your own recurring deliverable — a board memo, a redline summary, an investor update — and write the template once. You will use it forever.
