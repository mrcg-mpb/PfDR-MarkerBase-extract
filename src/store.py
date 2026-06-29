"""
State files for the pipeline.

Three files, split by who edits them (see NOTES.md):

  roster.csv     — BOT-OWNED. One row per paper, its current state + light,
                   safe-to-commit metadata. You only ever *read* this.
  exclude.txt    — YOU edit (in the GitHub web UI). One filename per line,
                   '#' for comments. Papers here are skipped, never assessed.
  decisions.yaml — YOU edit. A flat mapping `id: verdict` where verdict is
                   `duplicate` or `unique`, resolving duplicate-risk flags.

Anything you hand-edit is a line-based text format (plain lines / flat YAML),
never CSV — so a spreadsheet can never mangle a PubMed-ID key.
"""
import csv
from pathlib import Path

# --- Status values (a paper's current stage) ------------------------------
EXCLUDED = "EXCLUDED"                  # on exclude.txt — terminal
INELIGIBLE = "INELIGIBLE"             # failed the criteria — terminal (the majority)
DUPLICATE = "DUPLICATE"              # ruled a duplicate via decisions.yaml — terminal
ELIGIBLE = "ELIGIBLE"               # passed, no flags — ready for extraction (stage 2)
REVIEW_DUPLICATE = "REVIEW_DUPLICATE"  # parked: high duplicate risk, awaiting your ruling
AWAIT_SUPPLEMENT = "AWAIT_SUPPLEMENT"  # parked: needs supplementary files you must upload
NAME_COLLISION = "NAME_COLLISION"      # two Drive files share this name — rename one

# Statuses that need your attention — surfaced in the weekly digest.
OPEN_FLAGS = (REVIEW_DUPLICATE, AWAIT_SUPPLEMENT, NAME_COLLISION)

# CSV column order. Kept to safe, structured fields (no free-text quotes from
# papers) except `flag_evidence`, a one-line reason carried only for flagged rows.
ROSTER_FIELDS = [
    "id", "source", "status", "eligible", "confidence",
    "duplicate_risk", "needs_supplement",
    "markers", "countries", "years", "sample_size",
    "spec_version", "model", "first_seen", "last_assessed",
    "supp_attempts", "flag_evidence", "notes",
]


def stem(name):
    """Normalise a filename to its key: drop a trailing '.pdf'."""
    return name[:-4] if name.lower().endswith(".pdf") else name


def load_roster(path):
    path = Path(path)
    if not path.exists():
        return {}
    rows = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[row["id"]] = row
    return rows


def save_roster(path, rows):
    """Write the roster sorted by id, so each run produces a clean diff."""
    path = Path(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ROSTER_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for rid in sorted(rows):
            row = rows[rid]
            writer.writerow({k: row.get(k, "") for k in ROSTER_FIELDS})


def load_exclude(path):
    """Return a set of stems to skip. One filename per line; '#' comments."""
    path = Path(path)
    if not path.exists():
        return set()
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.add(stem(line))
    return out


def load_decisions(path):
    """Return {stem: verdict} from the flat YAML mapping. Verdict lowercased."""
    path = Path(path)
    if not path.exists():
        return {}
    import yaml  # lazy: the digest imports this module but never calls here
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {stem(str(k)): str(v).strip().lower() for k, v in data.items()}
