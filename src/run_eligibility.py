"""
Stage 1 — the eligibility driver. Run on a schedule by
.github/workflows/eligibility.yml.

Each run:
  1. Lists the PDFs currently in the Drive inbox folder.
  2. Applies your rulings from duplicate_decisions.yaml to any parked duplicates.
  3. Figures out what to work on:
       - new papers (in Drive, not yet in roster.csv)
       - AWAIT_SUPPLEMENT papers whose supplement folder has now appeared
     ...skipping anything on exclude.txt or with a clashing filename.
  4. Assesses up to MARKERBASE_MAX_PER_RUN papers (the rest wait for next run).
  5. Routes each to a status, writes roster.csv + eligibility/<id>.json.

It never notifies you — the weekly digest (digest.py) does that. The roster is
the durable queue between this stage and extraction.

Env:
  GOOGLE_APPLICATION_CREDENTIALS  path to the Drive service-account key
  DRIVE_FOLDER_ID                 the inbox folder of PDFs
  DRIVE_SUPPLEMENT_FOLDER_ID      (optional) parent of the supplement/<id>/ folders
  ANTHROPIC_API_KEY               for the assessment call
  MARKERBASE_MODEL                haiku | sonnet | opus   (default: haiku)
  MARKERBASE_MAX_PER_RUN          cost cap per run         (default: 100)
"""
import os
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import drive
import eligibility as agent
import store

DATA = Path(__file__).resolve().parent.parent / "data"
ROSTER = DATA / "roster.csv"
EXCLUDE = DATA / "exclude.txt"
DECISIONS = DATA / "duplicate_decisions.yaml"
ASSESS = DATA / "eligibility"   # per-paper <id>.json eligibility decisions

MODEL = os.environ.get("MARKERBASE_MODEL", "haiku")
MAX_PER_RUN = int(os.environ.get("MARKERBASE_MAX_PER_RUN", "100"))

TRUE_STRINGS = {"true", "1", "yes"}


def today():
    return date.today().isoformat()


def is_true(value):
    return str(value).strip().lower() in TRUE_STRINGS


# --- Applying your duplicate rulings ---------------------------------------

def apply_decisions(roster, decisions):
    """Resolve papers parked at REVIEW_DUPLICATE using duplicate_decisions.yaml."""
    for s, verdict in decisions.items():
        row = roster.get(s)
        if not row or row.get("status") != store.REVIEW_DUPLICATE:
            continue  # only act on papers currently awaiting your ruling
        if verdict in ("duplicate", "dup", "exclude"):
            row["status"] = store.DUPLICATE
            row["notes"] = "ruled duplicate via duplicate_decisions.yaml"
        elif verdict in ("unique", "proceed", "keep"):
            # Cleared as unique. If the stored assessment also wanted a
            # supplement, send it there; otherwise it's ready for extraction.
            if is_true(row.get("needs_supplement")):
                row["status"] = store.AWAIT_SUPPLEMENT
                row["notes"] = "ruled unique; now awaiting supplement"
            else:
                row["status"] = store.ELIGIBLE
                row["notes"] = "ruled unique via duplicate_decisions.yaml"


# --- Row builders ----------------------------------------------------------

def _base_row(existing, s, source=None):
    existing = existing or {}
    return {
        "id": s,
        "source": source if source is not None else existing.get("source", ""),
        "first_seen": existing.get("first_seen") or today(),
        "notes": existing.get("notes", ""),
    }


def excluded_row(existing, s, source):
    row = _base_row(existing, s, source)
    row.update(status=store.EXCLUDED, last_assessed="", notes="on exclude.txt")
    return row


def collision_row(existing, s, files):
    row = _base_row(existing, s)
    sources = ", ".join(sorted({f["source"] or "root" for f in files}))
    row.update(status=store.NAME_COLLISION,
               notes=f"{len(files)} files share this name (in: {sources}) — rename so each is unique")
    return row


def route(existing, s, assessment, mode, source):
    """Decide the new status, write the full per-paper decision, and return the
    lightweight roster row."""
    row = _base_row(existing, s, source)
    attempts = int((existing or {}).get("supp_attempts") or 0)
    if mode == "resume":
        attempts += 1
    row.update(last_assessed=today(), spec_version=agent.SPEC_VERSION,
               model=MODEL, supp_attempts=attempts)

    if assessment is None:
        row.update(status=store.INELIGIBLE, notes="model returned no structured result")
        return row

    a = assessment
    # The roster keeps only at-a-glance flags...
    row.update(
        eligible=a.eligible,
        confidence=a.confidence.value,
        duplicate_risk=a.duplicate_risk.level.value,
        needs_supplement=a.supplement.needed,
    )
    # ...while the full reasoning (every criterion + evidence, exclusion reasons,
    # markers, countries, years, sample size) goes to eligibility/<id>.json.
    store.save_assessment(ASSESS, s, {
        "id": s,
        "source": source,
        "model": MODEL,
        "spec_version": agent.SPEC_VERSION,
        "assessed": today(),
        "assessment": a.model_dump(mode="json"),
    })

    if not a.eligible:
        row["status"] = store.INELIGIBLE
        return row
    if a.duplicate_risk.level.value == "high":
        row["status"] = store.REVIEW_DUPLICATE
        return row
    if a.supplement.needed:
        row["status"] = store.AWAIT_SUPPLEMENT
        if mode == "resume":
            row["notes"] = "supplement uploaded but data still not found"
        return row
    row["status"] = store.ELIGIBLE
    return row


# --- Main ------------------------------------------------------------------

def main():
    folder_id = os.environ.get("DRIVE_FOLDER_ID")
    if not folder_id:
        sys.exit("Set DRIVE_FOLDER_ID.")
    supp_folder_id = os.environ.get("DRIVE_SUPPLEMENT_FOLDER_ID")  # optional

    svc = drive.service()
    pdfs = drive.list_pdfs(svc, folder_id)

    roster = store.load_roster(ROSTER)
    exclude = store.load_exclude(EXCLUDE)
    decisions = store.load_decisions(DECISIONS)

    # Group Drive files by stem so we can detect name collisions.
    by_stem = {}
    for p in pdfs:
        by_stem.setdefault(store.stem(p["name"]), []).append(p)
    collisions = {s for s, lst in by_stem.items() if len(lst) > 1}

    # Your rulings on previously-parked duplicates.
    apply_decisions(roster, decisions)

    # Build the work queue: (stem, drive_id, source, mode).
    queue = []
    for s, lst in by_stem.items():
        source = lst[0]["source"]
        if s in collisions:
            roster[s] = collision_row(roster.get(s), s, lst)
            continue
        if s in exclude:
            if roster.get(s, {}).get("status") != store.EXCLUDED:
                roster[s] = excluded_row(roster.get(s), s, source)
            continue
        existing = roster.get(s)
        if existing is None:
            queue.append((s, lst[0]["id"], source, "new"))
        elif existing.get("status") == store.AWAIT_SUPPLEMENT:
            # Resume once per upload: only if a supplement has appeared and we
            # haven't already re-assessed against it.
            if (supp_folder_id and int(existing.get("supp_attempts") or 0) < 1
                    and drive.supplement_ready(svc, supp_folder_id, s)):
                queue.append((s, lst[0]["id"], source, "resume"))

    # Process, capped.
    assessed = deferred = failed = 0
    for s, fid, source, mode in queue:
        if assessed >= MAX_PER_RUN:
            deferred += 1
            continue
        try:
            supp = drive.fetch_supplement_pdfs(svc, supp_folder_id, s) if mode == "resume" else None
            pdf_bytes = drive.fetch_bytes(svc, fid)
            resp = agent.assess_pdf_bytes(pdf_bytes, model_key=MODEL, supplement_bytes=supp)
        except Exception as e:  # don't let one bad paper abort the whole run
            print(f"  ! {s}: {e}")
            failed += 1
            continue
        assessed += 1
        roster[s] = route(roster.get(s), s, resp.parsed_output, mode, source)
        print(f"  · {s}: {roster[s]['status']}")

    store.save_roster(ROSTER, roster)

    # Refresh the status visual embedded in the README. Non-fatal if it fails.
    try:
        import stats
        stats.generate()
    except Exception as e:
        print(f"(stats SVG not updated: {e})")

    counts = Counter(r.get("status", "") for r in roster.values())
    print(f"\nAssessed {assessed} this run "
          f"({deferred} deferred, {failed} failed; cap {MAX_PER_RUN}, model {MODEL}).")
    print("Roster status counts:")
    for status, n in sorted(counts.items()):
        print(f"  {status:18} {n}")


if __name__ == "__main__":
    main()
