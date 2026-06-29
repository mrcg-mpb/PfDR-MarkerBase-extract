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
  upload files to Drive `supplement/<id>/` (one folder per paper, keyed by the
  PDF's name); the next run detects the folder and re-assesses *with* the
  supplement included. It re-tries **once** per upload (tracked by
  `supp_attempts`) so a non-readable supplement can't loop and re-bill forever.
  Only PDF supplements are sent to the model — spreadsheets count as "present"
  but their data can't be read at this stage.

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

`roster.csv` holds only safe, structured fields (status, booleans, marker names,
countries, years) plus a one-line `flag_evidence` quote carried *only* for
flagged papers (so the digest can tell you why). If this repo is **public**, even
those short quotes are paper-derived text. The clean fix is to make the repo
**private** — then storing fuller assessment output is fine too. Recommended,
given the repo now holds assessment results rather than just filenames.

## Secret hygiene

- Both secrets live **outside** the repo (`~/.secrets/…`), referenced via env vars.
- `.gitignore` is a backstop (excludes key files, `.env`, `papers/`).
- The real protection is keeping the JSON key out of the project folder entirely.
