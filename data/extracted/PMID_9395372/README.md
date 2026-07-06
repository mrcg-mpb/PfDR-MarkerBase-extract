# Extraction record — study PMID_9395372

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 3 · Count rows: 18

## Decisions

## Scope
Extracted only African sites (Mali=Bamako 1995, Kenya=Kilifi 1993, Malawi=Karonga 1995-96). Bolivia (Guayaramerin) is South American and excluded per African-field-sample requirement. Bolivia DHFR 164, Arg-50, Bolivia repeat, and DHPS 581/436/613 data therefore not extracted.

## Target markers extracted
Of the paper's markers, curated targets present are: dhfr:51 (N->I), dhfr:59 (C->R), dhfr:108 (S->N), dhps:436 (S->A), dhps:437 (A->G), dhps:540 (K->E). DHPS 581 and 613 were reported but only at high frequency in Bolivia / rare-absent in Africa; the paper reports the '436+613' paired mutation only combined and at very low African levels, and 581 was absent in Africa — these were not reliably resolvable at the target-single-codon level per site from the figures, so not extracted for African sites. dhfr:108 Thr variant (cycloguanil) was not detected at any site.

## Data source: figure bar graphs
All counts come from Figures 2, 3 and 6, which give percent prevalence bars with the N tested printed per marker per site. Exact numerators are NOT tabulated; variant_num values are ESTIMATES derived from reading bar heights multiplied by the stated N and rounding to whole numbers. These are approximate and flagged in each count's notes. total_num values use the printed N per marker (they differ slightly between markers, e.g. Mali DHFR N=58/56/57, DHPS N=32/58/30).

## Wild-type imputation
Mutation-specific PCR/restriction assays targeted specific codons; the assay distinguishes mutant vs wild type at each assayed codon, so denominators represent samples successfully typed at that position. For dhps:540 in Mali the bar is ~0%, encoded as variant_num=0 (i.e. all wild type Lys-540) rather than emitting a separate wild-type reference count, to avoid ambiguity. No broad range-based wild-type imputation was performed because only specific codons were assayed.

## Haplotype vs per-locus
The paper reports per-locus prevalences only (no per-site multi-locus haplotype counts at target positions); clonal linkage analyses are qualitative. Therefore per-locus extraction was used throughout.

## Temporal
Malawi samples span 1995-1996 and are not disaggregated by year in the figures, so a single combined survey over the 2-year window was created (within the 3-year rule). Mali=1995, Kenya=1993 each a single year.

## Geolocation
Bamako, Kilifi, and Karonga placed at town/city centroids from named clinic locations.

## Duplicate risk
Mali data overlaps with related publications (refs 1, 10, 23); Kenya with ref 22. Counts here are as reported in this paper only.

## Uncertainty
Because numerators were read off bar charts rather than tables, all variant_num values should be treated as approximate (+/- a few samples).
