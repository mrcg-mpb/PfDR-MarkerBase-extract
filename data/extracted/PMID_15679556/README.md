# Extraction record — study PMID_15679556

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 6

## Decisions

# Extraction decisions

## Targets found
Only dhfr codon 108 and dhps codon 437 are within the target list. crt, k13, mdr1, cytb, and other dhfr/dhps positions were not reported.

## Single survey
All molecular data come from a single site (clinic H, Maheba Refugee Settlement) over one collection window (March-June 2002), so survey_id = study_id.

## Counts (Table 3)
dhfr(108): Resistant 104, Mixed 6, Sensitive 3, Total 113.
- Encoded mutant 108N=104, wild type 108S=3, mixed 108S/N=6.
dhps(437): Resistant 50, Mixed 17, Sensitive 46, Total 113.
- Encoded mutant 437G=50, wild type 437A=46, mixed 437A/G=17.
Each position sums to 113 (denominator = all day-0 PCR samples analysed).

## Wild-type handling
Wild-type and mixed categories are explicitly reported in Table 3, so no imputation was needed. Only the two positions analysed (108, 437) are represented; no wild-type imputation for other target positions since the paper only assessed these two codons.

## Haplotype vs per-locus
The paper does not report a linked dhfr;dhps haplotype over target positions; only per-locus counts are given, so per-locus encoding is used.

## Notes
Text states dhps 437 mutant 44.2% but Table 3 gives 44.3% and n=50/113; the table count (50) is used. Supervised/unsupervised subgroup percentages are given but subgroup denominators for genotyping are not cleanly stated (85/84 patients vs 113 PCR samples), so only the pooled site-level Table 3 counts are extracted to avoid fabricating subgroup denominators.

## Geolocation
Maheba (Meheba) Refugee Settlement, North-Western Province, Zambia, placed at approximate settlement centroid (~ -11.15, 25.65).
