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

**100 paper(s) · estimated spend $26.68** (eligibility $17.41 · extraction $9.26) · updated 2026-07-17

| id | source | status | eligible | confidence | duplicate_risk | needs_supplement | spec_version | first_seen | last_assessed | supp_attempts | supplement_fp | elig_model | elig_tok_in | elig_tok_out | extract_model | extract_tok_in | extract_tok_out | notes | est_$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PMID_10456963 | master | INELIGIBLE | False | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 21608 | 743 |  |  |  |  | 0.1266 |
| PMID_10470338 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 25725 | 844 |  |  |  |  | 0.1497 |
| PMID_10471565 | master | INELIGIBLE | False | medium | high | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 20225 | 1122 |  |  |  |  | 0.1292 |
| PMID_10558957 | master | INELIGIBLE | False | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 32818 | 814 |  |  |  |  | 0.1844 |
| PMID_10762551 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 40279 | 878 |  |  |  |  | 0.2233 |
| PMID_10813484 | master | INELIGIBLE | False | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 27592 | 1020 |  |  |  |  | 0.1635 |
| PMID_10950805 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 17735 | 825 | claude-opus-4-8 | 19965 | 2218 | 2 survey(s), 6 count rows | 0.2646 |
| PMID_11090624 | master | INELIGIBLE | False | high | high | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 67683 | 1169 |  |  |  |  | 0.3676 |
| PMID_11172152 | master | INELIGIBLE | False | medium | low | True | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 29675 | 1085 |  |  |  |  | 0.1755 |
| PMID_11294676 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 17124 | 743 | claude-opus-4-8 | 19267 | 1454 | 1 survey(s), 2 count rows | 0.2369 |
| PMID_11294677 | master | EXTRACTED | True | medium | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 18644 | 1014 | claude-opus-4-8 | 21074 | 2597 | 1 survey(s), 11 count rows | 0.2889 |
| PMID_11372041 | master | INELIGIBLE | False | medium | high | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 17564 | 1014 |  |  |  |  | 0.1132 |
| PMID_11679121 | master | EXTRACTED | True | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 27823 | 920 | claude-opus-4-8 | 30146 | 2131 | 1 survey(s), 6 count rows | 0.3661 |
| PMID_11679122 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 21976 | 967 | claude-opus-4-8 | 24354 | 4293 | 2 survey(s), 28 count rows | 0.3631 |
| PMID_11679123 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 22646 | 763 |  |  |  |  | 0.1323 |
| PMID_11807721 | master | INELIGIBLE | False | medium | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 38291 | 1269 |  |  |  |  | 0.2232 |
| PMID_11857052 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 16756 | 759 |  |  |  |  | 0.1028 |
| PMID_11865433 | master | EXTRACTED | True | medium | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 13534 | 910 | claude-opus-4-8 | 15847 | 2451 | 3 survey(s), 4 count rows | 0.2309 |
| PMID_11969121 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 60630 | 926 |  |  |  |  | 0.3263 |
| PMID_12142257 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 32708 | 727 |  |  |  |  | 0.1817 |
| PMID_12201581 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 23423 | 1077 |  |  |  |  | 0.1440 |
| PMID_12224572 | master | EXTRACTED | True | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 25229 | 1044 | claude-opus-4-8 | 27671 | 1442 | 1 survey(s), 2 count rows | 0.3266 |
| PMID_12351583 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 46997 | 833 |  |  |  |  | 0.2558 |
| PMID_12378426 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 59444 | 894 |  |  |  |  | 0.3196 |
| PMID_12447777 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 17696 | 895 | claude-opus-4-8 | 20003 | 2395 | 2 survey(s), 5 count rows | 0.2707 |
| PMID_12524354 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 48689 | 916 |  |  |  |  | 0.2663 |
| PMID_12884171 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 9782 | 797 |  |  |  |  | 0.0688 |
| PMID_14613965 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 26641 | 779 |  |  |  |  | 0.1527 |
| PMID_14622411 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 41431 | 834 |  |  |  |  | 0.2280 |
| PMID_14728622 | master | EXTRACTED | True | medium | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 27673 | 881 | claude-opus-4-8 | 29963 | 2283 | 1 survey(s), 5 count rows | 0.3673 |
| PMID_15031793 | master | EXTRACTION_FAILED | True | medium | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 25114 | 1047 | claude-opus-4-8 | 150653 | 14427 | STAVE_ERROR: study_id in counts_dataframe is not a valid identifier. It must: - consist only of English letters (upper or lower case), numbers (0-9), or undersc | 1.2657 |
| PMID_15117308 | master | INELIGIBLE | False | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 24363 | 922 |  |  |  |  | 0.1449 |
| PMID_15130119 | master | INELIGIBLE | False | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 50777 | 1366 |  |  |  |  | 0.2880 |
| PMID_15216481 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 31527 | 851 |  |  |  |  | 0.1789 |
| PMID_15272415 | master | EXTRACTED | True | medium | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 13810 | 851 | claude-opus-4-8 | 16072 | 2089 | 1 survey(s), 8 count rows | 0.2229 |
| PMID_15383440 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 27135 | 687 |  |  |  |  | 0.1528 |
| PMID_15499534 | master | INELIGIBLE | False | high | high | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 39558 | 1164 |  |  |  |  | 0.2269 |
| PMID_15679556 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 25874 | 801 | claude-opus-4-8 | 28077 | 1926 | 1 survey(s), 6 count rows | 0.3379 |
| PMID_15679557 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 31997 | 890 |  |  |  |  | 0.1822 |
| PMID_15686571 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 46917 | 827 |  |  |  |  | 0.2553 |
| PMID_15717281 | master | EXTRACTED | True | medium | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 17079 | 818 | claude-opus-4-8 | 19301 | 2051 | 1 survey(s), 5 count rows | 0.2536 |
| PMID_15814601 | master | EXTRACTED | True | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 16952 | 780 | claude-opus-4-8 | 19132 | 3198 | 4 survey(s), 12 count rows | 0.2799 |
| PMID_15941416 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 27736 | 911 | claude-opus-4-8 | 30055 | 2603 | 1 survey(s), 14 count rows | 0.3768 |
| PMID_16135198 | master | EXTRACTED | True | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 33602 | 958 | claude-opus-4-8 | 35976 | 2263 | 1 survey(s), 4 count rows | 0.4284 |
| PMID_16185238 | master | INELIGIBLE | False | medium | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 31151 | 1083 |  |  |  |  | 0.1828 |
| PMID_16186171 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 29153 | 877 | claude-opus-4-8 | 31428 | 1515 | 1 survey(s), 2 count rows | 0.3627 |
| PMID_16206082 | master | EXTRACTED | True | medium | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 28250 | 892 | claude-opus-4-8 | 30545 | 2186 | 2 survey(s), 4 count rows | 0.3709 |
| PMID_16235185 | master | EXTRACTED | True | medium | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 23417 | 1061 | claude-opus-4-8 | 25880 | 2070 | 1 survey(s), 5 count rows | 0.3248 |
| PMID_16319183 | master | INELIGIBLE | False | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 24904 | 1011 |  |  |  |  | 0.1498 |
| PMID_16359407 | master | INELIGIBLE | False | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 18017 | 852 |  |  |  |  | 0.1114 |
| PMID_16420747 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 40510 | 856 |  |  |  |  | 0.2239 |
| PMID_16518760 | master | EXTRACTED | True | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 33636 | 1043 | claude-opus-4-8 | 36082 | 10110 | 6 survey(s), 96 count rows | 0.6274 |
| PMID_16640612 | master | INELIGIBLE | False | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 36098 | 1158 |  |  |  |  | 0.2094 |
| PMID_16703518 | master | EXTRACTED | True | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 17836 | 945 | claude-opus-4-8 | 20186 | 3623 | 4 survey(s), 12 count rows | 0.3043 |
| PMID_16779725 | master | INELIGIBLE | False | high | medium | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 33714 | 1101 |  |  |  |  | 0.1961 |
| PMID_16845638 | master | INELIGIBLE | False | high | none | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 33146 | 897 |  |  |  |  | 0.1882 |
| PMID_17002724 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 37556 | 956 | claude-opus-4-8 | 39919 | 2330 | 1 survey(s), 9 count rows | 0.4695 |
| PMID_17093247 | master | EXTRACTED | True | high | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 29694 | 848 | claude-opus-4-8 | 31940 | 1285 | 1 survey(s), 1 count rows | 0.3615 |
| PMID_17158810 | master | INELIGIBLE | False | medium | low | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 20761 | 939 |  |  |  |  | 0.1273 |
| PMID_17176345 | master | INELIGIBLE | False | medium | high | False | 1 | 2026-07-02 | 2026-07-02 | 0 |  | claude-opus-4-8 | 20262 | 1066 |  |  |  |  | 0.1280 |
| … 40 more rows |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

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
