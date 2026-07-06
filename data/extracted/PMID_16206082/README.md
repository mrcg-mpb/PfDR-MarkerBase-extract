# Extraction record — study PMID_16206082

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 4

## Decisions

## Targets extracted
Only curated target positions present: crt:76 and mdr1:86. pfmdr1 184F is reported but 184 is not a curated position, so excluded.

## Frequencies
The paper reports resistance-allele prevalences (percentages) among SM cases and matched controls: pfcrt 76T = 63.9% (cases) / 53.7% (controls); pfmdr1 86Y = 45.4% / 42.0%; pfmdr1 184F = 85.8% / 74.1% (184 excluded). No explicit numerator/denominator table for these prevalences.

### Denominator choice
The text states 3-locus data were obtained for 162 cases (69.2%) and 135 matched controls (83.3%). Table 2 gives locus-specific pair counts (pfcrt 76T: 141; pfmdr1 86Y: 185) but those are counts of case-control PAIRS with data, not per-group denominators, and mix cases/controls. I used the 3-locus counts (cases n=162, controls n=135) as the best available denominators. This is an approximation; numerators derived by multiplying percentages, then rounded to nearest whole number. Exact integer counts could not be uniquely determined from the paper, so all four counts are marked approximate in notes.

## Wild-type imputation
Not performed. Although sequenced range covers position 76 and 86 for the genotyped samples, the paper does not give clean wild-type integer counts by group, and mixed calls were coded as resistant for analysis (mixed at 76 and 86 counted as resistant). To avoid fabricating, only the mutant allele counts (derived from stated prevalences) were extracted. Wild-type = total - mutant is implied but not separately emitted to avoid double representation ambiguity; consumers can infer it.

## Case vs control as separate surveys
Cases (severe malaria, admitted) and controls (uncomplicated malaria, outpatients) are treated as two distinct surveys (different sample sources/clinical states) at the same site and time window. No pooling across them.

## Geolocation
Farafenni, The Gambia town centroid (~13.567 N, -15.600 W) used for both hospital and outpatient clinic.

## Duplicate risk
194 controls participated in a separate chloroquine+SP vs coartemether trial (PLoS Med 2005;2:e92) and Farafenni resistance data appear in related same-group papers (refs 18,21,23); potential sample overlap noted.

## Data not used
- pfmdr1 184F (position not curated).
- Table 2/3 odds ratios and pair counts (not extractable as per-group allele frequencies).
