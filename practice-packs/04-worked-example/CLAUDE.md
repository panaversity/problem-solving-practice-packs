# CLAUDE.md — Vendor MSA review workspace

## What this folder is

A vendor master services agreement review workspace. The inbound vendor draft lives in `inbound/`. The firm's redline standard is `redline-standard.md`. Your deliverables go in the working directory at each phase.

## Conventions

- One file per phase. Phase outputs are: `vendor-msa-explore.md`, `msa-plan.md`, then numbered `step1.md`, `step2.md`, …, then `vendor-msa-final.md`.
- Save files. Do not produce final analysis only in chat.
- Cite clauses by their MSA section number (for example, "Section 7.1") and the redline-standard section number (for example, "Standard §6"). Side-by-side citation is how reviewers verify your work.
- Severity labels are exactly three values: `HIGH`, `MED`, `LOW`. Anything else is ignored downstream.

## Three rules that are expensive to get wrong

1. **Never silently accept a vendor-favorable deviation.** If the MSA deviates from the redline standard in a way that hurts Customer, it must be flagged with severity, even if the deviation looks "small". Small clauses compound across vendors.
2. **Quote the source.** Every flagged deviation must include the exact MSA text (in quotes) and the redline-standard text (in quotes). No paraphrasing — a paraphrase is a place where a problem can hide.
3. **Severity discipline.** `HIGH` = unilateral risk shifted to Customer, or violates a firm policy. `MED` = adverse but negotiable. `LOW` = stylistic or minor. Inflating severity destroys the signal for the next reviewer.
