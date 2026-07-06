# Extraction record — study PMID_14728622

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 5

## Decisions

## Summary
Single-site, single-time-window study (Bandim Health Centre, Bissau; Jan-May 2001). One survey (survey_id = study_id). PCR successful in 97/100 samples; denominator = 97 for all counts.

## Target positions extracted
Only curated target codons investigated by the paper: dhfr 51, 59, 108 and dhps 436, 437, 540. dhps 436 A mutation extracted (target ref S -> alt A). Other dhps 436 variant (phenylalanine) is not a curated target and text states none carried it.

## Counts derived from percentages
The paper reports frequencies mainly as percentages of the 97 PCR-successful samples. Figure 1's per-genotype box counts (n=44 wt dhfr, 38 tp dhfr, etc.) are difficult to unambiguously transcribe into per-codon variant counts from the rendered figure, so I relied on the explicitly stated percentages in the Results/Discussion text and converted using N=97:
- dhfr 108 mutant: 52% -> 50/97
- dhfr triple (51+59+108): 41% -> 40/97
- dhps 437: 29% -> 28/97
- dhps 436-alanine: 27% -> 26/97
These are approximations since whole-number counts were not given directly; noted per count.

## Haplotype vs per-locus choice
The triple dhfr mutation (dhfr:51_59_108:I_R_N) is reported as a single figure (41%). Per-locus breakdowns for codons 51 and 59 individually are not cleanly stated as percentages in text (only 108 is given). To avoid double counting, I extracted the codon-108 mutant count AND the triple-mutant haplotype as separate, non-overlapping representations of DIFFERENT information (108 = any-108-mutant prevalence; triple = full haplotype prevalence). These describe overlapping samples but different variant definitions; per STAVE grammar they are distinct variant strings and both are informative. No per-locus 51/59 counts extracted because reliable whole-number values were unavailable.

## Wild-type imputation
dhps codon 540: text explicitly states 'None harboured mutations at codon 540', and codon 540 was among the investigated positions, so wild type (K) imputed at 97/97.
No wild-type imputation attempted for dhfr 51/59/108 or dhps 436/437 individually because exact whole-number sequenced counts and clean mutant-vs-wt breakdowns were not resolvable from the percentage-based reporting.

## Geolocation
Bandim is a semi-urban district on the outskirts of Bissau, Guinea-Bissau. Placed at approximate Bissau/Bandim coordinates (~11.8636, -15.5977) using town/district centroid.

## Data not used
E. coli resistance data (Figures 2, 3) is not a malaria marker and excluded. Figure 1/2/3 detailed genotype box counts not transcribed due to ambiguity in the rendered figure; text percentages used instead.
