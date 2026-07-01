# Extraction record — study PMID_9391510

- Extracted: 2026-07-01
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 6

## Decisions

## Extraction decisions

### Target markers
Only dhfr:51, dhfr:59, dhfr:108 are curated targets present in this paper. Codons 16 and 164 were also studied but are not in the target list, so ignored.

### Haplotype vs per-locus
Table 1 reports full three-locus haplotype patterns (combinations of 51-Ile, 59-Arg, 108-Asn) across all 44 samples. The multi-locus (haplotype) representation was chosen to preserve linkage. All patterns sum to 44 (33+2+1+1+6+1 = 44), consistent with the text stating all 44 children had at least one DHFR mutation and none were wild type. No per-locus breakdown table exists separately, so no comparison of totals needed; haplotype total (44) equals full sample.

### Wild-type imputation within haplotypes
Encoding uses reference amino acids for the loci not mutated in each pattern, since Table 1 explicitly defines each pattern by which of the three codons are mutated (the rest being wild type). Reference codons: 51 N, 59 C, 108 S. E.g. '108-Asn only' encoded as dhfr:51_59_108:N_C_N. The paper explicitly states changes were restricted to these three codons and no wild-type-at-all sample existed (Wildtype row = 0).

### Multiclonal infections
Text notes 14/44 samples showed evidence of multiclonal infection, but Table 1 uniquely assigns each of the 44 samples to a single pattern, so counts are used as reported without dropping any.

### Geolocation
Magoda village, Tanga region, North-east Tanzania (Muheza District area). No coordinates given in paper; approximate coordinates (~-4.9, 38.9) used for the Magoda/Muheza area.

### Temporal
Single study in 1995; no exact dates. One survey, survey_id = study_id. collection_day set to year midpoint 1995-07-02.

### Duplicate risk
Medium: same population/area as 1994 Rønn et al. study; potential overlap noted but this 1995 cohort is distinct sampling.
