"""
State files for the pipeline.

Three files, split by who edits them (see NOTES.md):

  roster.csv          — BOT-OWNED. One LIGHTWEIGHT row per paper: its current
                        state + a few at-a-glance flags. You only ever *read* it.
  eligibility/<id>.json — BOT-OWNED. The full eligibility decision for one paper:
                        every criterion with its evidence, exclusion reasons, the
                        duplicate-risk and supplement findings. The "why".
  extracted/<id>/     — BOT-OWNED. Stage-2 STAVE output for one study.
  exclude.txt         — YOU edit (in the GitHub web UI). One filename per line,
                        '#' for comments. Papers here are skipped, never assessed.
  duplicate_decisions.yaml — YOU edit. A flat mapping `id: verdict` where verdict
                        is `duplicate` or `unique`, resolving duplicate-risk flags.

Anything you hand-edit is a line-based text format (plain lines / flat YAML),
never CSV — so a spreadsheet can never mangle a PubMed-ID key.
"""
import csv
import json
from pathlib import Path

# --- Status values (a paper's current stage) ------------------------------
# Stage 1 — eligibility
EXCLUDED = "EXCLUDED"                  # on exclude.txt — terminal
INELIGIBLE = "INELIGIBLE"             # failed the criteria — terminal (the majority)
DUPLICATE = "DUPLICATE"              # ruled a duplicate via duplicate_decisions.yaml — terminal
ELIGIBLE = "ELIGIBLE"               # passed eligibility — ready for extraction (stage 2)
REVIEW_DUPLICATE = "REVIEW_DUPLICATE"  # parked: high duplicate risk, awaiting your ruling
AWAIT_SUPPLEMENT = "AWAIT_SUPPLEMENT"  # parked: needs supplementary files you must upload
NAME_COLLISION = "NAME_COLLISION"      # two Drive files share this name — rename one
# Stage 2 — extraction
EXTRACTED = "EXTRACTED"               # extracted + passed STAVE validation — terminal
EXTRACTION_FAILED = "EXTRACTION_FAILED"  # hit the validation retry limit — needs your attention

# Statuses that need your attention — surfaced in the weekly digest.
OPEN_FLAGS = (REVIEW_DUPLICATE, AWAIT_SUPPLEMENT, NAME_COLLISION, EXTRACTION_FAILED)

# CSV column order — deliberately lightweight: state + routing flags only. The
# detail (markers, countries, evidence, exclusion reasons, sample size) lives in
# the per-paper eligibility/<id>.json, not here.
ROSTER_FIELDS = [
    "id", "source", "status", "eligible", "confidence",
    "duplicate_risk", "needs_supplement",
    "spec_version", "model", "first_seen", "last_assessed",
    "supp_attempts", "notes",
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


def assessment_path(assess_dir, paper_id):
    return Path(assess_dir) / f"{paper_id}.json"


def save_assessment(assess_dir, paper_id, record):
    """Write the full eligibility decision for one paper as pretty JSON."""
    path = assessment_path(assess_dir, paper_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def load_assessment(assess_dir, paper_id):
    """Return the per-paper assessment record, or None if there isn't one."""
    path = assessment_path(assess_dir, paper_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


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
