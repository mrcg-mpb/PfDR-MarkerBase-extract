# Extraction record — study PMID_9391510

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 6

## Decisions

## Extraction decisions

### Target markers
Only Pfdhfr codons 51 (N->I), 59 (C->R), 108 (S->N) are curated targets present in this paper. Codons 16 and 164 were genotyped but are not target positions and were ignored. Codon 108-threonine was reported absent; the S->T change is not a curated target (target is 108 S->N) so not encoded.

### Haplotype vs per-locus
Table 1 reports full three-locus DHFR patterns for all 44 samples with no missing/other category (Wildtype=0, plus the six mutation patterns which sum to 44). Because the paper reports the complete linked haplotypes, I encoded each pattern as a single three-locus variant string (`dhfr:51_59_108:X_Y_Z`), preserving linkage. All six patterns share total_num=44. This is preferred over per-locus breakdown (which is derivable but would lose linkage and risk double counting).

### Wild-type imputation
The text explicitly states all 44 samples had at least one DHFR mutation (Wildtype=0 in Table 1), and that changes were restricted to codons 51, 59, 108, with no 108-threonine and no 16/164 changes. The three target codons were all sequenced in all 44 samples (denominator 44). Wild-type alleles at individual loci are captured within the haplotype strings (e.g. `N_C_N` carries wild 51 and wild 59). No separate all-wild-type count exists (it is 0). No no-range fallback needed since sequenced positions are explicit.

### Multiclonal infections
Text notes evidence of multiclonal infection in 14 of 44 samples, but Table 1 uniquely assigns each of the 44 to one pattern, so counts reconcile exactly (2+1+1+6+1+33=44). No allocation ambiguity for extraction.

### Spatial
Single site: Magoda village, Muheza District, Tanga region, NE Tanzania. No coordinates in paper; approximated to ~-4.85, 38.9 (Muheza/Magoda area centroid).

### Temporal
Single collection: 1995 (year only). Survey collection_day set to midpoint 1995-07-02.

### Duplicate risk
Same population studied in 1994 (Rønn et al. 1996); this is the 1995 follow-up study. Possible population overlap noted but this paper reports 1995 data.

### Single survey
One site, one time window -> survey_id = study_id (PMID_9391510).
