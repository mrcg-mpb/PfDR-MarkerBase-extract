"""
Stage 1 core: the eligibility spec, the structured schema the model fills in, and
the single assessment call.

The schema does three jobs in one call:
  1. Eligibility — does the paper meet the extraction criteria?
  2. Duplicate risk — might its samples overlap with / be a subset of another study?
  3. Supplement check — does data we'd need live in supplementary files not provided?

This module is imported (by run_eligibility.py), not run directly.
"""
import base64
from enum import Enum

import anthropic
from pydantic import BaseModel

import targets

# Bump this when the eligibility spec/schema changes materially. It's stamped on
# every assessed row so we can tell which papers were judged under an old spec.
SPEC_VERSION = 2

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
    reports_target_markers: Criterion            # >=1 of the curated target positions
    reports_extractable_frequencies: Criterion
    sub_country_location: Criterion              # every datapoint placeable below country level
    temporal_resolution_within_3y: Criterion     # every datapoint tied to a <=3-year window
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
    eligible: bool                  # True only if ALL checks are met
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

TARGET_SUMMARY = targets.summary()

CRITERIA = (
    "A paper is ELIGIBLE only if ALL of the following are true:\n"
    "1. P. falciparum — studies Plasmodium falciparum (not solely P. vivax or another species).\n"
    "2. Target markers — reports at least ONE of these curated drug-resistance codon "
    f"positions: {TARGET_SUMMARY}.\n"
    "3. Extractable frequencies — gives numerator/denominator counts or percentages per "
    "locus for those markers, not merely that a mutation was 'present' or 'detected'.\n"
    "4. Sub-country resolution — every extractable frequency can be tied to a location BELOW "
    "country level (a named sub-national admin unit, town, site, clinic, or explicit coordinates). "
    "This is about RESOLUTION, not extent: broad geographic coverage is fine and welcome — a "
    "nationwide study spanning many regions is desirable (more data). What fails is a frequency "
    "that can ONLY be placed at country level (e.g. a single national pooled total with no "
    "sub-national breakdown). A paper reporting both national totals AND a sub-national breakdown "
    "PASSES. If finer locations are likely in supplementary material, flag the supplement rather "
    "than failing this criterion.\n"
    "5. Temporal resolution <= 3 years — every extractable frequency can be tied to a collection "
    "window of at most three years. This is about the REPORTING INTERVAL, not the study's total "
    "length: a study running over many years is fine and welcome (more data), PROVIDED its data are "
    "binned finely enough in time. A 2016-2021 study that reports per-year (or per-<=3-year-block) "
    "frequencies PASSES; what fails is a single pooled frequency whose samples span MORE than three "
    "years, because it cannot be placed precisely enough in time. Judge the finest temporal "
    "breakdown the paper reports, not the overall span.\n"
    "6. African field samples — human field/clinical isolates collected in an African country "
    "(exclude lab strains, imported/traveller cases, and non-African sites).\n"
    "7. Primary study — a primary empirical study (exclude reviews, meta-analyses, "
    "commentaries, and pure modelling papers).\n\n"
    "Assess each criterion independently and cite the evidence you used. Set `eligible` to "
    "true only when EVERY criterion is met. When a criterion is unmet or unclear, record it "
    "in `exclusion_reasons`. Prefer low confidence over guessing."
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
    "SUPPLEMENT CHECK: decide whether data we'd need for extraction appears to live in "
    "SUPPLEMENTARY materials NOT included in the document(s) provided — either (a) the "
    "EXTRACTABLE per-locus frequency counts (e.g. the text points to 'Supplementary Table "
    "SX'), or (b) finer SPATIAL detail (site-level locations) that would lift an otherwise "
    "country-only paper above the sub-country resolution floor. Set `supplement.needed` to "
    "true and quote the pointer in `supplement.evidence`. If supplementary PDFs ARE included "
    "below and contain the data, set it false."
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
