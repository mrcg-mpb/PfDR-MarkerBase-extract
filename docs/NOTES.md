# MarkerBase pipeline — notes

## How the Google Drive access works

There are **two separate worlds**, linked by one deliberate act:

- **Google Cloud** — where *automation* lives (the robot identity + its credentials).
- **Google Drive** — where the *data* (PDFs) lives.

The Cloud project does **not** contain your Drive. They are connected **only** by
**sharing a folder** with the robot's email. Without that share, the robot is a
valid identity that can see none of your files.

### The elements

| Element | What it is | Analogy |
|---|---|---|
| Google account (`<project-account>@gmail.com`) | A *human* login that owns things | You, the person |
| Cloud project (`<your-project>`) | Container for APIs + identities you create | A company you registered |
| Drive API (enabled) | Switch allowing the project to talk to Drive | Permission to do Drive work at all |
| Service account (`markerbase-reader`) | A *non-human* robot identity scripts log in as | A robot employee you hired |
| Service-account email | The robot's address; how Drive grants it access | The name on the room's access list |
| JSON key file | The robot's credential ("this script IS that robot") | The employee's keycard |
| Scope (`drive.readonly`) | What the robot may do — read only | A read-only badge |
| Drive folder (`inbox_test`) | A normal folder holding the PDFs | A room you own |
| The share (folder → robot, Viewer) | Adds the robot to that folder's access list | Putting the robot on the entry list |

### How they nest

```
YOUR GOOGLE ACCOUNT  (a human login)
│
├── GOOGLE CLOUD
│     └── Project: <your-project>
│           ├── Drive API: ENABLED
│           └── Service account: markerbase-reader
│                 ├── email:  markerbase-reader@<your-project>.iam.gserviceaccount.com  ← its "name"
│                 └── JSON key (downloaded)          ← its "password"
│
└── GOOGLE DRIVE
      └── Folder: <inbox folder>
            ├── example.pdf
            └── Shared with → markerbase-reader@…  (Viewer)   ← THE LINK
```

(The project and the Drive can even live on different Google accounts — they're
only ever linked by the share. The real project ID, service-account email, and
folder ID are kept out of this public repo — they live in your local env vars
and GitHub secrets.)

### The key idea: identity vs. access

Two separate questions, both must be true:

- **Authentication — "who is making this request?"** → answered by the **JSON key**.
- **Authorization — "is that identity allowed to see this folder?"** → answered by the **share**.

The key proves *who*; the share grants *what*. Neither alone is enough.

### Runtime flow (what a Drive script does)

1. Read `GOOGLE_APPLICATION_CREDENTIALS` → find the JSON key.
2. Use the key to prove "I am `markerbase-reader`" → get a short-lived token. *(auth)*
3. Ask the Drive API to list/read files in folder X.
4. Drive checks the share: is `markerbase-reader` allowed? Yes, Viewer, read-only. *(authz)*
5. Drive returns the file. No browser login, no personal password used.

### Why this structure

- Your personal Google login is never in the code.
- Least privilege: the robot can only *read*, only the folders you *shared*.
- Small blast radius: a leaked key = read access to one folder; delete/rotate the
  key in the Cloud console without touching your account.

## The two credentials in the pipeline

The full pipeline talks to two external services, each with its own credential:

| Credential | Env var | Used for | Billed to |
|---|---|---|---|
| Google service-account key | `GOOGLE_APPLICATION_CREDENTIALS` | *Fetching* papers from Drive | Free (Drive API) |
| Anthropic API key | `ANTHROPIC_API_KEY` | *Assessing* papers | API credit |

A terminal running the whole flow needs **both** set. They're independent
accounts, credentials, and bills.

## The pipeline structure

Two scheduled GitHub Actions, decoupled so day-to-day processing never pings you:

- **`process.yml`** (every 4h, silent) — discovers new PDFs, runs the two gates,
  assesses eligible-stage papers, and updates `roster.csv`. Capped at 100
  assessments per run so a sudden dump of PDFs can't run up an unbounded bill;
  the rest are picked up on later runs. Cadence is 4h rather than 30 min only to
  be frugal with Actions minutes — the API cost is driven by *new* papers, not by
  how often we poll, so empty runs are nearly free.
- **`digest.yml`** (Friday 06:00 UTC) — reads the roster and maintains one
  GitHub issue listing everything outstanding. Because it reads *current roster
  state*, the digest is the complete standing queue, not "what changed this week".

### State, not stages-as-files

`roster.csv` is a single state machine: every paper has exactly one row and one
`status`. We deliberately avoided per-stage files (a paper would have to be moved
between them atomically, and bot+human edits would collide). The terminal states
(`EXCLUDED`, `INELIGIBLE`, `DUPLICATE`) are the "don't look again" guarantee —
discovery only assesses filenames not already in the roster.

### Who edits what (the no-shared-files rule)

The bot owns `roster.csv`; you own `exclude.txt` and `decisions.yaml`. No file is
written by both, which is what keeps the bot's pushes from clobbering your edits.
Your edits are line-based text (plain lines / flat YAML), never CSV — so opening
them can't mangle an all-digit PubMed-ID key (Excel turns `12345678` into
`1.23E+07`). The roster *is* CSV, but only the bot writes it and you only view it
(GitHub renders CSV as a table), so Excel never touches it.

### The two human-in-the-loop flags

- **Duplicate risk** needs your judgment and can't be auto-detected. The agent
  flags `REVIEW_DUPLICATE`; you resolve by adding `id: duplicate` / `id: unique`
  to `decisions.yaml`; the next run routes accordingly.
- **Missing supplement** resolves itself. The agent flags `AWAIT_SUPPLEMENT`; you
  upload files to Drive under a `<id>/` folder (one per paper, keyed by the PDF's
  name) beneath the supplement root; the next eligibility run re-assesses *with*
  the supplement included. It re-checks whenever the folder's **contents change**
  (a content fingerprint is stored in `supplement_fp`), so a corrected re-upload
  gets another chance while an unchanged folder never re-bills. `src/supplements.py`
  converts the files for the model: PDFs pass through natively; **spreadsheets
  (xlsx/xls), CSV/TSV/text, and Word (docx/doc)** are converted to text. Legacy
  `.doc` uses LibreOffice (preinstalled on the runner); unsupported types are
  skipped with a note. If a supplement IS examined but still doesn't contain the
  needed data, the paper is flagged `SUPPLEMENT_INSUFFICIENT` — distinct from
  `AWAIT_SUPPLEMENT` (nothing uploaded yet) so you can tell "waiting on you" from
  "what you gave us wasn't enough". Both re-check when the folder contents change.

### Spec versioning

`markerbase.SPEC_VERSION` is stamped on every assessed row. Bump it when the
eligibility spec changes; rows then show which spec judged them. (Re-assessing
old papers under a new spec is a deliberate manual action — not automatic, so a
spec tweak can't silently re-bill the whole back-catalogue.)

### What's NOT built yet

`ELIGIBLE` is the current finish line — the **extraction stage (stage 2)** that
pulls the actual marker frequencies is the next thing to design. The roster
already has a slot for it.

## A note on committed paper text

The repo is **public** on purpose, for transparency of the code. `roster.csv` is
lightweight — status + a few booleans, no paper text at all. The reasoning
(per-criterion evidence quotes, exclusion reasons, the model's summary) lives in
`data/assessments/<id>.json`. Those are short snippets, which is fine — a journal
owns the typesetting, not the underlying facts or a sentence of text. The firm
rule is simply: **never store a whole paper's text** (and the PDFs themselves are
never committed — they're fetched in memory, and `papers/` is gitignored).

## Secret hygiene

- Both secrets live **outside** the repo (`~/.secrets/…`), referenced via env vars.
- `.gitignore` is a backstop (excludes key files, `.env`, `papers/`).
- The real protection is keeping the JSON key out of the project folder entirely.

## Repository reference

The README is deliberately high-level; the detail lives here.

### Two stages

- **Stage 1 — eligibility** (`run_eligibility.py`, `eligibility.yml`, every 4h):
  triage PDFs against the eligibility spec; ELIGIBLE papers wait for stage 2.
- **Stage 2 — extraction** (`run_extraction.py`, `extraction.yml`, manual): pull
  STAVE-shaped data from ELIGIBLE papers and validate it with the real STAVE R
  package, repairing up to 5× before giving up (EXTRACTION_FAILED). Output lands
  in `data/extracted/<id>/`. Pushing to the separate data repo is a later step.

### Layout

```
config/  target_loci.csv — the curated target codon positions (you maintain)
src/     all the code (+ stave_validate.R, the R guardrail)
data/    state — roster.csv, eligibility/<id>.json, extracted/<id>/ (bot);
         exclude.txt, duplicate_decisions.yaml (you)
docs/    NOTES.md + the generated stats.svg
.github/ eligibility.yml, extraction.yml, digest.yml
requirements.txt   Python deps (top level, by convention)
```

### Code

| File | Role |
|---|---|
| `src/run_eligibility.py` | Stage-1 driver (run by `eligibility.yml`). |
| `src/eligibility.py` | Eligibility spec + the structured assessment call. |
| `src/run_extraction.py` | Stage-2 driver + STAVE validate/repair loop (`extraction.yml`). |
| `src/extraction.py` | Extractor schema/rules + writes the four output files. |
| `src/stave_validate.R` | Validates a study's files against the STAVE R package. |
| `src/targets.py` | Loads `config/target_loci.csv`. |
| `src/digest.py` | The weekly digest (run by `digest.yml`). |
| `src/stats.py` | Regenerates `docs/stats.svg` from the roster. |
| `src/drive.py` | Google Drive access (walk / fetch / supplements). |
| `src/store.py` | Roster, exclude list, decisions, per-paper eligibility files. |

### State / config files

| File | Owner | Purpose |
|---|---|---|
| `config/target_loci.csv` | you | The 51 target codon positions (WHO compendium v1.0). |
| `data/roster.csv` | bot | Lightweight: one row per paper — status + at-a-glance flags. |
| `data/eligibility/<id>.json` | bot | The full eligibility decision per paper (the "why"). |
| `data/extracted/<id>/` | bot | STAVE output: study.yaml, surveys.csv, counts.csv, README.md. |
| `data/exclude.txt` | you | Papers to skip entirely. One filename per line. |
| `data/duplicate_decisions.yaml` | you | `duplicate` / `unique` rulings on flagged papers. |

### Secrets (repo settings → Secrets and variables → Actions)

| Secret | Used for |
|---|---|
| `DRIVE_SA_KEY` | Drive service-account JSON key (full file contents). |
| `DRIVE_FOLDER_ID` | Top `papers` folder (walked recursively). |
| `DRIVE_SUPPLEMENT_FOLDER_ID` | Top supplements folder, same tree shape (optional). |
| `ANTHROPIC_API_KEY` | The eligibility and extraction model calls (billed per paper). |

`GITHUB_TOKEN` is provided automatically — no setup needed for the digest.

### STAVE extraction notes

- Targets are the codon positions in `config/target_loci.csv` (genes mapped to
  variantstring tokens via the `vs_gene` column). Encoding follows the
  `variantstring` grammar (`gene:pos:aa`; underscores for within-gene haplotypes;
  `;` across genes; reference AA for wild type; `/` for mixed calls).
- Resolution preference: prefer multi-locus haplotype encoding unless its N is
  <80% of the per-locus N. Wild-type imputed only where the sequenced range is
  known. Every non-trivial call is written into the study's `README.md`.
- The R validator is the guardrail: extraction is only accepted once STAVE's
  `append_data()` accepts it. The output format (14-col surveys with
  `sample_source`, short gene tokens `crt`/`k13`/`dhfr`/`dhps`/`mdr1`/`cytb`,
  reference-AA wild-type rows, the `pmid_` study_id prefix STAVE needs since it
  rejects digit-leading IDs) was validated against a local STAVE 2.0.3 install.
  The repair loop still guards against per-paper surprises.

### Drive layout & contributor access

```
papers/                ← shared with the SERVICE ACCOUNT (Viewer)
├── master/            ←   your own PDFs (incl. institutional-access ones)
│     └── 111.pdf
├── alice/             ← shared with alice only (Editor) — she sees ONLY this
│     └── 222.pdf
└── bob/               ← shared with bob only (Editor)
      └── 333.pdf
```

The pipeline walks this tree read-only (never moves files), tagging each PDF with
its source folder. Contributors see only their own folder, so institutional PDFs
in `master/` stay private. Supplements mirror this shape, with a `<paper-id>/`
folder inside any contributor's subfolder. Adding a contributor = create + share
their subfolder; no secret or code change needed.

### Running locally

```bash
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS=~/.secrets/pfdr-markerbase-key.json
export DRIVE_FOLDER_ID=...            # and DRIVE_SUPPLEMENT_FOLDER_ID if used
export ANTHROPIC_API_KEY=sk-ant-...
python src/pipeline.py
```
