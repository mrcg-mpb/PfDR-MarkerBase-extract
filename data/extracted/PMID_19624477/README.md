# Extraction record — study PMID_19624477

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 4

## Decisions

## Target markers genotyped
Paper genotyped pfcrt K76T; dhfr N51I, C59R, S108N, I164L; dhps A437G, K540E. Of the reported summaries, only pfcrt 76 is presented as a single-locus mutant percentage that can be uniquely allocated.

## Why only crt:76 extracted as counts
Table 1 reports for dhfr/dhps only COMPOSITE summaries: 'dhfr triple mutant %', 'dhps double mutant %', and 'dhfr/dhps quintuple mutant %'. The triple mutant is not defined by explicit codon list in a way mapping to the exact three target codons individually, and no per-locus (individual codon) breakdown is given (text says 'data not shown'). The dhps double mutant combines 437 and 540 but individual 437/540 counts are not separable. Because these composites cannot be uniquely mapped onto individual target-codon variant strings (and encoding the composite would misuse the grammar for single-gene target codons defined here), and per-locus data are explicitly not shown, no dhfr/dhps counts were extracted. Documented as unusable due to lack of per-locus disaggregation.

## dhfr I164L
Text: 'No dhfr I164L mutations were observed at either site.' I164L is NOT in the target position list, so not extracted.

## Wild-type imputation (crt:76)
pfcrt K76T was genotyped in all reported samples (183 Karonga, 148 Blantyre). Karonga: 8.7% of 183 = 15.9 -> 16 mutant, 167 wild type. Blantyre: 0% mutant of 148 -> 148 wild type. Mixed (wild+mutant) samples were classified as mutant by the authors for statistical comparison; the mutant count therefore includes any mixed calls.

## Geolocation
- Karonga (Kaporo Health Centre): placed near Karonga town/Kaporo, northern Malawi, ~lat -9.86, lon 33.93 (district centroid near lakeshore).
- Blantyre (Queen Elizabeth Central Hospital): Blantyre city centroid, lat -15.79, lon 35.01.

## Temporal
- Karonga: May 2007 (month) -> midpoint 2007-05-16.
- Blantyre: year 2007 -> midpoint 2007-07-02.

## Excluded external data
Mbeya (Tanzania) figures in Table 1 are cited from Schönfeld et al. 2007 (external study) and were NOT extracted.
