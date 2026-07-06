# Extraction record — study PMID_12224572

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 2

## Decisions

## Target markers
The only curated target position reported is pfmdr1 codon 86 (ref N -> alt Y). Codons 184, 1034, 1042, 1246 are not in the target list and were ignored.

## Counts
- Text states 56/64 (88%) carried mutant Tyr-86, 7 (11%) wild-type Asn-86, and 1 had mixed codons at position 86. Total sequenced at codon 86 = 64.
- Emitted mdr1:86:Y = 56/64 and wild-type mdr1:86:N = 7/64. The 1 mixed isolate cannot be uniquely allocated and is not represented as a separate count (would need a K/T-style mixed string but the specific isolate genotype at 86 for the mixed call is not resolvable); it is retained in the denominator (total_num=64) per the reported sequencing total.

## Wild-type imputation
Wild-type Asn-86 is directly reported (7 isolates), not imputed.

## Resolution / no pooling
The paper reports a single collection window (1997-2000) at one site with no finer spatial or temporal breakdown, so a single survey is created (survey_id = study_id).

## Geolocation
All isolates from Nlongkak Catholic missionary dispensary, Yaounde, Cameroon. Placed at Yaounde city centroid (~3.8667N, 11.5167E).

## Duplicate risk
Prior publications (refs 32,33) reported 1994-1996 data from the same site; the 64 isolates here are the distinct 1997-2000 set, so no overlap in this extraction.
