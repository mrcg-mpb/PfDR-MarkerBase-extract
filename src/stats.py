"""
Generate docs/stats.svg — the live status card embedded in the README.

The README markdown never changes; it just embeds this image. Each pipeline run
regenerates the SVG from the roster, so the numbers under the README update
automatically without ever editing README.md itself.

Run standalone (`python src/stats.py`) or via the stage drivers at end of a run.
"""
import csv
from datetime import date
from pathlib import Path

import pricing
import store

ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "data" / "roster.csv"
OUT = ROOT / "docs" / "stats.svg"
README = ROOT / "README.md"

# Markers in README.md between which the roster table is (re)written each run.
RM_START = "<!-- ROSTER:START -->"
RM_END = "<!-- ROSTER:END -->"
RM_MAX_ROWS = 60          # cap the inline table; full data is linked as CSV

# Palette (GitHub-ish) and bar-chart layout.
INK = "#1f2328"
GREEN = "#2da44e"
BLUE = "#0969da"
AMBER = "#bf8700"
ORANGE = "#bc4c00"
PINK = "#bf3989"
RED = "#cf222e"
PURPLE = "#8250df"
GREY = "#57606a"
MUTE = "#afb8c1"
TRACK = "#eaeef2"

LABEL_X = 24        # x of each row's label
BAR_X = 248         # x where the bar tracks start (room for full labels)
BAR_W = 400         # track width (count sits just past the fill)
BAR_H = 16
ROW_H = 30
TOP = 102           # y of the first bar


def counts():
    c = {}
    if ROSTER.exists():
        with ROSTER.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                s = row.get("status", "")
                c[s] = c.get(s, 0) + 1
    return c


def _bar(y, label, n, colour, maxn):
    """One horizontal bar row: label, background track, proportional fill, count."""
    fillw = max(BAR_W * n / maxn, 4) if (n > 0 and maxn > 0) else 0
    out = [
        f'<text x="{LABEL_X}" y="{y + 12}" font-size="12" fill="{INK}">{label}</text>',
        f'<rect x="{BAR_X}" y="{y}" width="{BAR_W}" height="{BAR_H}" rx="8" fill="{TRACK}"/>',
    ]
    if fillw:
        out.append(f'<rect x="{BAR_X}" y="{y}" width="{fillw:.1f}" height="{BAR_H}" rx="8" fill="{colour}"/>')
    out.append(f'<text x="{BAR_X + fillw + 8:.1f}" y="{y + 12}" font-size="12" '
               f'font-weight="700" fill="{INK}">{n}</text>')
    return "".join(out)


def render(c):
    total = sum(c.values())
    # Every roster status maps to exactly one group, so the bars always sum to
    # the total. Empty groups are dropped below, so the card only shows what's
    # actually in the pipeline (and each row reappears the moment it has a paper).
    groups = [
        ("Extracted",                    [store.EXTRACTED],                 GREEN),
        ("Eligible — to extract",   [store.ELIGIBLE],                  BLUE),
        ("Possible duplicate (to rule)", [store.REVIEW_DUPLICATE],          AMBER),
        ("Awaiting supplement",          [store.AWAIT_SUPPLEMENT],          ORANGE),
        ("Supplement insufficient",      [store.SUPPLEMENT_INSUFFICIENT],   PINK),
        ("Extraction failed",            [store.EXTRACTION_FAILED],         RED),
        ("Filename collision",           [store.NAME_COLLISION],            PURPLE),
        ("Ineligible",                   [store.INELIGIBLE],                GREY),
        ("Excluded / duplicate",         [store.EXCLUDED, store.DUPLICATE], MUTE),
    ]
    cats = [(label, sum(c.get(s, 0) for s in statuses), colour)
            for label, statuses, colour in groups]
    cats = [row for row in cats if row[1] > 0]      # hide empty groups

    maxn = max((n for _, n, _ in cats), default=1)
    height = int(TOP + max(len(cats), 1) * ROW_H + 16)
    if cats:
        rows = "".join(_bar(TOP + i * ROW_H, label, n, colour, maxn)
                       for i, (label, n, colour) in enumerate(cats))
    else:
        rows = (f'<text x="{LABEL_X}" y="{TOP + 12}" font-size="13" fill="{GREY}">'
                "No papers in the pipeline yet.</text>")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" viewBox="0 0 720 {height}" font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">
  <rect x="1" y="1" width="718" height="{height - 2}" rx="12" fill="#ffffff" stroke="#d0d7de"/>
  <text x="24" y="38" font-size="18" font-weight="700" fill="{INK}">MarkerBase &#183; pipeline status</text>
  <text x="696" y="38" font-size="12" text-anchor="end" fill="{GREY}">updated {date.today().isoformat()}</text>
  <text x="24" y="80"><tspan font-size="30" font-weight="700" fill="{INK}">{total}</tspan><tspan font-size="14" fill="{GREY}"> papers seen</tspan></text>
  {rows}
</svg>
'''


# --- README roster table ---------------------------------------------------

def _rows():
    if not ROSTER.exists():
        return []
    with ROSTER.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _row_cost(r):
    return (pricing.cost_usd(r.get("elig_model"), r.get("elig_tok_in"), r.get("elig_tok_out"))
            + pricing.cost_usd(r.get("extract_model"), r.get("extract_tok_in"), r.get("extract_tok_out")))


def _toks(r, stage):
    ti, to = pricing._int(r.get(f"{stage}_tok_in")), pricing._int(r.get(f"{stage}_tok_out"))
    return f"{ti:,} / {to:,}" if (ti or to) else "—"


def roster_markdown():
    """Markdown block (summary + table) written between the README markers."""
    rows = sorted(_rows(), key=lambda r: r.get("id", ""))
    total_cost = sum(_row_cost(r) for r in rows)
    elig_cost = sum(pricing.cost_usd(r.get("elig_model"), r.get("elig_tok_in"), r.get("elig_tok_out"))
                    for r in rows)
    extract_cost = total_cost - elig_cost

    out = [RM_START, "",
           f"**{len(rows)} paper(s) · estimated spend ${total_cost:.2f}** "
           f"(eligibility ${elig_cost:.2f} · extraction ${extract_cost:.2f}) · "
           f"updated {date.today().isoformat()}", ""]
    if not rows:
        out += ["_No papers in the roster yet._", "", RM_END]
        return "\n".join(out)

    out += ["| Study | Status | Model | Elig tok (in/out) | Extract tok (in/out) | Est. $ |",
            "|---|---|---|--:|--:|--:|"]
    for r in rows[:RM_MAX_ROWS]:
        model = r.get("elig_model") or r.get("extract_model") or r.get("model") or "—"
        out.append(f"| `{r.get('id','')}` | {r.get('status','')} | {model} | "
                   f"{_toks(r,'elig')} | {_toks(r,'extract')} | {_row_cost(r):.4f} |")
    if len(rows) > RM_MAX_ROWS:
        out.append(f"| … | _{len(rows) - RM_MAX_ROWS} more_ | | | | |")
    out += ["",
            "_Full sortable, searchable table: [`data/roster.csv`](data/roster.csv) "
            "(GitHub renders CSVs as an interactive table)._", "", RM_END]
    return "\n".join(out)


def update_readme():
    """Rewrite the roster block between the markers in README.md, if present."""
    if not README.exists():
        return
    text = README.read_text(encoding="utf-8")
    if RM_START not in text or RM_END not in text:
        return
    before = text.split(RM_START)[0]
    after = text.split(RM_END, 1)[1]
    README.write_text(before + roster_markdown() + after, encoding="utf-8")


def generate():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(counts()), encoding="utf-8")
    try:
        update_readme()
    except Exception as e:
        print(f"(README roster table not updated: {e})")
    return OUT


if __name__ == "__main__":
    print(f"Wrote {generate()}")
