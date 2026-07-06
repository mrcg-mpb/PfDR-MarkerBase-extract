# Extraction record — study PMID_16235185

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 5

## Decisions

## Extraction decisions

### Scope
Only the 2002 in vitro surveillance subset provides extractable target-marker frequencies. The 1995 chemotherapy-trial samples (Table 1) report pfmdr1 codon 86 only for a small selected set of amplified/multiclonal samples (n=10 with mixed calls), which cannot be uniquely allocated to a well-defined denominator population, so no counts were extracted from 1995. Table 2 (EC50/EC90) contains no target-marker genotype data.

### Target markers present
- mdr1:86 (N86Y) and crt:76 (K76T). Codon 184 (pfmdr1) is not a target position and was ignored. S1034/N1042 and pfcrt 76 are the only relevant loci; S1034/N1042 are not targets.

### mdr1:86
Text: '86Y exclusively detected in 30 samples (plus 3 in which detected along with N86, overall 89%); only 1 sample exclusively N86 (plus 3 mixed, overall 11%).' 30+1+3 = 34 = denominator. Extracted mdr1:86:Y=30/34, mdr1:86:N=1/34, mdr1:86:N/Y (mixed)=3/34.

### crt:76
Text: 'all but one carried the pfcrt K76T mutation' among 34 samples => crt:76:T=33/34. Wild type imputed: crt:76:K=1/34. This is a direct statement, so wild-type imputation is well supported.

### Wild-type imputation
- crt:76:K = 1/34 imputed from 'all but one' of 34. mdr1:86:N = 1 stated directly (not imputed).

### Geolocation
Single site, Lambarene, Gabon (Albert Schweitzer Hospital). Coordinates ~ -0.70, 10.23 (town centroid).

### Temporal
Single survey for the 2002 surveillance window (Feb-Jun 2002); midpoint 2002-04-15 used as collection_day.

### Duplicate risk
Samples derive from previously published studies (refs 11, 13, 14). The 2002 marker data are from ref 11's isolates. Noted for downstream deduplication.

### Data not used
- 1995 Table 1: mixed/composite copy-number and codon-86 calls on selected amplified samples; not a clean denominator, dropped.
- Codon 184, S1034, N1042: not target positions.
