# PfDR MarkerBase — extraction pipeline

A self-running pipeline that triages papers for a database of *P. falciparum*
drug-resistance marker frequencies. PDFs are dropped into a Google Drive folder;
the pipeline reads each one, judges whether it's eligible for data extraction,
and keeps a running record of where every paper stands — checking in with a
human only when it genuinely needs a decision.

## Status

![pipeline status](docs/stats.svg)

<sub>Updates automatically on every run.</sub>

## Roster

<!-- ROSTER:START -->

**7 paper(s) · estimated spend $0.28** (eligibility $0.20 · extraction $0.08) · updated 2026-07-01

| id | source | status | eligible | confidence | duplicate_risk | needs_supplement | spec_version | first_seen | last_assessed | supp_attempts | supplement_fp | elig_model | elig_tok_in | elig_tok_out | extract_model | extract_tok_in | extract_tok_out | notes | est_$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PMID_30898164 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-01 | 2026-07-01 | 0 |  | claude-haiku-4-5 | 42445 | 1265 | claude-haiku-4-5 | 45175 | 7208 | 4 survey(s), 34 count rows | 0.1300 |
| PMID_38461239 | master | EXCLUDED |  |  |  |  |  | 2026-07-01 |  |  |  |  |  |  |  |  |  | on exclude.txt | 0.0000 |
| PMID_38594679 | master | INELIGIBLE | False | high | low | True | 1 | 2026-07-01 | 2026-07-01 | 0 |  | claude-haiku-4-5 | 36430 | 1379 |  |  |  |  | 0.0433 |
| PMID_40666313 | master | EXCLUDED |  |  |  |  |  | 2026-07-01 |  |  |  |  |  |  |  |  |  | on exclude.txt | 0.0000 |
| PMID_41379859 | master | EXTRACTION_FAILED | True | high | none | False | 1 | 2026-07-01 | 2026-07-01 | 0 |  | claude-haiku-4-5 | 58500 | 1742 | claude-haiku-4-5 | 0 | 0 | STAVE: extractor error: 1 validation error for Extraction   Invalid JSON: EOF while parsing a string at line 1 column 20832 [type=json_invalid, input_value='{"study": | 0.0672 |
| PMID_9236824 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-01 | 2026-07-01 | 0 |  | claude-haiku-4-5 | 12470 | 1130 |  |  |  |  | 0.0181 |
| PMID_9391510 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-01 | 2026-07-01 | 0 |  | claude-haiku-4-5 | 17483 | 1009 |  |  |  |  | 0.0225 |

_The table above is a static snapshot. For a searchable, filterable view (paginated for large sets), open [`data/roster.csv`](data/roster.csv) — GitHub renders CSV files as an interactive table._

<!-- ROSTER:END -->

## How it works

The pipeline runs in two stages.

**Stage 1 — eligibility** (every few hours, automatic). For each new PDF it:

1. **Skips** anything you've told it to ignore.
2. **Assesses** the rest against a clear eligibility spec (right parasite, target
   markers with extractable frequencies, sub-country location, ≤3-year window).
3. **Sorts** each into an outcome: *eligible* (ready for stage 2), *ineligible*
   (the majority), or **flagged** — needs a human because it might duplicate an
   existing study, or its data lives in supplementary files still to be uploaded.

**Stage 2 — extraction** (on demand). For eligible papers, an agent pulls the
marker data into the **STAVE** schema (study / survey / counts) and the real
STAVE R package validates it — anything malformed is sent back to the agent to
fix. Output lands in `data/extracted/<id>/`.

Nothing is ever looked at twice, and every paper's state is tracked in one file.
Once a week (Friday morning) you get a single GitHub issue summarising anything
waiting on you.

## What you need to do

The pipeline runs itself — you rarely touch anything. There are only **two
files** you ever edit, both directly in the GitHub web editor:

- **`data/exclude.txt`** — add a paper's filename here to skip it entirely.
- **`data/duplicate_decisions.yaml`** — when a paper is flagged as a possible
  duplicate, add one line ruling it `duplicate` or `unique`.

(The target markers to extract live in `config/target_loci.csv` — a reference
list you update when the marker set changes, not per-paper.)

That's it. The weekly issue tells you when either is needed (and when to upload a
paper's supplementary files to Drive). You never edit the code or the records the
pipeline keeps.

## More detail

Design rationale, the full file/secret reference, and how the Google Drive access
and contributor sharing work all live in **[docs/NOTES.md](docs/NOTES.md)**.
