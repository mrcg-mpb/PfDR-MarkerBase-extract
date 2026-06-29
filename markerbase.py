"""
Shared core for the MarkerBase pipeline.

Up to now each script carried its own copy of the eligibility schema. Now that
several scripts need it, it lives here ONCE — the schema, the criteria, the
assessment call, and the console report. Scripts import from this module instead
of copy-pasting, so there's a single source of truth to evolve.

This isn't a script you run directly — it's imported (e.g. by 08_assess_from_drive.py).
"""
import base64
from enum import Enum

import anthropic
from pydantic import BaseModel

# Short name -> (full model ID, input $/1M, output $/1M).
MODELS = {
    "haiku": ("claude-haiku-4-5", 1.0, 5.0),
    "sonnet": ("claude-sonnet-4-6", 3.0, 15.0),
    "opus": ("claude-opus-4-8", 5.0, 25.0),
}


# --- The eligibility schema ------------------------------------------------

class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Criterion(BaseModel):
    met: bool
    evidence: str  # a short quote or paraphrase from the paper justifying the call


class EligibilityChecks(BaseModel):
    is_p_falciparum: Criterion
    reports_resistance_markers: Criterion
    reports_extractable_frequencies: Criterion
    african_field_samples: Criterion
    is_primary_study: Criterion


class Assessment(BaseModel):
    eligible: bool                  # True only if ALL five checks are met
    confidence: Confidence
    checks: EligibilityChecks
    markers_found: list[str]
    countries: list[str]
    collection_years: list[int]
    sample_size: int | None
    summary: str
    exclusion_reasons: list[str]


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

SYSTEM = (
    "You are a meticulous curator for a database of P. falciparum "
    "drug-resistance marker frequencies. " + CRITERIA
)


def assess_pdf_bytes(pdf_bytes: bytes, model_key: str = "haiku",
                     client: anthropic.Anthropic | None = None):
    """Send PDF bytes to the model and return the raw response.

    Returns the response object (not just the parsed result) so the caller can
    inspect stop_reason / usage. Use `report()` to print it.
    """
    client = client or anthropic.Anthropic()
    model = MODELS[model_key][0]
    pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    return client.messages.parse(
        model=model,
        max_tokens=1500,
        system=SYSTEM,
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


def report(resp, model_key: str) -> None:
    """Print the verdict (with defensive handling) plus tokens and cost."""
    if resp.stop_reason == "refusal":
        print("[the model declined to assess this paper]")
    elif resp.parsed_output is None:
        print(f"[no structured result — stop_reason: {resp.stop_reason}]")
    else:
        print_assessment(resp.parsed_output)

    _, in_price, out_price = MODELS[model_key]
    cost = (resp.usage.input_tokens / 1e6 * in_price
            + resp.usage.output_tokens / 1e6 * out_price)
    print(f"\n— stop_reason: {resp.stop_reason}")
    print(f"— tokens: {resp.usage.input_tokens} in / {resp.usage.output_tokens} out")
    print(f"— estimated cost: ${cost:.6f}")
