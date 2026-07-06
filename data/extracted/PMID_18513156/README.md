# Extraction record — study PMID_18513156

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 14 · Count rows: 50

## Decisions

## Source
All counts taken from Table 2 ("Amino acids at dhfr codons 51, 59, and 108") of Certain et al. 2008. These are monoclonal, enrollment-collected samples (the 'Monoclonal' column serves as the denominator per period). Table 2 reports four haplotype categories: NCS (wild type), ICN (51I/108N double mutant), NRN (59R/108N double mutant), and IRN (triple mutant 51I/59R/108N).

## Haplotype vs per-locus
The paper reports data as three-locus haplotypes over the target dhfr positions 51, 59, 108. I encoded each as a single multi-locus variant string (dhfr:51_59_108:...) to preserve linkage, as instructed. No separate per-locus breakdown is provided in a form with a different denominator, so no comparison of totals was needed.

## Denominators
The 'Monoclonal' column gives the number of enrollment monoclonal samples per period. For each period the four category counts sum exactly to the monoclonal count (e.g. 1987: 5=5; 1993: 2+1+2+1=6; 2006: 1+4+5+28=38). I used the monoclonal count as total_num. The '% ' values in Table 2 confirm the category counts.

## Time bins
Each single-year period in Table 2 becomes its own survey. The pooled '1993-1995' row (11 monoclonal) was NOT extracted because its component years 1993, 1994, 1995 are reported separately (avoiding double counting). Only years with monoclonal counts were extracted; note 1988 had 8 monoclonal but I extracted it as part of no separate treatment-naive analysis 	reatment-exposed post-SP; actually 1988 samples were post-treatment (all children treated with SP by fall 1988) — see below.

## 1988 excluded
The 1988 samples (Collected at enrollment = 0; monoclonal = 8) are post-SP-treatment samples per the text (all 36 children treated with SP over 18 months). They are not treatment-naive enrollment samples and are biased toward resistance, so I excluded 1988 to keep surveys comparable (the main analysis in the paper likewise uses enrollment samples). This choice is documented here.

## Wild-type imputation
No imputation was needed: the paper directly reports wild-type (NCS) counts per period. Positions 51, 59, 108 were all directly genotyped. Other target positions (crt, k13, dhps, mdr1, etc.) were not assessed by this study and are not reported.

## Geolocation
All samples from Kilifi town / Kilifi District Hospital, coastal Kenya. Coordinates set to Kilifi town centroid (-3.6305, 39.8499).

## Duplicate risk
Samples were reused from previously published collections (refs 21, 22/23, and Kilifi District Hospital 1997-2006). Medium duplicate risk with those original studies; noted for downstream deduplication.
