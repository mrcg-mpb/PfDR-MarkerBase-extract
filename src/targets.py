"""
Load the curated target drug-resistance codon positions (config/target_loci.csv).

Both stages use this: eligibility checks a paper reports >=1 target position;
extraction encodes exactly these positions (with wild-type imputation). The CSV
is the version-controlled source of truth — see config/target_loci.csv.
"""
import csv
from pathlib import Path

TARGETS_CSV = Path(__file__).resolve().parent.parent / "config" / "target_loci.csv"


def load(path=TARGETS_CSV):
    """Return the target loci as a list of dicts, ignoring '#' comment lines."""
    with open(path, newline="", encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.lstrip().startswith("#")]
    rows = []
    for r in csv.DictReader(lines):
        r["position"] = int(r["position"])
        rows.append(r)
    return rows


def summary(loci=None):
    """Compact per-gene list for prompts, e.g. 'Pfcrt: 72,74,76; Pfk13: 446,458,...'."""
    loci = loci or load()
    by_gene = {}
    for r in loci:
        by_gene.setdefault(r["gene"], set()).add(r["position"])
    return "; ".join(f"{g}: {','.join(str(p) for p in sorted(ps))}"
                     for g, ps in sorted(by_gene.items()))
