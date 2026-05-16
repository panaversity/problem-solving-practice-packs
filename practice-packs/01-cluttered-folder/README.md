# Pack 1 — Cluttered Downloads Folder

**Serves:** Practice 1 (P1) of the Problem-Solving Crash Course.

The goal of this pack is to practice **staying out of the agent's way**: describe the problem, name the artifact you want, and let the agent pick the commands.

---

## What this pack contains

```
01-cluttered-folder/
├── README.md         (this file)
├── SIZES.txt         (realistic file sizes — see note below)
└── downloads/        53 stub files mimicking a real Downloads folder
```

The `downloads/` directory holds **53 empty stub files** named after the kind of clutter that accumulates in a real Downloads folder over a year: invoices (with duplicates and "-final" siblings), bank statements, MSAs, ebooks, installers, screenshots, photos, draft documents, and random scratch files.

The files are empty so the zip stays small. `SIZES.txt` lists the **plausible size** each file would have in a real folder (for example, `GoogleChrome.dmg = 225M`). If the agent's organization recommendation depends on file size, paste the relevant rows from `SIZES.txt` into the chat when the agent asks. That is the realistic signal the agent would have read from `ls -lah` on your real machine.

You do not need to edit `SIZES.txt`. Treat it as a stand-in for what `ls -lah` would have reported.

---

## Set up the exercise

1. Unzip `pack-1-cluttered-folder.zip` into a fresh folder somewhere on your machine.
2. Open that folder in your AI assistant of choice (Claude Code, OpenCode, Cowork, OpenWork — anything with file access).
3. Make sure the assistant has read access to the `downloads/` subfolder.

That is the entire setup. No installs, no accounts.

---

## The exact prompt to paste

Paste this verbatim into your assistant. Do **not** suggest commands. The whole point of P1 is that the agent picks the commands.

```text
I have a cluttered Downloads folder at ./downloads/. Don't move, rename,
or delete anything yet.

Inspect the folder and produce a single file called ORGANIZATION-PLAN.md
in the current directory containing:

  1. A one-paragraph summary of what's in there (rough file counts by
     kind, total size estimate).
  2. A table of duplicate or near-duplicate file groups (e.g., the same
     invoice with "(1)" or "-final" siblings, multiple versions of the
     same archive). One row per group.
  3. A proposed folder structure (4-7 top-level folders, no deeper than
     one nesting) with a one-line rationale for each folder.
  4. A "Questions before I move anything" list — up to 5 things you'd
     want me to clarify before you'd feel safe actually reorganizing.

Constraints:
  - Read-only. No file moves, copies, or deletes.
  - If you need file sizes, ask me and I will paste them from SIZES.txt.
  - Output must be a saved file (ORGANIZATION-PLAN.md), not just chat.
```

---

## What success looks like

A good run produces a saved `ORGANIZATION-PLAN.md` with **all four sections**. Score yourself on these:

- [ ] The agent **read the folder first** before proposing anything. You can see the read step in the execution view, not just inferred categories.
- [ ] **It did not move any files.** `downloads/` is byte-identical to how it started. Run `ls downloads/ | wc -l` and you should still get 53.
- [ ] The duplicate table catches at least **3 of these obvious groups**: the three `invoice-globex-march*` files, the two `Sample_Vendor_MSA_v2*` files, the two `design-assets-final*.zip` files, the three `Q4-roadmap-DRAFT*.docx` files, the two `profile-photo*` files, the two `Untitled*` text files.
- [ ] The proposed structure is **outcome-oriented** ("Receipts/", "Installers/", "Screenshots/"), not just file-extension-oriented ("PDFs/", "ZIPs/"). Extension-only buckets are a mild fail: it means the agent leaned on `find -name '*.pdf'` instead of reading the names.
- [ ] The questions list contains at least one **judgment call you genuinely cannot answer from the folder alone** (for example, "Should signed contracts be kept indefinitely or archived after a year?", "Which of the three roadmap drafts is canonical?").

### Where this fails

- **Agent narrates instead of acting** ("I would `ls -lah` and then categorize…"): that is the classic P1 failure. Tell it again: _"Don't describe what you would do. Read the folder and save the file."_
- **Agent produces a beautiful schema in chat with no saved file**: P1 fail. The artifact must land on disk.
- **Agent moves files anyway**: re-read your prompt; it said read-only. If the prompt was clear, that is a permission/scoping problem, which is Principle 6 territory.

---

## Why this exercise

In the crash course (Principle 1), the Downloads-folder vignette is the canonical illustration of "use the action surface; let the agent pick the command." This pack lets you run that vignette **without polluting your real Downloads folder** and without trusting the agent to be reversible. The folder is fake, so the worst case is harmless. The skill you are training, describing an outcome instead of dictating commands, is real.

When you are ready, repeat this on your **actual** Downloads folder. By then you will know what a good plan looks like before you give the agent write access.
