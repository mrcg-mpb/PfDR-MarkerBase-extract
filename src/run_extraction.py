"""
Stage 2 — the extraction driver. Run on demand by
.github/workflows/extraction.yml (manual dispatch for now).

For each ELIGIBLE paper in the roster (capped per run):
  1. Fetch the PDF (+ supplements) from Drive.
  2. Ask the extractor agent for STAVE-shaped study/survey/count data.
  3. Validate it with the real STAVE R package (stave_validate.R).
  4. If it fails, feed the error back to the agent and retry — up to MAX_REPAIRS.
  5. On success: write data/extracted/<id>/{study.yaml, surveys.csv, counts.csv,
     README.md} and set status EXTRACTED. On repeated failure: set
     EXTRACTION_FAILED (surfaced in the weekly digest) and record the error.

Pushing the results to the separate data repo is a deliberately later step.

Env:
  GOOGLE_APPLICATION_CREDENTIALS, DRIVE_FOLDER_ID, DRIVE_SUPPLEMENT_FOLDER_ID,
  ANTHROPIC_API_KEY, EXTRACT_MODEL (default haiku), EXTRACT_MAX_PER_RUN (default 10),
  EXTRACT_MAX_REPAIRS (default 5).
"""
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import drive
import extraction
import store

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "data"
ROSTER = DATA / "roster.csv"
ELIG = DATA / "eligibility"
EXTRACTED = DATA / "extracted"
VALIDATOR = ROOT / "stave_validate.R"

MODEL = os.environ.get("EXTRACT_MODEL", "haiku")
MAX_PER_RUN = int(os.environ.get("EXTRACT_MAX_PER_RUN", "10"))
MAX_REPAIRS = int(os.environ.get("EXTRACT_MAX_REPAIRS", "5"))

OUTPUT_FILES = ("study.yaml", "surveys.csv", "counts.csv", "README.md")


def today():
    return date.today().isoformat()


def run_stave(work):
    """Run the STAVE validator on a work dir. Returns (ok, error_message)."""
    try:
        proc = subprocess.run(
            ["Rscript", str(VALIDATOR), str(work / "study.yaml"),
             str(work / "surveys.csv"), str(work / "counts.csv")],
            capture_output=True, text=True, timeout=300)
    except FileNotFoundError:
        return False, "Rscript not found — is R installed on the runner?"
    except subprocess.TimeoutExpired:
        return False, "STAVE validation timed out"
    out = (proc.stdout or "").strip()
    if out == "OK":
        return True, ""
    return False, out or (proc.stderr or "").strip() or "no output from validator"


def _set(roster, rid, status, notes):
    row = roster.get(rid) or {"id": rid}
    row["status"] = status
    row["notes"] = notes
    roster[rid] = row


def extract_one(rid, pdf, supp, elig_ctx, roster):
    """Extract + validate-repair loop for a single paper. Returns True on success."""
    sid = extraction.stave_id(rid)            # STAVE-valid study_id (letter-first)
    out_dir = EXTRACTED / sid
    work = Path(tempfile.mkdtemp(prefix=f"extract_{sid}_"))
    repair, last_err = None, ""
    try:
        for attempt in range(1, MAX_REPAIRS + 1):
            try:
                resp = extraction.extract(pdf, sid, model_key=MODEL, supplement_bytes=supp,
                                          eligibility_record=elig_ctx, repair=repair)
            except Exception as e:
                last_err = f"extractor error: {e}"
                print(f"  ! {rid} attempt {attempt}: {last_err}")
                break
            ex = resp.parsed_output
            if ex is None:
                last_err = f"no structured output (stop_reason {resp.stop_reason})"
                print(f"  ! {rid} attempt {attempt}: {last_err}")
                break

            extraction.write_outputs(work, sid, ex, MODEL)
            ok, err = run_stave(work)
            if ok:
                out_dir.mkdir(parents=True, exist_ok=True)
                for fn in OUTPUT_FILES:
                    shutil.copy(work / fn, out_dir / fn)
                fail = out_dir / "EXTRACTION_FAILED.md"
                if fail.exists():
                    fail.unlink()
                _set(roster, rid, store.EXTRACTED,
                     f"{len(ex.surveys)} survey(s), {len(ex.counts)} count rows")
                print(f"  · {rid}: EXTRACTED (attempt {attempt})")
                return True

            last_err = err
            repair = {"error": err, "previous": ex.model_dump(mode="json")}
            print(f"  · {rid} attempt {attempt}: STAVE rejected — {err[:140]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    # Out of retries — record the failure for the digest.
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "EXTRACTION_FAILED.md").write_text(
        f"# Extraction failed — study {rid}\n\n"
        f"Hit the validation retry limit ({MAX_REPAIRS}) on {today()}.\n\n"
        f"Last STAVE error:\n\n```\n{last_err}\n```\n", encoding="utf-8")
    _set(roster, rid, store.EXTRACTION_FAILED, f"STAVE: {last_err[:160]}")
    print(f"  ! {rid}: EXTRACTION_FAILED — {last_err[:140]}")
    return False


def main():
    folder_id = os.environ.get("DRIVE_FOLDER_ID")
    if not folder_id:
        sys.exit("Set DRIVE_FOLDER_ID.")
    supp_folder_id = os.environ.get("DRIVE_SUPPLEMENT_FOLDER_ID")  # optional

    svc = drive.service()
    by_stem = {store.stem(p["name"]): p for p in drive.list_pdfs(svc, folder_id)}

    roster = store.load_roster(ROSTER)
    todo = [rid for rid, row in roster.items() if row.get("status") == store.ELIGIBLE]
    todo = sorted(todo)[:MAX_PER_RUN]
    if not todo:
        print("No ELIGIBLE papers to extract.")
        return

    done = failed = 0
    for rid in todo:
        p = by_stem.get(rid)
        if not p:
            print(f"  ! {rid}: PDF no longer in Drive; skipping")
            continue
        pdf = drive.fetch_bytes(svc, p["id"])
        supp = drive.fetch_supplement_pdfs(svc, supp_folder_id, rid) if supp_folder_id else None
        elig = store.load_assessment(ELIG, rid) or {}
        if extract_one(rid, pdf, supp, elig.get("assessment", {}), roster):
            done += 1
        else:
            failed += 1

    store.save_roster(ROSTER, roster)
    try:
        import stats
        stats.generate()
    except Exception as e:
        print(f"(stats not updated: {e})")

    print(f"\nExtracted {done}, failed {failed} (of {len(todo)} eligible this run; model {MODEL}).")


if __name__ == "__main__":
    main()
