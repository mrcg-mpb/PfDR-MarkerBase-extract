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

import store

ROSTER = "roster.csv"
MARKER = "<!-- markerbase-attention -->"   # hidden tag to re-find our issue
TITLE = "📋 MarkerBase: papers needing attention"

SECTIONS = [
    (store.REVIEW_DUPLICATE, "🔁 Possible duplicates — rule on each in `decisions.yaml`",
     "Add a line `id: duplicate` or `id: unique` to decisions.yaml."),
    (store.AWAIT_SUPPLEMENT, "📎 Waiting on supplementary files",
     "Upload the files to Drive under `supplement/<id>/`, then the pipeline resumes them."),
    (store.NAME_COLLISION, "⚠️ Duplicate filenames in Drive",
     "Two files share this name — rename so each PDF is unique."),
]


def load_rows():
    if not os.path.exists(ROSTER):
        return []
    with open(ROSTER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


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
            note = r.get("flag_evidence") or r.get("notes") or ""
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
        api("PATCH", f"{base}/{existing['number']}", token,
            {"title": TITLE, "body": body, "state": "open"})
        print(f"Updated issue #{existing['number']} — {total} item(s).")
    else:
        created = api("POST", base, token, {"title": TITLE, "body": body})
        print(f"Opened issue #{created['number']} — {total} item(s).")


if __name__ == "__main__":
    main()
