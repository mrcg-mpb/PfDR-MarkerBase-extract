"""
Stage 2 core: the extractor agent. Pulls STAVE-shaped data out of a paper —
study, survey and count levels — encoding markers as variantstring variant
strings, then writes the four output files for one study.

The output is validated downstream by the real STAVE R package (stave_validate.R);
this module just produces candidate data and documents the decisions made. The
STAVE validation loop in run_extraction.py is the guardrail that catches anything
malformed and feeds the error back here for repair.
"""
import base64
import csv
import re
from datetime import date
from enum import Enum
from pathlib import Path

import anthropic
import yaml
from pydantic import BaseModel

import targets

# STAVE identifiers must start with a letter and contain only letters, digits and
# underscores. Our paper IDs are typically all-digit PMIDs, so we map them to a
# valid study_id by sanitising and prefixing when needed (deterministic).
STAVE_ID_PREFIX = "pmid_"


def stave_id(paper_id):
    s = re.sub(r"[^A-Za-z0-9_]", "_", str(paper_id))
    if not s[:1].isalpha():
        s = STAVE_ID_PREFIX + s
    return s

# Model registry (kept in step with eligibility.py).
MODELS = {
    "haiku": ("claude-haiku-4-5", 1.0, 5.0),
    "sonnet": ("claude-sonnet-4-6", 3.0, 15.0),
    "opus": ("claude-opus-4-8", 5.0, 25.0),
}

ACCESS_LEVEL = "public"   # every paper from this automated pipeline is public

# Exact STAVE column orders (study/survey/count). The output files must match.
STUDY_COLS = ["study_id", "study_label", "description", "access_level",
              "contributors", "reference", "reference_year", "PMID"]
SURVEY_COLS = ["study_id", "survey_id", "country_name", "site_name", "latitude",
               "longitude", "location_method", "location_notes", "sample_source",
               "collection_start", "collection_end", "collection_day",
               "time_method", "time_notes"]
COUNT_COLS = ["study_id", "survey_id", "variant_string", "variant_num", "total_num", "notes"]


# --- The schema the model fills in -----------------------------------------

class SampleSource(str, Enum):
    clinical_passive = "clinical_passive"
    clinical_anc = "clinical_anc"
    clinical_tes = "clinical_tes"
    clinical_trial = "clinical_trial"
    community_household = "community_household"
    community_school = "community_school"
    cohort = "cohort"
    other = "other"
    unknown = "unknown"


class StudyFields(BaseModel):
    # study_id, access_level and are injected by us; the agent supplies the rest.
    study_label: str | None
    description: str | None
    contributors: str | None
    reference: str
    reference_year: int | None
    PMID: str | None


class Survey(BaseModel):
    survey_id: str           # = study_id if a single survey; else study_id + short suffix
    country_name: str | None
    site_name: str | None
    latitude: float
    longitude: float
    location_method: str | None    # how lat/long was determined
    location_notes: str | None     # any imputation / assumptions
    sample_source: SampleSource
    collection_start: str | None   # ISO date YYYY-MM-DD
    collection_end: str | None     # ISO date YYYY-MM-DD
    collection_day: str            # ISO date YYYY-MM-DD (required; midpoint if a range)
    time_method: str | None        # how the date was determined
    time_notes: str | None


class Count(BaseModel):
    survey_id: str           # must match a Survey.survey_id
    variant_string: str      # variantstring encoding, e.g. pfcrt:76:T
    variant_num: int         # numerator (>=0)
    total_num: int           # denominator (>0; samples sequenced at the position)
    notes: str | None


class Extraction(BaseModel):
    study: StudyFields
    surveys: list[Survey]
    counts: list[Count]
    decisions_readme: str    # markdown documenting the extraction decisions made


# --- The spec / rules given to the model -----------------------------------

def _target_table():
    rows = []
    for t in targets.load():
        rows.append(f"  {t['vs_gene']}:{t['position']}  (ref {t['ref_aa']} -> alt {t['alt_aa']})")
    return "\n".join(rows)


ENCODING = (
    "VARIANT STRING ENCODING (variantstring grammar):\n"
    "- One codon: `gene:position:amino_acid`, e.g. `crt:76:T` (the threonine mutant at crt 76).\n"
    "- Use the `gene` token EXACTLY as given in the target table below (e.g. crt, k13, dhfr, mdr1).\n"
    "- WILD TYPE has no special symbol — encode it as the REFERENCE amino acid, e.g. `crt:76:K`.\n"
    "- Haplotype within a gene: `dhfr:51_59_108:I_R_N` (positions ascending).\n"
    "- Cross-gene haplotype: join genes with ';', e.g. `dhfr:51:I;dhps:437:G`.\n"
    "- Mixed/heterozygous call (alleles both observed): `crt:76:K/T`.\n"
    "- `variant_num` = number of samples with that variant; `total_num` = number SEQUENCED at "
    "that position (the denominator). variant_num <= total_num.\n"
)

RULES = (
    "EXTRACTION RULES:\n"
    "1. Targets: extract ONLY the curated positions in the target table below. Ignore other markers.\n"
    "2. Resolution preference: if the paper reports a HAPLOTYPE over target positions, encode it as "
    "one multi-locus variant string (preserves linkage, less data loss). If it reports both a "
    "haplotype AND its per-locus breakdown in separate tables, PREFER the multi-locus form UNLESS "
    "its sample size is much lower — specifically use the per-locus data if the haplotype's total_num "
    "is below 80% of the per-locus total_num. Never store both representations of the same samples "
    "(no double counting). Record the choice and both totals in the README.\n"
    "3. Wild-type imputation: for a target position, if the paper states (or clearly implies) the "
    "sequenced range covers it and reports no variant there, emit the wild-type (reference) count at "
    "variant_num = total_num = N sequenced. If the paper gives NO information on what range was "
    "sequenced, assume only the reported-variant positions were sequenced and do NOT impute wild type "
    "elsewhere. Document every imputation — and, for the no-range fallback, the risk it biases away "
    "from wild type — in the README.\n"
    "4. Inconsistent data: if counts don't reconcile (variant_num > total_num, percentages that don't "
    "map to whole numbers, ambiguous mixed/multiclonal counts that can't be uniquely allocated), do "
    "NOT fabricate — extract only the uniquely-determinable subset and document what was dropped.\n"
    "5. Aim to extract the MAXIMUM information the paper supports, balanced against never inventing "
    "samples.\n"
    "6. Resolution & no pooling: extract at the FINEST spatial and temporal breakdown the paper "
    "reports (per site, per time bin). If the paper ALSO gives pooled totals (national, whole-study, "
    "or multi-year), do NOT additionally extract those — they duplicate the disaggregated counts. "
    "Broader or longer studies therefore yield MORE surveys, never coarser ones.\n"
)

SPATIAL = (
    "SPATIAL: give latitude/longitude for each survey, doing your best from all available context "
    "(site/town/clinic names, regions, descriptions, any coordinates stated). Record HOW you placed "
    "it in `location_method` (e.g. 'stated coordinates', 'town centroid', 'district centroid') and any "
    "assumptions in `location_notes`. One survey per distinct site x time window.\n"
)

IDENTIFIERS = (
    "IDENTIFIERS: every survey_id must START WITH A LETTER and contain only letters, digits and "
    "underscores (the study_id given to you already satisfies this). If the study has a SINGLE survey "
    "(one site, one time window), set survey_id = study_id. If multiple, set survey_id = study_id plus "
    "a short distinguishing suffix (e.g. '_kisumu_2001'). Every count's survey_id must match a survey.\n"
)

TEMPORAL = (
    "TEMPORAL: create a SEPARATE survey for each reported time bin — a multi-year study reported "
    "per-year (or per-block) becomes many surveys, one per (site x time bin), which preserves "
    "temporal resolution; never pool counts across a window wider than the paper reports. "
    "`collection_day` is required (ISO YYYY-MM-DD) for each survey: exact day -> use it; a range -> "
    "set `collection_start`/`collection_end` to the range and `collection_day` to the midpoint; only "
    "a year -> Jan 1 / Dec 31 and the midpoint (~Jul 2). Record the method in `time_method`/`time_notes`.\n"
)

DOCUMENTATION = (
    "README: in `decisions_readme`, write concise markdown documenting the critical extraction "
    "decisions — wild-type imputations made (and any no-range fallback), haplotype vs per-locus "
    "choices (with the totals compared), how each site was geolocated, and any data you could not use "
    "and why. This is the human-facing record of how the numbers were produced.\n"
)


def system_prompt():
    return (
        "You are a meticulous data extractor building a STAVE-format database of P. falciparum "
        "drug-resistance marker frequencies. Extract study-, survey- and count-level data from the "
        "paper into the required schema.\n\n"
        + ENCODING + "\n" + RULES + "\n" + SPATIAL + "\n" + TEMPORAL + "\n" + IDENTIFIERS
        + "\n" + DOCUMENTATION
        + "\nTARGET POSITIONS (encode only these):\n" + _target_table()
    )


def _pdf_block(pdf_bytes):
    b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")
    return {"type": "document",
            "source": {"type": "base64", "media_type": "application/pdf", "data": b64}}


def extract(pdf_bytes, study_id, model_key="haiku", supplement_bytes=None,
            eligibility_record=None, repair=None, client=None, max_tokens=8000):
    """Run the extractor. Returns the raw response; `resp.parsed_output` is an
    `Extraction` (or None on refusal).

    repair: optional {"error": str, "previous": dict} to drive a fix-up retry.
    """
    client = client or anthropic.Anthropic()
    model = MODELS[model_key][0]
    supplement_bytes = supplement_bytes or []

    content = [_pdf_block(pdf_bytes)]
    for sb in supplement_bytes:
        content.append(_pdf_block(sb))

    instr = [f"Extract this paper. Use study_id = '{study_id}' verbatim for every record."]
    if supplement_bytes:
        instr.append(f"{len(supplement_bytes)} supplementary PDF(s) are included above — use them.")
    if eligibility_record:
        instr.append("Context from the eligibility stage (markers/countries/years already spotted): "
                     + str(eligibility_record))
    if repair:
        instr.append("Your PREVIOUS attempt FAILED STAVE validation with this error:\n"
                     + repair["error"]
                     + "\n\nYour previous output was:\n" + str(repair["previous"])
                     + "\n\nFix the specific problem and return the corrected, complete extraction.")
    content.append({"type": "text", "text": "\n\n".join(instr)})

    return client.messages.parse(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt(),
        messages=[{"role": "user", "content": content}],
        output_format=Extraction,
    )


# --- Writing the four output files -----------------------------------------

def _clean(value):
    return "" if value is None else value


def write_outputs(out_dir, study_id, extraction, model_key):
    """Write study.yaml, surveys.csv, counts.csv, README.md for one study."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # study.yaml — inject study_id + access_level; everything else from the agent.
    s = extraction.study
    study = {
        "study_id": study_id,
        "study_label": s.study_label,
        "description": s.description,
        "access_level": ACCESS_LEVEL,
        "contributors": s.contributors,
        "reference": s.reference,
        "reference_year": s.reference_year,
        "PMID": s.PMID,
    }
    (out_dir / "study.yaml").write_text(
        yaml.safe_dump(study, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # surveys.csv
    with (out_dir / "surveys.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SURVEY_COLS)
        w.writeheader()
        for sv in extraction.surveys:
            row = {c: _clean(getattr(sv, c, None)) for c in SURVEY_COLS}
            row["study_id"] = study_id
            row["sample_source"] = sv.sample_source.value
            w.writerow(row)

    # counts.csv
    with (out_dir / "counts.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COUNT_COLS)
        w.writeheader()
        for ct in extraction.counts:
            row = {c: _clean(getattr(ct, c, None)) for c in COUNT_COLS}
            row["study_id"] = study_id
            w.writerow(row)

    # README.md — header + the agent's documented decisions.
    readme = (f"# Extraction record — study {study_id}\n\n"
              f"- Extracted: {date.today().isoformat()}\n"
              f"- Model: {MODELS[model_key][0]}\n"
              f"- Surveys: {len(extraction.surveys)} · Count rows: {len(extraction.counts)}\n\n"
              "## Decisions\n\n" + extraction.decisions_readme.strip() + "\n")
    (out_dir / "README.md").write_text(readme, encoding="utf-8")
