# Extraction record — study PMID_19841150

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 2

## Decisions

# Extraction decisions for PMID_19841150 (Karema et al. 2010)

## Overview
Study genotyped 725 P. falciparum isolates at two Rwandan sites (Rukara, eastern; Mashesha/Muganza, western) collected during a 2006 drug trial. Data are presented mostly as HAPLOTYPE/genotype-class frequencies (wild type, single, double, triple, quadruple, mixed) in Figs 1-2 and Tables 1-2, plus a few codon-specific percentages in the text.

## Curated target positions available
Of the target list, this paper reports: dhfr:51, dhfr:59, dhfr:108, dhps:436, dhps:437, dhps:540, dhps:581, dhps:613. (dhfr:164 was reported but is NOT a curated target, so excluded.)

## Why very few per-locus counts could be extracted
The great majority of results are given as multi-locus genotype CLASSES (e.g. 'triple mutant = Asn-108/Ile-51/Arg-59', 'double = 108-Asn/51-Ile') rather than as per-codon counts, and the class labels do NOT uniquely determine which curated codon carries which allele in every isolate (e.g. pfdhps 'double mutant' could be Gly-437/Glu-540 OR Glu-540/Gly-581; 'triple' is 437/540/581). Because the specific codon composition per isolate is ambiguous within these class definitions, per-codon counts cannot be uniquely allocated for most positions. Per Rule 4, these ambiguous class frequencies were NOT converted to fabricated per-codon counts.

## Codon-specific data that WAS extractable (from text)
- pfdhps codon 437 (Gly): '97% of the isolates in Rukara and 80% of the isolates in Mashesha.' These are the only clean per-codon percentages for a curated target with a clear allele.
- pfdhps codon 581 (Gly): 60% Rukara / 29% Mashesha (text) but abstract/discussion give conflicting values (40%/27%); given the inconsistency and unclear denominator, NOT extracted to avoid fabrication.
- pfdhps codon 436 (Ala): '3% (n=22) of the samples analyzed' — this is POOLED across both sites (n=22 of 725), not site-disaggregated, so per Rule 6 the pooled figure was not extracted and no per-site breakdown is available.
- pfdhfr codons 51/59/108: only given as haplotype classes; no clean per-codon site count. Wild type at dhfr codon 16 (not a target) noted as absent.
- pfdhps codon 613: 'not detected' (wild type at 613). See imputation note.

## Denominators
The paper states 725 total genotyped for both genes but does not cleanly split 725 by site. Tables 1-2 give per-site treatment-arm totals (Rukara ~377, Mashesha ~346 from summed table cells), which conflict slightly with 725. For the codon-437 extraction I used approximate site denominators (~365 Rukara, ~358 Mashesha) derived from these; these totals are APPROXIMATE and the resulting counts are percentage-derived. Flagged in notes.

## Wild-type imputation (Rule 3)
dhps:613 was reported as 'Mutations at codon 613 (Ala->Ser) were not detected' and codon 613 was explicitly among the genotyped residues (436,437,540,581,613). This implies all sequenced isolates were wild type (Ala) at 613. However, a clean per-site sequenced N for codon 613 is not separable from the ambiguous class denominators, and I chose not to emit imputed wild-type 613 counts because the reliable per-site denominator is uncertain. Documented here as a conscious omission to avoid attaching a count to an unreliable denominator.

## Data NOT used
- All Fig 1 (pfdhfr) and Fig 2 (pfdhps) genotype-CLASS frequencies: ambiguous per-codon composition (Rule 4).
- Tables 1-2 (outcome-stratified genotype-class counts): ambiguous per-codon allocation and stratified by treatment outcome, not clean molecular-epi counts.
- Pooled codon 436 (n=22/725) and pooled/conflicting codon 581 figures.
- dhfr:164 data (not a curated target).

## Geolocation
- Rukara: sector in Kayonza District, Eastern Province — town/sector centroid (~-1.82, 30.42).
- Mashesha/Muganza: western province site — approximate western Rwanda centroid (~-2.65, 29.0).

## Temporal
Samples collected 2006 (trial NCT00461578); exact months not given, so year-only handling with midpoint 2006-07-02, one survey per site.
