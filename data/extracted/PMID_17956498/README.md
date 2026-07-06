# Extraction record — study PMID_17956498

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 6

## Decisions

## Extraction decisions

### Source
Single site (Tenrikyo health centre, Makélékélé district, Brazzaville), single collection window (Oct 2003 - Feb 2004). One survey; survey_id = study_id.

### Per-locus vs haplotype
Table 4 gives both per-locus counts and combined-mutation counts (e.g. triple dhfr 51+59+108 = 52/80; quadruple 3dhfr+437 = 42/80). The per-locus data have the full N=80 denominator and provide the individual target-position frequencies without loss. Since target positions are individual codons and the per-locus counts are complete (N=80), per-locus representation was used. Combined/haplotype counts were NOT additionally extracted to avoid double counting. Table 5 (ACPR vs recrudescence subsets, N=44 and 17) is a disaggregation by treatment outcome not by site/time, and its denominators (61 total) are lower than the full pre-treatment set (80); these subsets are subsets of the same 80 isolates, so they were not extracted separately to avoid double counting.

### Wild-type imputation
- dhps 540: text explicitly states 'Lys540Glu substitution was not found' and Methods confirm dhps codon 540 was sequenced. Imputed wild type dhps:540:K = 80/80.
- Target positions covered by dhfr genotyping (51, 59, 108) and dhps genotyping (436, 437) all had reported variant counts, so mutant counts extracted directly (no wild-type-only imputation needed there).
- dhfr 164 and dhps 581, 613 were genotyped (per Methods) but are NOT in the target list, so not extracted. dhps 431 was not assessed.

### Data not used
- Combined multi-locus mutation counts (Table 4 bottom rows) and outcome-stratified counts (Table 5) omitted as duplicates of the per-locus N=80 data.
- No k13, crt, mdr1, cytb data reported.

### Geolocation
Makélékélé is a southern district of Brazzaville. Coordinates (-4.30, 15.23) approximate the district centroid within Brazzaville.
