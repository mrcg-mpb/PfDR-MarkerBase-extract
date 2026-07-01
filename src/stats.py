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

import store

ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "data" / "roster.csv"
OUT = ROOT / "docs" / "stats.svg"

# Palette (GitHub-ish) and bar-chart layout.
INK = "#1f2328"
GREEN = "#2da44e"
BLUE = "#0969da"
AMBER = "#bf8700"
GREY = "#57606a"
MUTE = "#afb8c1"
TRACK = "#eaeef2"

LABEL_X = 24        # x of each row's label
BAR_X = 200         # x where the bar tracks start
BAR_W = 452         # track width (count sits just past the fill)
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
    # Five outcome groups that together cover EVERY roster status, so the bars
    # always sum to the total shown in the header.
    cats = [
        ("Extracted",             c.get(store.EXTRACTED, 0),  GREEN),
        ("Eligible (to extract)", c.get(store.ELIGIBLE, 0),   BLUE),
        ("Needs attention",       c.get(store.REVIEW_DUPLICATE, 0) + c.get(store.AWAIT_SUPPLEMENT, 0)
                                   + c.get(store.NAME_COLLISION, 0) + c.get(store.EXTRACTION_FAILED, 0), AMBER),
        ("Ineligible",            c.get(store.INELIGIBLE, 0), GREY),
        ("Excluded / duplicate",  c.get(store.EXCLUDED, 0) + c.get(store.DUPLICATE, 0), MUTE),
    ]
    maxn = max((n for _, n, _ in cats), default=0)
    height = int(TOP + len(cats) * ROW_H + 16)
    rows = "".join(_bar(TOP + i * ROW_H, label, n, colour, maxn)
                   for i, (label, n, colour) in enumerate(cats))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" viewBox="0 0 720 {height}" font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">
  <rect x="1" y="1" width="718" height="{height - 2}" rx="12" fill="#ffffff" stroke="#d0d7de"/>
  <text x="24" y="38" font-size="18" font-weight="700" fill="{INK}">MarkerBase &#183; pipeline status</text>
  <text x="696" y="38" font-size="12" text-anchor="end" fill="{GREY}">updated {date.today().isoformat()}</text>
  <text x="24" y="80"><tspan font-size="30" font-weight="700" fill="{INK}">{total}</tspan><tspan font-size="14" fill="{GREY}"> papers seen</tspan></text>
  {rows}
</svg>
'''


def generate():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(counts()), encoding="utf-8")
    return OUT


if __name__ == "__main__":
    print(f"Wrote {generate()}")
