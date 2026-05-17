# Pack 6 — Hiring Loop Persistence

**Serves:** Practice 5 (P5) of the Problem-Solving Crash Course.

The goal of this pack is to **feel the difference between volatile chat context and durable file context**. You'll run the same screening task twice — once on a fresh folder, once after you and the agent draft a `CLAUDE.md` for it together — and see what the rules file actually buys you.

---

## What this pack contains

```
06-persistence/
├── README.md                          (this file)
├── hiring-loop/                       The recurring-work folder
│   ├── job-spec.md                    Senior PM, Growth team — 1 page
│   ├── weighting.md                   How to weight preferred qualifications
│   ├── inbound/                       Five candidate résumés as .md
│   ├── shortlist/                     Empty — where advances would go
│   └── scorecards/                    Empty — where panel scorecards would go
└── reference/
    └── example-CLAUDE.md              A reference rules file — DO NOT OPEN until after Run B
```

You are the hiring manager for a Senior Product Manager role on the Growth team. Five candidates' résumés are sitting in `inbound/`. There is **no `CLAUDE.md` in `hiring-loop/`** — and that is the point of the exercise. You will generate one together with the agent partway through.

> **Don't peek at `reference/example-CLAUDE.md` yet.** It's only useful as a comparison *after* you've made your own attempt. Looking at it first defeats the exercise.

---

## Set up the exercise

1. Unzip `pack-6-persistence.zip` into a fresh folder.
2. Open the **`hiring-loop/`** subfolder in your AI assistant of choice. Open `hiring-loop/` specifically — not the outer folder — so the agent's working directory is the hiring loop itself. That is how `CLAUDE.md` auto-loading works in Claude Code and Cowork.
3. Make sure the assistant has both read AND write access inside `hiring-loop/`.

No installs, no accounts.

---

## Run A — naive screening (no rules file)

This is the baseline. The agent has no special context.

**Prompt to paste:**

```text
Read every résumé in inbound/. For each candidate, produce a short
recommendation: ADVANCE, HOLD, or DECLINE, with a one-sentence rationale.
Save the result to inbound-screen-runA.md.
```

That's it. Don't restate any rules. Don't tell the agent about the job spec. Let it do what it would do on a cold start.

When it's done, read `inbound-screen-runA.md`. Note in your head: which candidates did it advance, hold, decline?

---

## Run B — draft the rules file, then re-screen

### Step 1 — let the agent draft `CLAUDE.md`

**Prompt to paste:**

```text
Read this folder and propose a CLAUDE.md under 250 words: what this is,
where things live, conventions a hiring manager would normally state
manually, and three to five critical rules — things that are expensive
or embarrassing to get wrong. Pay particular attention to required vs.
preferred qualifications, credential verification, and privacy.

Save your proposal as CLAUDE.md at the root of this folder. After
saving, summarize what you put in it in two bullets.
```

> **Naming note:** if you are using OpenCode or OpenWork, save the file as `AGENTS.md` instead. OpenCode also reads `CLAUDE.md` as a fallback; OpenWork does not. The contents are the same either way.

### Step 2 — edit the rules file minimally

Read what the agent wrote. Spend two minutes — no more — editing it. Tighten any rule that's vague. Cut anything redundant. Save.

The goal is *not* to write a perfect rules file. It's to get one good enough to test in Run B.

### Step 3 — re-run the screening

Start a fresh session if your tool supports it. If it doesn't, begin with "Forget everything we discussed earlier."

**Prompt to paste:**

```text
Read every résumé in inbound/. Produce the same per-candidate
recommendation (ADVANCE / HOLD / DECLINE with one-sentence rationale).
Save as inbound-screen-runB.md.
```

Notice: **the prompt is identical to Run A.** No restated rules. The whole point is that the agent picks the rules up from `CLAUDE.md` on its own.

---

## Diff the two runs

In your terminal, or by opening both files side by side:

```text
diff inbound-screen-runA.md inbound-screen-runB.md
```

That diff *is* the lesson. The persistence you got from the rules file is exactly what changed between the two screens.

---

## What success looks like

Score Run B and the diff:

- [ ] **`CLAUDE.md` exists at the root of `hiring-loop/`.** If there's no file, the exercise didn't happen.
- [ ] **It is under 250 words.** The lesson's "table of contents, not encyclopedia" rule. A 2,000-word rules file is the failure mode P5 warns about.
- [ ] **It contains at least one rule about credential verification** — anything that names a flag-and-don't-auto-advance behavior for credential discrepancies.
- [ ] **It contains at least one rule about required vs. preferred qualifications** — anything that names "required gap = hard fail."
- [ ] **In Run B, Carlos has flipped to HOLD with a credential-flag rationale.** This is the single most important success signal. Carlos's résumé claims an MBA from a school that didn't exist yet on the date he claims to have graduated. In Run A, most agents miss this and advance him on the strength of the rest of the résumé. In Run B, the credential rule fires.
- [ ] **In Run B, Amelia and Evan are unchanged from Run A** (Amelia ADVANCE, Evan DECLINE). The rules file shouldn't disturb obvious cases.
- [ ] **The diff between Run A and Run B is non-trivial** — at minimum, rationales got more specific (cite "required qual: 3+ yrs B2B SaaS" instead of "lacks experience"). If the two runs are identical, the agent never opened `CLAUDE.md`.

### Stretch (gold-star)

After you've scored Run B, open `reference/example-CLAUDE.md` and compare it to your own draft. Ask yourself: **was there anything the reference file had that yours didn't?** That gap is the next revision of *your* rules file.

This is exactly the closing move from the lesson: each session reveals the next thing the rules file should have known.

### Where this fails

- **Agent ignored `CLAUDE.md` in Run B (output identical to Run A).** Usually this means the tool didn't auto-load the file. In Claude Code and Cowork, `CLAUDE.md` is auto-loaded only when the folder is opened as a workspace. Re-prompt: _"Before screening, read `CLAUDE.md` at the root of this folder and confirm what rules you'll apply."_ Same payoff, less elegant.
- **`CLAUDE.md` is 1,200 words and contains the full job spec inline.** The agent treated it as documentation, not table of contents. Re-prompt: _"Cut this rules file to under 250 words. Inline only the rules themselves. Reference `job-spec.md` and `weighting.md` instead of pasting them."_
- **Carlos advances in Run B anyway.** Either your rules file didn't include the credential-flag rule, or the agent didn't read the date discrepancy carefully. Open `inbound/candidate-carlos-mendoza.md` and confirm the date issue is still visible (it should be — MBA 2018 from a school founded 2019). If it is, the credential rule needs to be more explicit in your `CLAUDE.md`.

---

## Why this exercise

In the crash course (Practice 5), the rules-file vignette is the answer to "why does the agent forget what we decided yesterday?" This pack lets you run it end to end on a realistic recurring-work folder — a hiring loop — without first having to clean up a folder of your own. The skill you are training (writing a tight rules file that captures the conventions and critical rules a particular folder lives by) transfers directly to any matter folder, reporting folder, or operations runbook you already maintain.

When you are done, repeat this on a real folder of yours. The first `CLAUDE.md` you write for it will be wrong in interesting ways. That is the point.

---

## Optional engineering extension

For readers who want the engineering version:

> Spin up a free Neon project (~60 seconds), ask the agent to design the smallest schema for a personal budget tracker, run it, then add three lines about Neon to your project's `CLAUDE.md` (connection string, the migrations directory, the rule that schema changes go through a migration file, never a direct `psql` session). Any future session inherits that database context automatically — same persistence pattern, different domain.

We don't ship the Neon flow because it requires account creation. Just point at it when you're ready.
