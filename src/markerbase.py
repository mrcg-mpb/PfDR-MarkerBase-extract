"""
Shared core for the MarkerBase pipeline: the eligibility spec, the structured
schema the model fills in, and the single assessment call.

The schema does three jobs in one call:
  1. Eligibility — does the paper meet the extraction criteria?
  2. Duplicate risk — might its samples overlap with / be a subset of another study?
  3. Supplement check — does the extractable data live in supplementary files
     that aren't in the PDF we were given?

This module is imported (by pipeline.py), not run directly.
"""
import base64
from enum import Enum

import anthropic
from pydantic import BaseModel

# Bump this when the eligibility spec/schema changes materially. It's stamped on
# every assessed row so we can tell which papers were judged under an old spec.
SPEC_VERSION = 1

# Short name -> (full model ID, input $/1M, output $/1M).
MODELS = {
    "haiku": ("claude-haiku-4-5", 1.0, 5.0),
    "sonnet": ("claude-sonnet-4-6", 3.0, 15.0),
    "opus": ("claude-opus-4-8", 5.0, 25.0),
}


# --- The schema ------------------------------------------------------------

class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class RiskLevel(str, Enum):
    none = "none"
    low = "low"
    medium = "medium"
    high = "high"


class Criterion(BaseModel):
    met: bool
    evidence: str  # a short quote or paraphrase justifying the call


class EligibilityChecks(BaseModel):
    is_p_falciparum: Criterion
    reports_resistance_markers: Criterion
    reports_extractable_frequencies: Criterion
    african_field_samples: Criterion
    is_primary_study: Criterion


class DuplicateRisk(BaseModel):
    level: RiskLevel
    # One short quote/paraphrase if the paper hints its samples are part of a
    # larger or previously-published collection; empty when level is none/low.
    evidence: str


class SupplementNeed(BaseModel):
    needed: bool
    # What extractable data appears to sit in supplementary files we can't see
    # (e.g. "per-locus counts are in Supplementary Table S3"); empty if not needed.
    evidence: str


class Assessment(BaseModel):
    eligible: bool                  # True only if ALL five checks are met
    confidence: Confidence
    checks: EligibilityChecks
    duplicate_risk: DuplicateRisk
    supplement: SupplementNeed
    markers_found: list[str]
    countries: list[str]
    collection_years: list[int]
    sample_size: int | None
    summary: str
    exclusion_reasons: list[str]


# --- The spec the model is judged against ----------------------------------

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

DUPLICATE_GUIDANCE = (
    "DUPLICATE RISK: judge whether this study's samples may overlap with, or be a "
    "subset of, a LARGER or previously-published dataset — for example the paper "
    "states the samples are part of a multi-site consortium, a named cohort, a "
    "surveillance network, or a prior collection. Set `duplicate_risk.level` to "
    "`high` only when there is concrete textual evidence of such overlap, and quote "
    "it in `duplicate_risk.evidence`. Routine new field collections are `none`/`low`."
)

SUPPLEMENT_GUIDANCE = (
    "SUPPLEMENT CHECK: decide whether the EXTRACTABLE per-locus frequency data "
    "appears to live in SUPPLEMENTARY materials that are NOT included in the "
    "document(s) provided to you (e.g. the text points to 'Supplementary Table SX' "
    "for the counts, or says full genotype tables are online). Set "
    "`supplement.needed` to true and quote the pointer in `supplement.evidence`. "
    "If supplementary PDFs ARE included below and they contain the data, set it false."
)

SYSTEM = (
    "You are a meticulous curator for a database of P. falciparum "
    "drug-resistance marker frequencies. " + CRITERIA + "\n\n"
    + DUPLICATE_GUIDANCE + "\n\n" + SUPPLEMENT_GUIDANCE
)


def _pdf_block(pdf_bytes):
    b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")
    return {
        "type": "document",
        "source": {"type": "base64", "media_type": "application/pdf", "data": b64},
    }


def assess_pdf_bytes(pdf_bytes, model_key="haiku", client=None, supplement_bytes=None):
    """Send the paper (and any supplementary PDFs) to the model.

    Returns the raw response object so the caller can inspect stop_reason /
    usage; `resp.parsed_output` is the validated `Assessment` (or None on refusal).
    """
    client = client or anthropic.Anthropic()
    model = MODELS[model_key][0]
    supplement_bytes = supplement_bytes or []

    content = [_pdf_block(pdf_bytes)]
    for sb in supplement_bytes:
        content.append(_pdf_block(sb))

    if supplement_bytes:
        note = (f"The main paper PDF is provided, along with {len(supplement_bytes)} "
                "supplementary PDF(s). ")
    else:
        note = "The main paper PDF is provided. "
    content.append({
        "type": "text",
        "text": note + "Assess it against the eligibility criteria, the duplicate-risk "
                "check, and the supplementary-data check.",
    })

    return client.messages.parse(
        model=model,
        max_tokens=1800,
        system=SYSTEM,
        messages=[{"role": "user", "content": content}],
        output_format=Assessment,
    )


# --- Local debugging helpers (not used by the workflow) --------------------

def print_assessment(a: Assessment) -> None:
    verdict = "ELIGIBLE" if a.eligible else "NOT ELIGIBLE"
    print(f"\n=== {verdict}  (confidence: {a.confidence.value}) ===\n")
    for name, c in a.checks.model_dump().items():
        tick = "✓" if c["met"] else "✗"
        print(f"  {tick} {name}\n      {c['evidence']}")
    print(f"\n  duplicate risk: {a.duplicate_risk.level.value}"
          + (f" — {a.duplicate_risk.evidence}" if a.duplicate_risk.evidence else ""))
    print(f"  needs supplement: {a.supplement.needed}"
          + (f" — {a.supplement.evidence}" if a.supplement.evidence else ""))
    print(f"  markers found : {', '.join(a.markers_found) or '—'}")
    print(f"  countries     : {', '.join(a.countries) or '—'}")
    print(f"  years         : {', '.join(str(y) for y in a.collection_years) or '—'}")
    print(f"  sample size   : {a.sample_size if a.sample_size is not None else '—'}")
    if a.exclusion_reasons:
        print("\n  exclusion reasons:")
        for r in a.exclusion_reasons:
            print(f"    - {r}")
    print(f"\n  summary: {a.summary}")


def report(resp, model_key: str) -> None:
    if resp.stop_reason == "refusal":
        print("[the model declined to assess this paper]")
    elif resp.parsed_output is None:
        print(f"[no structured result — stop_reason: {resp.stop_reason}]")
    else:
        print_assessment(resp.parsed_output)
    _, in_price, out_price = MODELS[model_key]
    cost = (resp.usage.input_tokens / 1e6 * in_price
            + resp.usage.output_tokens / 1e6 * out_price)
    print(f"\n— tokens: {resp.usage.input_tokens} in / {resp.usage.output_tokens} out")
    print(f"— estimated cost: ${cost:.6f}")
