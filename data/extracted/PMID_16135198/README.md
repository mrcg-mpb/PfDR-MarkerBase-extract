# Extraction record — study PMID_16135198

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 4

## Decisions

# Extraction decisions

## Site & time
- Single site (Tamale, Northern Region, Ghana), single collection window (Aug-Dec 2002). One survey; survey_id = study_id.
- Geolocation: Tamale town centroid (~9.40N, -0.84E).
- Time: range Aug-Dec 2002; collection_day = midpoint 2002-10-16.

## Marker resolution
- The paper reports the dhfr triple mutation (Ile-51+Arg-59+Asn-108) in 47% (59/126). It also reports per-locus prevalences: Ile-51 70/126, Arg-59 82/126, Asn-108 91/126 (all with total_num=126). Per-locus total (126) equals the haplotype total (126), so per the 80% rule per-locus data is fully usable. However, storing both the haplotype AND per-locus would double-count the same 126 samples. I chose the PER-LOCUS representation because it captures each target codon (51, 59, 108) individually with clean denominators (126) and full sample size, whereas the haplotype only reports the triple-mutant count. Per-locus totals (126) = haplotype total (126), so no data loss on denominator.
- Mixed alleles were counted as mutant by the authors; this inflates mutant counts. Recorded in notes.

## Wild-type imputation
- Not imputed: The paper reports mutant prevalences with denominator 126 for dhfr 51/59/108, but wild-type counts are the complement (mixed counted as mutant). I extracted the mutant variant counts directly rather than imputing separate wild-type entries, to avoid ambiguity about mixed allele allocation.

## dhps
- dhps codons 436, 437, 540, 581, 613 genotyped. Figure 1 shows prevalences but exact numerators for the full 126 sample are not given in text for 436, 540, 581, 613. Glu-540 and Gly-581 stated as 'one each' (1/126) and quintuple (dhfr triple + Gly-437 + Glu-540) = 1/126. 
- Gly-437: Table 2 grouping (dhps single Gly-437: 31 failure + 77 ACPR = 108) excludes some categories (mixed/other codons disregarded), so it does not represent a clean 437-mutant count over 126. The exact whole-number count of Gly-437 over the full 126 could not be uniquely determined from text/percentages (Figure 4 recruitment ~44%). I recorded an approximate Gly-437 count flagged in notes; this value is uncertain and should be treated cautiously.

## Data not used
- dhps 436, 540, 581, 613 individual counts over the full 126 sample: not uniquely determinable from text (only figure bars). Glu-540 and Gly-581 stated as 1/126 each but I did not add them as they are qualitative ('too rare, one each') and not cleanly tabulated; omitted to avoid fabrication.
- Treatment-failure vs ACPR subgroup counts (Table 2) and the 35-pair recruitment/failure comparison (Figure 4) were not extracted as separate surveys because they are outcome-stratified subsets of the same 126 (or overlapping) samples, which would double-count.
- Dhfr Thr-108, Val-16, Leu-164 not detected and are not target positions; ignored.

## Duplicate risk
- Samples derive from a parent SP treatment trial (Mockenhaupt et al. 2005, TMIH 10:512-520) and NORMAP; potential overlap with other publications.
