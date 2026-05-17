# Download URL Pattern

Lesson links in `problem-solving-crash-course.md` should use the **`/releases/latest/download/`** pattern so they always resolve to the most recent release. Do not hardcode a version tag.

## Canonical URLs

| Pack                       | Serves           | URL to use in lesson                                                                                                  |
| -------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| Pack 1 — Cluttered folder  | Practice 1 (P1)  | `https://github.com/panaversity/problem-solving-practice-packs/releases/latest/download/pack-1-cluttered-folder.zip`  |
| Pack 2 — Structured output | Practice 2 (P2)  | `https://github.com/panaversity/problem-solving-practice-packs/releases/latest/download/pack-2-structured-output.zip` |
| Pack 3 — Decomposition     | Practice 4 (P4)  | `https://github.com/panaversity/problem-solving-practice-packs/releases/latest/download/pack-3-decomposition.zip`     |
| Pack 4 — Worked example    | Part 10 capstone | `https://github.com/panaversity/problem-solving-practice-packs/releases/latest/download/pack-4-worked-example.zip`    |
| Pack 5 — Verification      | Practice 3 (P3)  | `https://github.com/panaversity/problem-solving-practice-packs/releases/latest/download/pack-5-verification.zip`      |
| Pack 6 — Persistence       | Practice 5 (P5)  | `https://github.com/panaversity/problem-solving-practice-packs/releases/latest/download/pack-6-persistence.zip`       |

## Rules for lesson-writer

- **Always** use `/releases/latest/download/<asset>` — never `/releases/tag/v1.0.0/...` or `/blob/main/...`.
- Link text should name the pack and what it does, not the URL. Example:
  > Download [Pack 1 — Cluttered folder](https://github.com/panaversity/problem-solving-practice-packs/releases/latest/download/pack-1-cluttered-folder.zip) and unzip it before starting Practice 1.
- One pack per callout. Do not bundle multiple downloads into a single Practice callout.
- The repo browse URL (`https://github.com/panaversity/problem-solving-practice-packs`) is fine for "See the source" references, but the action link in a Practice callout should be a direct zip download.

## How the URL resolves

GitHub auto-redirects `/releases/latest/download/<filename>` to the newest release that has that asset. Once `v1.0.0` is tagged and CI publishes the four zips, all four URLs above will start working simultaneously. Until then they 404 — this is expected and is why T9 (tagging) is the final gate before T11 (link verification).
