"""
Experiment 3 — Structured output (the heart of your extraction pipeline).

Instead of free text, the model is forced to return data matching a schema, so
you get a validated object you can use directly. This is a miniature of the
real extraction step — lingering here is worth it.

Run:  python 03_structured_output.py

Try editing `text` to something messier or ambiguous and watch how it copes.
"""
import anthropic
from pydantic import BaseModel

MODEL = "claude-opus-4-8"
client = anthropic.Anthropic()


# The schema: what fields you want back, and their types.
class MarkerCount(BaseModel):
    gene: str
    codon: int
    mutant_aa: str
    country: str
    year: int
    mutant_n: int
    total_n: int


text = (
    "In Gondar, Ethiopia, 45 of 200 P. falciparum samples carried the "
    "pfcrt K76T mutation in 2019."
   #"we found a load of wild type mutations in Ghana"
)

resp = client.messages.parse(
    model=MODEL,
    max_tokens=500,
    messages=[
        {"role": "user", "content": f"Extract the resistance marker survey data:\n\n{text}"}
    ],
    output_format=MarkerCount,
)

result = resp.parsed_output  # a validated MarkerCount object
print(result)
print(f"\nmutant fraction: {result.mutant_n}/{result.total_n}")
