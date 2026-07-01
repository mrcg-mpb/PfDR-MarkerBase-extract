# Extraction record — study PMID_38594679

- Extracted: 2026-07-01
- Model: claude-opus-4-8
- Surveys: 5 · Count rows: 5

## Decisions

# Extraction decisions

## Target markers found
- **pfmdr1 codon 86 (N->Y)**: Table 4 reports pfmdr1 N86 = 328/328 (100%) wild type at day 0. This is POOLED across all four sites (not disaggregated), so extracted as a single pooled survey (PMID_38594679_pooled). R0 (recurrent-infection) samples 43/43 N86 were NOT extracted separately because they represent post-treatment recurrent infections rather than the enrollment population and are a different denominator; extracting only the day-0 baseline avoids ambiguity.
- **pfk13 codon 469 (C->F / C->Y)**: Table 5 breaks pfk13 SNPs down by site. The paper states pfk13 codons 440-600 were analysed, which covers 469. All detected mutations at 469 were **C469C synonymous** (nucleotide change, amino acid remains wild-type Cys). Therefore every sequenced sample at each site is wild type at the codon-469 AMINO ACID level. Wild type imputed per site: Ipinda 85, Nagaga 88, Karume 79, Simbo 94.

## Wild-type imputation
- pfk13 469: sequenced range (codons 440-600) explicitly covers 469, and no NON-synonymous change at 469 was reported at any site, so wild-type C469 imputed at variant_num = total_num = per-site day-0 sample count (Table 5). C469C is synonymous so does not alter the amino acid.
- pfmdr1 86: reported directly as 100% N86, no imputation needed.

## Not extracted / out of scope
- pfmdr1 184F and D1246: codons 184 and 1246 are NOT in the target list, so excluded.
- Other pfk13 nucleotide changes reported (P417P, R539R, F505F, P475S): codons 417, 539, 505, 475 are NOT target positions (475 target codon is 476; 505 not listed; 539 target is R539T here it's synonymous R539R anyway). Excluded.
- Note: eligibility flagged 'Pfk13 505' and 'Pfk13 475' but these codons are not in the curated target set and were dropped.

## Geolocation
- Karume = Igombe near Mwanza (Lake Victoria, north): ~-2.55, 32.98.
- Ipinda = Kyela, Mbeya region (south): ~-9.53, 33.85.
- Simbo = Igunga, Tabora region (central-NW): ~-4.28, 33.88.
- Nagaga = Masasi, Mtwara region (SE): ~-10.72, 38.80.
- Pooled pfmdr1 survey placed at mainland Tanzania centroid since site-level not resolvable.

## Haplotype vs per-locus
- No multi-locus target haplotypes reported; only single-locus data available.
