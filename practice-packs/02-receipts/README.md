# Pack 2 — Receipts

**Serves:** Principle 2 of the Problem-Solving Crash Course (_Code as Universal Interface_).

A folder of 15 fake-but-plausible receipts in three different formats:

```
receipts/
├── photos/         5 JPGs    — phone photos of paper receipts
├── pdfs/           5 PDFs    — email receipts
└── screenshots/    5 PNGs    — phone-app payment screenshots
```

All names, merchants, amounts, and confirmation numbers are synthetic. No real personal data.

Two purchases are planted **outliers** so "flag any unusually large purchases" has a clear correct answer when the agent walks through its approach:

- `pdfs/hotel-folio-marriott-2024-10-18.pdf` — **$384.40** (one-night hotel stay)
- `screenshots/transit-clipper-2024-10-25.png` — **$182.40** (Verizon phone bill)

The other 13 receipts cluster between roughly $11 and $99.

## What this pack is for

The Principle 2 hello-world asks the agent to walk through how it would extract dates, amounts, and categories from a mixed-format receipt folder, build a monthly summary by category, and flag outliers — and to name which of the **Five Powers** (precise thinking, workflow orchestration, organized memory, universal compatibility, instant tool creation) each step would use.

Only code can compose this workflow end to end: vision/OCR for the JPGs and PNGs, text extraction for the PDFs, normalization into a single table, aggregation into a monthly summary, threshold logic for outliers. No pre-built receipt app does this combination across these three input formats.

## How to use this pack

Open the lesson at `https://learn.panaversity.org/docs/problem-solving-crash-course#principle-2--code-as-universal-interface` and follow the **Hands-on: Hello world** in Principle 2. The lesson supplies the exact prompt.

## Regenerating the receipts

The receipts are produced by a deterministic Python script:

```
practice-packs/02-receipts/generate.py
```

Run it with `uv run generate.py` to recreate the contents from scratch. The script uses Pillow for the JPGs and PNGs, and reportlab for the PDFs. Inline PEP 723 metadata declares the dependencies.

## License

CC0 — the synthetic receipts in this folder are released into the public domain.
