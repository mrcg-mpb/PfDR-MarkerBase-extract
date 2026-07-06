# Extraction record — study PMID_15941416

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 14

## Decisions

## Study
Single-site, single-year clinical study at Kasangati Medical Complex (Wakiso district, Uganda), samples collected day 0 during year 2000. One survey (survey_id = study_id).

## Target positions extracted
Only curated targets present: dhfr 51, 59, 108 and dhps 437, 540. Other positions not assayed.

## Per-locus vs haplotype choice
Table 3 gives per-codon WT/MX/MT counts out of n=118 successful assays. Table 4 gives haplotype combinations (dhfr mut / dhps mut) but only sums to 113 (3+1+2+4+34+2+2+30+2+3+3+27), which is <80% of the per-locus total (118) — and Table 4 uses mutation-count categories that do not distinguish pure vs mixed alleles nor identify which specific dhps codon (437 vs 540). The per-locus Table 3 is more complete and allele-resolved, so I extracted the PER-LOCUS data from Table 3 and did NOT extract Table 4 haplotypes (avoids double counting; per-locus total 118 > haplotype total 113).

## Mixed alleles
Table 3 reports MX (mixed WT+MT) separately. Encoded as heterozygous calls (e.g. dhfr:51:N/I). WT, MX, and MT counts for each codon sum to 118 (except codon 51: 49+9+60=118 ✓; 59: 81+30+7=118 ✓; 108: 6+37+75=118 ✓; 437: 13+0+105=118 ✓; 540: 19+11+88=118 ✓).

## Wild-type imputation
No imputation beyond reported WT counts was needed — Table 3 explicitly reports WT counts for all five codons out of the 118 assayed. denominators taken directly as 118 (stated: successful completed assays for the three dhfr and two dhps codons were 118).

## Geolocation
Kasangati town, ~20 km NE of Kampala, Wakiso district. Coordinates (~0.442 N, 32.602 E) approximate the Kasangati town centroid.

## Temporal
Clinical/parasitological assessment carried out in 2000; molecular assays done later (2002-2003) but samples were collected day 0 in 2000. Collection window set to full year 2000, midpoint 2000-07-02.

## Not used
Table 4 haplotype data not extracted (see reasoning above). Clinical outcome data (ACR/ETF/LTF, parasitological RI/RII/RIII) not relevant to marker frequencies.
