# Extraction record — study PMID_15717281

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 5

## Decisions

## Targets extracted
Only pfcrt codon 76 and pfmdr1 codon 86 are curated targets present in this paper.

## Baseline vs follow-up
Only PRETREATMENT (day 0) frequencies were extracted as a population survey. Post-treatment recurrent-parasite counts (Table 1 follow-up days, Table 2 recrudescence/reinfection) represent drug-selected recurrent parasites, not an unbiased population survey, so they were NOT extracted as frequency counts.

## pfmdr1 codon 86 (Table 1, Day 0)
Direct counts: 86Y=140, 86N=29, mixed 86Y+86N=20, total=189. Encoded mixed as `mdr1:86:N/Y`. No imputation needed; all three categories reconcile to 189.

## pfcrt codon 76
Text states 185 of 190 distinguishable parasite strains carried 76T before treatment (freq 0.974), with 4 pure 76K infections. The denominator (190) differs from the pfmdr1 denominator (189) because pfcrt counts distinguishable strains (mixed infections counted per allele). Wild type 76K imputed as 190-185=5. Note the text mentions '4 pure 76K infections' but the 185/190 count implies 5 non-T strains among distinguishable strains; the small discrepancy arises from mixed-infection accounting. Retained 185 T and 5 K to sum to stated denominator 190.

## Geolocation
Two sites (Kivunge on Unguja, Micheweni on Pemba). Baseline molecular data are pooled across both sites in the paper with no per-site breakdown, so a single survey was created with an approximate central coordinate (~-5.8, 39.5) between the two sites. This is the finest spatial resolution the reported data support.

## Temporal
Single enrollment window Oct 2002-Feb 2003; midpoint 2002-12-30 used. Baseline is a single time bin.

## Data not used
Follow-up/recurrent counts (Tables 1 & 2) excluded as they reflect selection, not survey prevalence.
