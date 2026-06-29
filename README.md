# PfDR MarkerBase — extraction pipeline

A self-running pipeline that triages papers for a database of *P. falciparum*
drug-resistance marker frequencies. PDFs are dropped into a Google Drive folder;
the pipeline reads each one, judges whether it's eligible for data extraction,
and keeps a running record of where every paper stands — checking in with a
human only when it genuinely needs a decision.

## Status

![pipeline status](docs/stats.svg)

<sub>Updates automatically on every run.</sub>

## How it works

Every few hours, the pipeline looks for new PDFs in the Drive folder. For each
new paper it:

1. **Skips** anything you've told it to ignore.
2. **Assesses** the rest with an AI model against a clear eligibility spec.
3. **Sorts** each into an outcome: *eligible* (passed, ready for the next stage),
   *ineligible* (the majority), or **flagged** — needs a human because it might
   duplicate an existing study, or its data lives in supplementary files that
   still need uploading.

Nothing is ever looked at twice, and every paper's current state is tracked in
one file. Once a week (Friday morning) you get a single GitHub issue summarising
anything waiting on you.

## What you need to do

The pipeline runs itself — you rarely touch anything. There are only **two
files** you ever edit, both directly in the GitHub web editor:

- **`data/exclude.txt`** — add a paper's filename here to skip it entirely.
- **`data/decisions.yaml`** — when a paper is flagged as a possible duplicate,
  add one line ruling it `duplicate` or `unique`.

That's it. The weekly issue tells you when either is needed (and when to upload a
paper's supplementary files to Drive). You never edit the code or the records the
pipeline keeps.

## More detail

Design rationale, the full file/secret reference, and how the Google Drive access
and contributor sharing work all live in **[docs/NOTES.md](docs/NOTES.md)**.
