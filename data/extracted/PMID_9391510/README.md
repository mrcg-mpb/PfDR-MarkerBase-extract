# Extraction record — study PMID_9391510

- Extracted: 2026-06-30
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 6

## Decisions

## Extraction decisions

### Target markers
Paper reports Pfdhfr codons 51 (N->I), 59 (C->R), 108 (S->N), all curated targets. Codons 16 and 164 were also assayed but are not target positions and are excluded.

### Haplotype vs per-locus
Table 1 reports full 3-locus haplotype patterns over codons 51/59/108 with counts (total n=44). Per the resolution preference, the multi-locus form is used to preserve linkage. All seven rows except 'Wildtype' (0) are encoded as 3-locus variant strings. The six non-zero haplotypes sum to 44 = total sequenced, so the wild-type combination is correctly 0 and need not be emitted separately. No per-locus-only breakdown exists that would beat the haplotype total (both share n=44), so haplotype form chosen.

### Wild-type encoding within haplotypes
The paper states changes were restricted to codons 51/59/108 and that all 44 samples had >=1 mutation (no full wild type observed). Within each reported haplotype, positions not mutated are encoded with the reference amino acid (51:N, 59:C, 108:S). 108-threonine and codon-16/164 mutations were assayed and not found; these are non-target (16,164) or non-target alleles (108-T is not a curated alt) so not separately emitted.

### Denominator
total_num = 44 (all children genotyped at all three codons; nested PCR-RFLP assayed all three positions in every sample).

### Multiclonal infections
Paper notes 14/44 samples showed evidence of multiclonal infection but Table 1 assigns each sample to a single discrete pattern, so counts are uniquely determinable and used as given.

### Geolocation
Magoda village, Tanga region (Muheza district), NE Tanzania. No coordinates in paper; approximate village location used (~ -4.85, 38.95).

### Duplicate risk
Samples from 1995; a related 1994 study (Rønn et al. 1996) used the same population. Only 1995 molecular data extracted here.
