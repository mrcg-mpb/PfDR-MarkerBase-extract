# PfDR MarkerBase — extraction pipeline

Automated triage of papers for a database of *P. falciparum* drug-resistance
marker frequencies. PDFs land in a Google Drive folder; this repo watches that
folder, judges each paper for eligibility, and tracks where every paper is in
the pipeline — all via GitHub Actions, with a weekly digest of anything that
needs a human.

## The flow

```
Drive inbox (PDFs)
      │   process.yml — every 4h, silent
      ▼
  GATE 1: on exclude.txt?  ── yes ─► EXCLUDED            (terminal)
      │ no
      ▼
  GATE 2: eligibility agent (markerbase.py)
      ├─ not eligible ─────────────► INELIGIBLE          (terminal, the majority)
      ├─ high duplicate risk ──────► REVIEW_DUPLICATE     (you rule in decisions.yaml)
      ├─ data in missing supplement ► AWAIT_SUPPLEMENT    (you upload to Drive)
      └─ clean ────────────────────► ELIGIBLE            (ready for extraction, stage 2)

digest.yml — Friday 06:00 UTC ─► one GitHub issue listing everything outstanding
```

## Files you edit (in the GitHub web UI)

| File | What it's for |
|---|---|
| [`exclude.txt`](exclude.txt) | Papers to skip entirely. One filename per line. |
| [`decisions.yaml`](decisions.yaml) | Your `duplicate` / `unique` ruling on flagged papers. |

## Files the bot owns (you only read)

| File | What it is |
|---|---|
| `roster.csv` | One row per paper: its current status + light metadata. The source of truth. |

## Code

| File | Role |
|---|---|
| [`pipeline.py`](pipeline.py) | The processing driver (run by `process.yml`). |
| [`digest.py`](digest.py) | The weekly digest (run by `digest.yml`). |
| [`markerbase.py`](markerbase.py) | Eligibility spec + the structured assessment call. |
| [`drive.py`](drive.py) | Google Drive access (list / fetch / supplements). |
| [`store.py`](store.py) | Reads/writes the roster, exclude list, and decisions. |

## Secrets (repo settings → Secrets and variables → Actions)

| Secret | Used for |
|---|---|
| `DRIVE_SA_KEY` | Drive service-account JSON key (full file contents). |
| `DRIVE_FOLDER_ID` | Top `papers` folder (walked recursively — see below). |
| `DRIVE_SUPPLEMENT_FOLDER_ID` | Top supplements folder, same tree shape (optional). |
| `ANTHROPIC_API_KEY` | The eligibility assessment (billed per new paper). |

`GITHUB_TOKEN` is provided automatically — no setup needed for the digest.

## Drive layout & contributor access

```
papers/                ← shared with the SERVICE ACCOUNT (Viewer)
├── master/            ←   your own PDFs (incl. institutional-access ones)
│     └── 111.pdf
├── alice/             ← shared with alice only (Editor) — she sees ONLY this
│     └── 222.pdf
└── bob/               ← shared with bob only (Editor)
      └── 333.pdf
```

The pipeline **walks** this tree read-only (it never moves files) and tags each
PDF with its source folder (the `source` column in the roster). Contributors
only ever see their own folder, so institutional PDFs in `master/` stay private.
The supplements folder mirrors this shape, with a `<paper-id>/` folder inside any
contributor's subfolder. Adding a contributor = create + share their subfolder;
no secret or code change needed.

See [NOTES.md](NOTES.md) for how the Drive access works and the design rationale.

## Running locally

```bash
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS=~/.secrets/pfdr-markerbase-key.json
export DRIVE_FOLDER_ID=...            # and DRIVE_SUPPLEMENT_FOLDER_ID if used
export ANTHROPIC_API_KEY=sk-ant-...
python pipeline.py
```
