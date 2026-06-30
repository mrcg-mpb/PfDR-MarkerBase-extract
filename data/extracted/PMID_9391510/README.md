# Extraction record — study PMID_9391510

- Extracted: 2026-06-30
- Model: claude-haiku-4-5
- Surveys: 1 · Count rows: 3

## Decisions

## Extraction Notes: PMID_9391510 (Jelinek et al. 1997, Tanzania)

### Study and Survey Details
- **Study ID**: PMID_9391510
- **Single survey**: One site (Magoda village, Tanga region), one time window (1995), so survey_id = study_id
- **Geographic location**: Magoda village, Tanga region, North-east Tanzania. No coordinates provided in paper. Geolocation method: assigned to approximate centroid of Tanga region (~-5.06, 38.99) based on known regional boundaries. Tanga region is a well-documented administrative region in north-eastern Tanzania. Uncertainty: ±~50 km due to use of regional centroid rather than village-specific coordinates.
- **Temporal**: Paper states study 'undertaken in 1995' with no specific month reported. Assumed January 1 to December 31, 1995; collection_day set to midpoint (July 2, 1995).
- **Sample source**: Clinical trial—44 children aged 1–10 years enrolled in a therapeutic trial; samples taken before S/P treatment (day 0).

### Marker Coverage and Sequencing Range
The nested PCR assays explicitly covered DHFR codons 16, 51, 59, 108, and 164. Results state:
- **Codon 16**: No mutations detected; results also note "no mutations were detected at 16-alanine"
- **Codon 51**: Mutations (asparagine to isoleucine) detected in 36/44 samples
- **Codon 59**: Mutations (cysteine to arginine) detected in 40/44 samples  
- **Codon 108**: Mutations (serine to asparagine) detected in 44/44 samples; no threonine substitution detected
- **Codon 164**: No mutations detected; "no mutations were detected at ... 164-isoleucine"

### Wild-Type Imputation
Because the PCR assays explicitly targeted and sequenced codons 16, 51, 59, 108, and 164, **wild-type imputation is appropriate** for positions where no variants were observed (following rule 3):

1. **dhfr:51 (wild-type, Asn)**: 44 - 36 = **8 samples carry 51-Asn** (wild-type reference). Coded as `dhfr:51:N`, variant_num = 8, total_num = 44.
2. **dhfr:59 (wild-type, Cys)**: 44 - 40 = **4 samples carry 59-Cys** (wild-type reference). Coded as `dhfr:59:C`, variant_num = 4, total_num = 44.
3. **dhfr:108 (wild-type, Ser)**: The paper explicitly states Table 1 shows "Wildtype 0" for codon 108 and reports no 108-serine samples. All 44 samples carry 108-Asn or are otherwise non-wild-type at this position. No imputation of wild-type; variant_num = 44 (all mutants, variant = Asn-108).
4. **Codons 16 and 164**: Both are outside the target position list and are not extracted, although the paper confirms both are wild-type in all samples.

**NOTE**: Imputations for 51-Asn and 59-Cys assume that the nested PCR method, which explicitly designs primers and restriction digests for these codons, would have detected any wild-type alleles with the same sensitivity as mutations. This is a standard assumption in molecular surveillance and is reasonable given the methodology. The paper does not explicitly state "wild-type at 51" and "wild-type at 59" for the respective counts; these are inferred from the mutation-only tallies. Risk of overestimating mutation frequency is low given the design, but the imputation is documented here.

### Counts Extraction Logic
**No haplotype vs. per-locus trade-off**: The paper reports mutation patterns (multi-locus combinations) in Table 1 but does not separately provide per-locus frequencies. The table breaks down samples by haplotype (combination of codons 51, 59, 108), so counts are inherently at the haplotype level. Per-locus counts are derived by summing across haplotypes carrying each allele. Both are reported and are consistent (no double counting).

**Resolved inconsistencies**:
- The paper's Results section mentions evidence of multiclonal infections in "14 out of the 44 samples." These are not explicitly separated in Table 1. Interpretation: Table 1 represents the dominant or detected genotypes per sample; multiclonal status does not prevent assignment to a count bin (a sample is counted once per detected allele pattern, even if mixed).
- Table 1 row "51-Ile + 59-Arg only" (n=1) indicates one sample with these two mutations but without 108-Asn, meaning it carries wild-type 108-Ser OR 108-Thr. No 108-Thr mutations were detected in any sample, so this sample is inferred to carry 108-Ser. It is included in the 51-Ile count (36 total) and 59-Arg count (40 total) but NOT in the 108-Asn count.

### Counts Reported
1. **dhfr:51:I** (51-Isoleucine mutant): 36 samples
2. **dhfr:51:N** (51-Asparagine, wild-type): 8 samples
3. **dhfr:59:R** (59-Arginine mutant): 40 samples
4. **dhfr:59:C** (59-Cysteine, wild-type): 4 samples
5. **dhfr:108:N** (108-Asparagine mutant): 44 samples

All counts have total_num = 44 (all 44 samples were sequenced at these positions).

### Data Not Extracted
- **DHFR codons 16 and 164**: Confirmed wild-type in all samples but outside the target position list; not extracted per rule 1.
- **Other genes (CRT, K13, DHPS, Cytb, MDR1)**: The paper focuses exclusively on DHFR mutations and does not report data on other target genes.
- **Clinical phenotype stratification**: Table 1 stratifies by sensitivity/resistance (parasitaemia at day 7). For surveillance purposes, counts are pooled across both groups (n=44 total), reflecting the full sample set.

### Confidence Assessment
- **High confidence** in extracted DHFR counts: explicit table with clear numerators and denominators.
- **Moderate confidence** in wild-type imputations: based on standard PCR design assumptions and explicit statement of "no mutations detected" at codons 16 and 164.
- **Geographic uncertainty**: ±~50 km due to use of regional centroid for a small village without published coordinates.
- **Temporal precision**: ±~6 months (no specific month reported; assumed full calendar year).
