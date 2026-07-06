# Extraction record — study PMID_11294677

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 11

## Decisions

# Extraction decisions

## Site & time
Single study site: Kampala, Uganda. Geolocated to Kampala city centroid (0.3476, 32.5825). Single collection window Aug 1998-Mar 1999; midpoint 1998-11-30 used for collection_day. One survey = study_id.

## K76T
All 114 randomly selected pre-treatment isolates contained crt:76:T (100%), no mixed/wild. Extracted as crt:76:T 114/114.

## Case-control subset (Table 2, n=30)
The 30-sample case-control set is a subset of the 114, but it reports additional codons (74,75,220,271,326,356,371) and pfmdr-1 86 NOT genotyped in the full 114. To avoid double-counting K76: for position 76 the full 114/114 result was used (larger N); the Table 2 K76T entry (15+15=30) was NOT separately extracted since it duplicates a subset of the 114.

## Denominators
For Table 2, total_num = number successfully amplified = mutant + wild + mixed (excludes 'No result'). Per-position: 74 -> 25 (5 no result); 75,220,371 -> 30; 271 -> 28 (2 no result); 326 -> 29 (1 no result); 356 -> 30; mdr1 86 -> 30.

## Mixed genotypes
Mixed calls could not be uniquely allocated to a single allele, so were left in the denominator but not assigned to either variant. At 326: mutant 5, wild 22, mixed 2 (out of 29). At mdr1 86: mutant 23, wild 1, mixed 6 (out of 30).

## Wild-type imputation
crt:356 reported as only wild-type identified -> crt:356:I 30/30. crt:326 wild-type explicitly reported -> crt:326:N 22/29. No imputation beyond what the paper reported; sequencing ranges for other positions not detailed at per-locus resolution, so no additional wild-type imputed.

## Not extracted
- pfmdr-1 D1246Y: not a curated target position.
- crt:326:D variant: paper only reports N326S, so only S/N alleles extracted.
- Pooled/parent cohort (258 patients) not used; only the reported 114 and 30-sample subset counts extracted.

## Duplicate note
Samples are a subset of a previously published efficacy cohort (ref 9); medium duplicate risk noted.
