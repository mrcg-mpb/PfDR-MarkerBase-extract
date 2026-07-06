# Extraction record — study PMID_19036751

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 3 · Count rows: 3

## Decisions

## Extraction decisions

### Target positions
Only dhfr:51 (N->I), dhfr:59 (C->R), dhfr:108 (S->N) are among the curated targets. The paper reports these as multi-locus DHFR genotypes (positions 50,51,59,108,164) per country: CNCSI (wild-type), CNCNI (single), CICNI and CNRNI (double), CIRNI (triple).

### Haplotype vs per-locus
The paper only presents genotype frequencies as a stacked pie chart (Figure 1), not a numeric per-locus table. Given the STAVE preference for preserving linkage, the triple mutant CIRNI is encoded as the multi-locus variant dhfr:51_59_108:I_R_N. No separate per-locus breakdown table is provided, so per-locus counts cannot be independently derived without double counting.

### Counts extracted
Only the CIRNI triple-mutant percentages are explicitly stated in text/abstract (Congo 82%, Ghana 81%, Kenya 27%). Counts computed from these percentages against the stated denominators (n=50 Congo, n=54 Ghana, n=55 Kenya):
- Congo: 82% x 50 = 41
- Ghana: 81% x 54 = 43.7 -> 44 (approximate)
- Kenya: 27% x 55 = 14.85 -> 15 (approximate)
These are approximate because the paper gives only percentages read from/reported with a pie chart, not exact tabulated counts.

### Data NOT extracted
The exact counts of the other genotypes (CNCSI wild-type, CNCNI single mutant, CICNI and CNRNI double mutants) are only shown graphically in Figure 1 without numeric percentages in the text, so they could not be reliably quantified. Because these were not uniquely determinable, they were dropped to avoid fabrication. Consequently no wild-type imputation was performed for positions 51/59/108 (partial-composition genotypes prevent a clean single-position wild-type denominator without the omitted genotype counts).

### Wild-type imputation
Not performed. Although the first 184 codons were sequenced (covering positions 51, 59, 108), the presence of multiple partial-mutant genotypes whose exact counts are not numerically reported prevents reliable per-position wild-type totals. Only the explicitly stated triple-mutant frequency was used.

### Geolocation
- Republic of Congo: samples from Pointe-Noire, Brazzaville, Gamboma; frequencies country-aggregated. Placed near Brazzaville (~-4.27, 15.24) as representative central reference.
- Ghana: three villages near Winneba; placed at Winneba (~5.35, -0.62).
- Kenya: two villages in Kisii District; placed at Kisii (~-0.68, 34.77).
All are approximate because frequencies are reported at country level, not per site.

### Temporal
Each country is a single collection year (Congo 2006, Ghana 2004, Kenya 1998); one survey per country-year, midpoint 2 July used for collection_day.
