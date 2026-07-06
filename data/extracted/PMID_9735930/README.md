# Extraction record — study PMID_9735930

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 3 · Count rows: 26

## Decisions

## Extraction decisions

### Root cause of prior validation failure
STAVE sums variant_num across ALL variants sharing the same (study, survey, gene:position) and requires that sum <= total_num. The paper counts MIXED (heterozygous) infections at BOTH alleles of a codon, so its per-allele counts frequently sum to MORE than N (e.g. 1995 dhps:437 alanine 26 + glycine 37 = 63 > 45). These are not a disjoint partition and cannot be uniquely allocated. Storing both alleles at such a position therefore violates the constraint.

### Fix applied
For every position where the two reported allele counts sum to more than N (because of mixed infections), I retained ONLY the mutant/resistance allele row (most informative) and dropped the wild-type companion row. Where the two allele counts DO reconcile exactly to N (day 7 samples, which the paper explicitly states had NO mixed allelic infections), both alleles are eligible; I stored both for dhfr:59 and dhps:436 at day 7. For dhps:437 and dhps:540 at day 7 (which also reconcile) I stored only the mutant for consistency; this loses no unique sample count.

### Positions with only one allele present
Where the wild type was absent (e.g. 1996 dhfr:51:I 27/27, dhfr:108:N), a single row equal to the total was stored.

### Dropped wild-type companions (documented, over-count due to mixed calls)
- 1995 d0: dhfr:51:N (14/45), dhfr:59:C (25/45), dhfr:108:S (8/45), dhps:436:S (45/45), dhps:437:A (26/45), dhps:540:K (25/45)
- 1996 d0: dhfr:59:C (9/27), dhfr:108:S (1/27), dhps:436:S (27/27), dhps:437:A (18/27), dhps:540:K (17/27)
- 1996 d7: dhps:437:A (4/26), dhps:540:K (4/26) [these reconcile but dropped for consistency]

### Source tables
Table 2 used (finest temporal resolution: 1995 day0 n=45, 1996 day0 n=27, 1996 day7 n=26). Table 1 resistant/sensitive split not extracted separately (it is a subset partition of the 1995 all=45 already captured by Table 2, avoiding double counting).

### Surveys
Three surveys: 1995 day0, 1996 day0, 1996 day7. Day 7 kept separate as a distinct selection timepoint.

### Targets
DHFR 51,59,108; DHPS 436,437,540,581,613 extracted. DHFR 16,164 and DHPS 436-phenylalanine ignored (not curated targets). 108-threonine (0 everywhere) is not a curated target (S->N only).

### Haplotype vs per-locus
Only per-locus codon frequencies reported; no multi-locus haplotypes.

### Duplicate risk
DHFR 1995 data previously published (Jelinek et al. 1997) \u2014 same sample set; medium duplicate risk noted.

### Geolocation
Magoda village, Tanga Region, north-east Tanzania (Muheza District). Coordinates ~-4.93, 38.97 approximate; none stated in paper.
