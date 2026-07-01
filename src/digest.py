"""
The weekly digest — run by .github/workflows/digest.yml on Friday morning.

Reads roster.csv and maintains a single GitHub issue listing everything that
currently needs your attention: possible duplicates to rule on, papers waiting
on supplementary uploads, and Drive filename clashes. GitHub emails you when the
issue is created or updated. When nothing is outstanding, the issue is closed.

Stdlib only — no pip install needed.

Env (both provided automatically by GitHub Actions):
  GITHUB_TOKEN        a token with `issues: write`
  GITHUB_REPOSITORY   "owner/repo"
"""
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

import store

DATA = Path(__file__).resolve().parent.parent / "data"
ROSTER = DATA / "roster.csv"
ASSESS = DATA / "eligibility"
MARKER = "<!-- markerbase-attention -->"   # hidden tag to re-find our issue
TITLE = "📋 MarkerBase: papers needing attention"

# Assign the attention issue to these GitHub users so they get emailed: an
# assignment (and a comment on each update) notifies you even on the low-noise
# "Participating and @mentions" watch setting — a silent body edit never does.
# Override with the DIGEST_ASSIGNEES env var (comma-separated usernames).
ASSIGNEES = [u.strip() for u in os.environ.get("DIGEST_ASSIGNEES", "bobverity").split(",") if u.strip()]

SECTIONS = [
    (store.REVIEW_DUPLICATE, "🔁 Possible duplicates — rule on each in `duplicate_decisions.yaml`",
     "Add a line `id: duplicate` or `id: unique` to duplicate_decisions.yaml."),
    (store.AWAIT_SUPPLEMENT, "📎 Waiting on supplementary files",
     "Upload the files to Drive in a folder named `<id>` under the supplements folder."),
    (store.SUPPLEMENT_INSUFFICIENT, "🧩 Supplement examined but still insufficient",
     "The uploaded supplement was read but didn't contain the needed data — replace/add the "
     "right files in that `<id>` folder (a change re-triggers assessment), or add the paper to "
     "exclude.txt if it can't be extracted."),
    (store.NAME_COLLISION, "⚠️ Duplicate filenames in Drive",
     "Two files share this name — rename so each PDF is unique."),
    (store.EXTRACTION_FAILED, "🔧 Extraction failed (hit the retry limit)",
     "STAVE rejected the extraction 5×; see data/extracted/<id>/EXTRACTION_FAILED.md."),
]


def load_rows():
    if not os.path.exists(ROSTER):
        return []
    with open(ROSTER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def flag_reason(row):
    """The short 'why' for a flagged paper — from its eligibility assessment file
    for stage-1 flags, or the roster note (collisions, extraction failures)."""
    status = row.get("status")
    if status in (store.NAME_COLLISION, store.EXTRACTION_FAILED):
        return row.get("notes", "")
    rec = store.load_assessment(ASSESS, row["id"]) or {}
    a = rec.get("assessment", {})
    if status == store.REVIEW_DUPLICATE:
        return a.get("duplicate_risk", {}).get("evidence", "") or row.get("notes", "")
    if status in (store.AWAIT_SUPPLEMENT, store.SUPPLEMENT_INSUFFICIENT):
        return a.get("supplement", {}).get("evidence", "") or row.get("notes", "")
    return row.get("notes", "")


def build_body(rows):
    by_status = {s: [] for s, _, _ in SECTIONS}
    for r in rows:
        if r.get("status") in by_status:
            by_status[r["status"]].append(r)

    total = sum(len(v) for v in by_status.values())
    lines = [MARKER, "", f"**{total} paper(s) need your attention.**", ""]
    if total == 0:
        lines.append("Nothing outstanding right now. 🎉")

    for status, heading, action in SECTIONS:
        items = by_status[status]
        if not items:
            continue
        lines.append(f"## {heading} ({len(items)})")
        lines.append(f"_{action}_")
        lines.append("")
        for r in sorted(items, key=lambda x: x["id"]):
            note = flag_reason(r)
            extra = f" — {note}" if note else ""
            lines.append(f"- `{r['id']}`{extra}")
        lines.append("")

    lines.append("---")
    lines.append("_Auto-generated weekly. Resolve items, and they drop off the next digest._")
    return "\n".join(lines), total


def api(method, url, token, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "markerbase-digest",
    })
    if body:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def find_issue(repo, token):
    """Return our existing open attention issue, or None."""
    url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page=100"
    for issue in api("GET", url, token):
        if "pull_request" in issue:
            continue
        if MARKER in (issue.get("body") or ""):
            return issue
    return None


def main():
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        sys.exit("GITHUB_TOKEN and GITHUB_REPOSITORY must be set.")

    body, total = build_body(load_rows())
    existing = find_issue(repo, token)
    base = f"https://api.github.com/repos/{repo}/issues"

    if total == 0:
        if existing:
            api("PATCH", f"{base}/{existing['number']}", token,
                {"body": body, "state": "closed"})
            print(f"Closed issue #{existing['number']} — queue empty.")
        else:
            print("Nothing outstanding; no issue to update.")
        return

    if existing:
        changed = (existing.get("body") or "") != body
        api("PATCH", f"{base}/{existing['number']}", token,
            {"title": TITLE, "body": body, "state": "open", "assignees": ASSIGNEES})
        # A body edit doesn't notify; a comment does. Only comment when the set
        # of outstanding papers actually changed, to avoid weekly noise. The
        # comment repeats the full actionable list (minus the hidden marker) so
        # the notification email is self-contained and informative.
        if changed:
            visible = body.split("\n", 2)[2] if body.startswith(MARKER + "\n") else body
            api("POST", f"{base}/{existing['number']}/comments", token,
                {"body": "🔔 **The attention list changed.**\n\n" + visible})
            print(f"Updated + commented on issue #{existing['number']} — {total} item(s).")
        else:
            print(f"Issue #{existing['number']} unchanged — {total} item(s), no comment.")
    else:
        created = api("POST", base, token,
                      {"title": TITLE, "body": body, "assignees": ASSIGNEES})
        print(f"Opened issue #{created['number']} — {total} item(s).")


if __name__ == "__main__":
    main()
