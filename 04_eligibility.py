"""
Experiment 4 — An eligibility-style judgment (mirrors pipeline Step 4).

Combines a system prompt (the curator role) with structured output (a yes/no
plus reasoning). This is a stripped-down version of your real eligibility check.

Run:  python 04_eligibility.py

To try a real paper, replace `abstract` with text loaded from a file, e.g.:

    import json
    abstract = json.load(open("path/to/abstract.json"))["abstract"]
"""
import anthropic
from pydantic import BaseModel

MODEL = "claude-opus-4-8"
client = anthropic.Anthropic()


class Eligibility(BaseModel):
    eligible: bool
    reason: str
    markers_found: list[str]


abstract = (
    "We genotyped pfk13, pfcrt and pfmdr1 in 312 P. falciparum isolates "
    "collected from febrile children in Kisumu, Kenya, in 2021. Mutant allele "
    "frequencies are reported for each locus."
)

resp = client.messages.parse(
    model=MODEL,
    max_tokens=400,
    system="You assess whether a paper reports extractable P. falciparum "
           "resistance-marker frequencies from African field samples.",
    messages=[{"role": "user", "content": f"Assess this abstract:\n\n{abstract}"}],
    output_format=Eligibility,
)

print(resp.parsed_output)
