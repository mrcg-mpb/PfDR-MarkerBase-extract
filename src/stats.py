"""
Generate docs/stats.svg — the live status card embedded in the README.

The README markdown never changes; it just embeds this image. Each pipeline run
regenerates the SVG from the roster, so the numbers under the README update
automatically without ever editing README.md itself.

Run standalone (`python src/stats.py`) or via pipeline.py at the end of a run.
"""
import csv
from datetime import date
from pathlib import Path

import store

ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "data" / "roster.csv"
OUT = ROOT / "docs" / "stats.svg"

# Tile / segment colours (GitHub-ish palette).
INK = "#1f2328"
GREEN = "#2da44e"
GREY = "#57606a"
AMBER = "#bf8700"
MUTE = "#afb8c1"


def counts():
    c = {}
    if ROSTER.exists():
        with ROSTER.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                s = row.get("status", "")
                c[s] = c.get(s, 0) + 1
    return c


def _tile(x, n, label, colour):
    return (
        f'<text x="{x}" y="104" font-size="30" font-weight="700" fill="{colour}">{n}</text>'
        f'<text x="{x}" y="126" font-size="12" fill="{GREY}">{label}</text>'
    )


def _segments(total, parts):
    """Stacked proportion bar (clipped to rounded corners)."""
    if total == 0:
        return f'<rect x="24" y="150" width="672" height="16" fill="{MUTE}"/>'
    out, cx = [], 24.0
    for n, colour in parts:
        if n <= 0:
            continue
        w = 672 * n / total
        out.append(f'<rect x="{cx:.1f}" y="150" width="{w:.1f}" height="16" fill="{colour}"/>')
        cx += w
    return "".join(out)


def _legend():
    items = [("passed", GREEN), ("failed", GREY), ("needs you", AMBER), ("excluded/dup", MUTE)]
    out, x = [], 24
    for label, colour in items:
        out.append(f'<rect x="{x}" y="186" width="10" height="10" rx="2" fill="{colour}"/>')
        out.append(f'<text x="{x + 16}" y="195" font-size="11" fill="{GREY}">{label}</text>')
        x += 24 + 7 * len(label) + 18
    return "".join(out)


def render(c):
    total = sum(c.values())
    passed = c.get(store.ELIGIBLE, 0)
    failed = c.get(store.INELIGIBLE, 0)
    attention = (c.get(store.REVIEW_DUPLICATE, 0) + c.get(store.AWAIT_SUPPLEMENT, 0)
                 + c.get(store.NAME_COLLISION, 0))
    dropped = c.get(store.EXCLUDED, 0) + c.get(store.DUPLICATE, 0)

    parts = [(passed, GREEN), (failed, GREY), (attention, AMBER), (dropped, MUTE)]
    tiles = (_tile(24, total, "seen", INK) + _tile(192, passed, "passed", GREEN)
             + _tile(360, failed, "failed", GREY) + _tile(528, attention, "needs you", AMBER))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="220" viewBox="0 0 720 220" font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">
  <defs><clipPath id="bar"><rect x="24" y="150" width="672" height="16" rx="8"/></clipPath></defs>
  <rect x="1" y="1" width="718" height="218" rx="12" fill="#ffffff" stroke="#d0d7de"/>
  <text x="24" y="44" font-size="18" font-weight="700" fill="{INK}">MarkerBase &#183; pipeline status</text>
  <text x="696" y="44" font-size="12" text-anchor="end" fill="{GREY}">updated {date.today().isoformat()}</text>
  {tiles}
  <g clip-path="url(#bar)">{_segments(total, parts)}</g>
  {_legend()}
</svg>
'''


def generate():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(counts()), encoding="utf-8")
    return OUT


if __name__ == "__main__":
    print(f"Wrote {generate()}")
