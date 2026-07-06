# Extraction record — study PMID_18682531

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 2

## Decisions

# Extraction decisions

## Markers
Only Pfcrt codons 74, 75, 76 were characterized as variable (I/M, E/N, T/K), reported as CVMNK (wild) and CVIET (resistant) haplotypes. Codon 72 was always C (wild), 73 always V. Target positions among these: crt:74, crt:75, crt:76. The paper states all other exon 2 codons matched 3D7 (wild type).

## Haplotype vs per-locus choice
The paper reports single-allele haplotypes pooled across BOTH placenta and venous blood (CVMNK n=11, CVIET n=87, total single-allele n=98), plus 43 mixed. These pooled counts cannot be assigned to a single site (they combine placental + venous), so they violate the no-pooling rule. The compartment-specific quantitative data uniquely available is the K76T / 76K presence figures from Table 2 text: venous 42/69 wild-type 76K; placenta 10/59 wild-type 76K. These are extractable per compartment and were used.

## Why only crt:76:K extracted
- The only counts with clean numerator/denominator broken down by compartment are the 76K (wild-type) presence figures (42/69 venous, 10/59 placenta). These represent samples harbouring the wild-type lysine allele.
- The 76T (mutant) figures are given as percentages (92% venous, 93% placenta) but with mixed infections these are 'presence' proportions that overlap with the 76K presence figures (a mixed sample counts as both 76K present and 76T present). Thus 76K-present + 76T-present would exceed the sample count (double counting individuals with mixed infection). To avoid fabricating a clean allele partition, only the explicitly stated integer count (76K present) was extracted per compartment.
- 92% of 69 = 63.5 and 93% of 59 = 54.9 do not yield unique whole numbers, and would double-count mixed infections, so mutant counts were not extracted.

## Codons 74/75
Because CVMNK and CVIET are the only haplotypes and codons 74/75/76 are perfectly linked in these two haplotypes (74I+75E+76T together, or 74M+75N+76K together), the 76 status fully determines 74 and 75. However, only 76-based integer counts are cleanly stated by compartment, so 74/75 were not separately encoded to avoid duplicating the same individuals under multiple locus rows.

## Wild-type imputation
No separate imputation performed beyond the directly reported wild-type (76K) counts. Sequenced range was Pfcrt exon 2 (all target crt codons in exon 2 covered: 72,74,75), but no variants were found at 72 and no numerator/denominator by compartment for those non-varying positions is cleanly reported per compartment, so they were not added.

## Pooling avoidance
The study reports pooled single-allele haplotype counts (n=98 across both tissues) and combined 141-sample totals; these were NOT extracted as they merge the two compartments (finer resolution = per compartment).

## Geolocation
Both surveys placed at Guediawaye, a suburb of Dakar, Senegal (~14.769 N, -17.406 W, town centroid).

## Temporal
Collection 'during 2000 and 2001'; no per-year breakdown given, so a single 2000-2001 window used (midpoint ~2001-01-01) for both compartment surveys.

## Data dropped
- Pooled single-allele haplotype counts (CVMNK n=11, CVIET n=87) and 43 mixed - not assignable to a single site/compartment.
- Mutant 76T percentages - would double-count mixed infections and yield non-integer numerators.
