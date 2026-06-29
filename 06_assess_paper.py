"""
Experiment 6 — Assess a real PDF for eligibility (closer to the real pipeline).

This pulls together everything so far:
  - a system prompt carrying the inclusion criteria   (script 2)
  - structured output via a schema                     (script 3)
  - an eligibility judgment with reasoning             (script 4)
  - defensive stop_reason handling                     (script 2)
  - a --model flag and a per-call cost line            (script 1)

The new piece: it reads an actual PDF from ./papers and sends it straight to
the API as a document (the model reads the PDF itself — no text-extraction
library needed).

Run:  python 06_assess_paper.py --paper 10456963.pdf
      python 06_assess_paper.py --paper 10470338.pdf --model sonnet

--paper takes either a bare filename inside ./papers or a full path.
"""
import argparse
import base64
import pathlib

import anthropic
from pydantic import BaseModel
from enum import Enum

# Short name -> (full model ID, input $/1M, output $/1M).
MODELS = {
    "haiku": ("claude-haiku-4-5", 1.0, 5.0),
    "sonnet": ("claude-sonnet-4-6", 3.0, 15.0),
    "opus": ("claude-opus-4-8", 5.0, 25.0),
}

PAPERS_DIR = pathlib.Path(__file__).parent / "papers"


# --- The eligibility schema ------------------------------------------------
# Deeper than script 4: instead of one bool + reason, every inclusion rule is
# checked individually with the evidence the model used, plus extracted
# metadata. This nested shape is what a real extraction record starts to look
# like.

class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Criterion(BaseModel):
    met: bool
    evidence: str  # a short quote or paraphrase from the paper justifying the call


class EligibilityChecks(BaseModel):
    is_p_falciparum: Criterion          # studies Plasmodium falciparum
    reports_resistance_markers: Criterion  # molecular drug-resistance markers (pfk13, pfcrt, pfmdr1, dhfr, dhps, ...)
    reports_extractable_frequencies: Criterion  # allele/genotype counts or % — not just presence/absence
    african_field_samples: Criterion    # human field/clinical samples from an African country
    is_primary_study: Criterion         # primary empirical study (not a review, meta-analysis, or pure modelling)


class Assessment(BaseModel):
    eligible: bool                  # True only if ALL five checks are met
    confidence: Confidence
    checks: EligibilityChecks
    markers_found: list[str]        # e.g. ["pfk13 C580Y", "pfcrt K76T"]
    countries: list[str]
    collection_years: list[int]
    sample_size: int | None         # total isolates genotyped, if stated
    summary: str                    # one or two sentences explaining the verdict
    exclusion_reasons: list[str]    # empty if eligible; otherwise why it fails


CRITERIA = (
    "A paper is ELIGIBLE only if ALL of the following are true:\n"
    "1. It studies Plasmodium falciparum (not solely P. vivax or another species).\n"
    "2. It reports molecular drug-resistance markers (e.g. pfk13, pfcrt, pfmdr1, "
    "dhfr, dhps, pfpm2/3, k13 propeller mutations).\n"
    "3. It reports EXTRACTABLE marker frequencies — numerator/denominator counts "
    "or percentages per locus — not merely that a mutation was 'present' or 'detected'.\n"
    "4. The samples are human field/clinical isolates collected in an African country "
    "(exclude lab strains, imported/traveller cases, and non-African sites).\n"
    "5. It is a primary empirical study (exclude reviews, meta-analyses, commentaries, "
    "and pure modelling papers).\n\n"
    "Assess each criterion independently and cite the evidence you used. Set "
    "`eligible` to true only when every criterion is met. When a criterion is unmet "
    "or unclear, record it in `exclusion_reasons`. If the PDF text is unreadable or "
    "the relevant section is missing, prefer low confidence over guessing."
)


def resolve_paper(arg: str) -> pathlib.Path:
    """Accept a bare filename (looked up in ./papers) or a full path."""
    p = pathlib.Path(arg)
    if p.is_file():
        return p
    candidate = PAPERS_DIR / arg
    if candidate.is_file():
        return candidate
    available = sorted(f.name for f in PAPERS_DIR.glob("*.pdf"))
    raise SystemExit(
        f"Could not find paper '{arg}'.\n"
        f"Available in {PAPERS_DIR}: {', '.join(available) or '(none)'}"
    )


def print_assessment(a: Assessment) -> None:
    verdict = "ELIGIBLE" if a.eligible else "NOT ELIGIBLE"
    print(f"\n=== {verdict}  (confidence: {a.confidence.value}) ===\n")

    for name, c in a.checks.model_dump().items():
        tick = "✓" if c["met"] else "✗"
        print(f"  {tick} {name}")
        print(f"      {c['evidence']}")

    print(f"\n  markers found : {', '.join(a.markers_found) or '—'}")
    print(f"  countries     : {', '.join(a.countries) or '—'}")
    years = ', '.join(str(y) for y in a.collection_years) or '—'
    print(f"  years         : {years}")
    print(f"  sample size   : {a.sample_size if a.sample_size is not None else '—'}")

    if a.exclusion_reasons:
        print("\n  exclusion reasons:")
        for r in a.exclusion_reasons:
            print(f"    - {r}")

    print(f"\n  summary: {a.summary}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Assess a paper PDF for eligibility.")
    parser.add_argument("--paper", required=True,
                        help="PDF filename inside ./papers, or a full path")
    parser.add_argument("--model", choices=MODELS, default="haiku",
                        help="which model to use (default: haiku)")
    args = parser.parse_args()

    model, in_price, out_price = MODELS[args.model]
    paper_path = resolve_paper(args.paper)

    # Read the PDF and base64-encode it for the document content block.
    pdf_b64 = base64.standard_b64encode(paper_path.read_bytes()).decode("utf-8")

    client = anthropic.Anthropic()
    print(f"Assessing {paper_path.name} with {model} …")

    resp = client.messages.parse(
        model=model,
        max_tokens=1500,
        system=(
            "You are a meticulous curator for a database of P. falciparum "
            "drug-resistance marker frequencies. " + CRITERIA
        ),
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_b64,
                    },
                },
                {"type": "text", "text": "Assess this paper against the eligibility criteria."},
            ],
        }],
        output_format=Assessment,
    )

    # Defensive handling — a refusal or a non-parsed reply must not crash the run.
    if resp.stop_reason == "refusal":
        print("[the model declined to assess this paper]")
    elif resp.parsed_output is None:
        print(f"[no structured result — stop_reason: {resp.stop_reason}]")
    else:
        print_assessment(resp.parsed_output)

    cost = (resp.usage.input_tokens / 1e6 * in_price
            + resp.usage.output_tokens / 1e6 * out_price)
    print(f"\n— stop_reason: {resp.stop_reason}")
    print(f"— tokens: {resp.usage.input_tokens} in / {resp.usage.output_tokens} out")
    print(f"— estimated cost: ${cost:.6f}")


if __name__ == "__main__":
    main()
