# Extraction record — study PMID_11865433

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 3 · Count rows: 4

## Decisions

# Extraction decisions

## Target markers
Only crt:76 (K76T) is reported. All other curated positions absent from paper.

## Counts source (Table 1)
Table 1 gives K76T presence/absence counts:
- Madagascar 'Random' group: 0/40 Yes
- Madagascar IC50>=100nM group: 0/24 Yes
- Madagascar Mahajanga region: 0/19 Yes
- Comoro Islands (Moroni/Grande Comore): 33/49 Yes (67%)

## Wild-type imputation
Since Table 1 explicitly reports both 'No' (wild type K76) and 'Yes' (T76) counts as complementary categories with totals, wild-type counts are directly given, not imputed. For Madagascar groups all isolates were wild type (K76 = total sequenced). For Comoros, 33 mutant + 16 wild type = 49.

## Spatial resolution
- The Madagascar 'Random' (n=40, found throughout the island) and IC50>=100nM (n=24, chloroquine-resistant strains) groups are both described as island-distributed selections rather than a distinct site, so they are combined into one island-wide Madagascar survey (n=64). The Mahajanga region group (n=19) is spatially distinct (NW coast) and kept as a separate survey.
- Comoros isolates from Grande Comore / Moroni region kept as separate survey.

## Temporal
- Madagascar isolates dated 2000-2001 (study Feb 2001); range midpoint used.
- Comoro Islands: study performed February 2001.

## Discrepancy noted
Text states 62% (30/48) of Comoro isolates harbored K76T, while Table 1 states 33/49 (67%). Table 1 counts used as the primary reconcilable source. The 30/48 figure not extracted separately to avoid double counting.

## Geolocation
- Madagascar: country centroid (-18.7669, 46.8691).
- Mahajanga: city centroid (-15.7167, 46.3167).
- Grande Comore/Moroni: Moroni city centroid (-11.7022, 43.2551).

## Duplicate risk
Samples from RER national surveillance network; possible overlap with other RER-derived publications.
