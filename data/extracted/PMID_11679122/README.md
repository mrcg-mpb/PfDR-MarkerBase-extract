# Extraction record — study PMID_11679122

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 28

## Decisions

## Extraction decisions

### Source
All counts taken from Table 1, which gives per-codon counts and percentages separately for Aioun (DHFR n=59, DHPS n=59) and Kobeni (DHFR n=103, DHPS n=101). Two surveys created (one per site), both from the single 1998 collection year.

### Target positions covered
- DHFR: 51, 59, 108 (target positions extracted). DHFR codons 16 and 164 were reported but are NOT in the target table, so excluded.
- DHPS: 436, 437, 540, 581, 613 (target positions extracted). DHPS 431 not reported.

### Denominators
Note DHFR denominators (Aioun 59, Kobeni 103) differ from DHPS denominators (Aioun 59, Kobeni 101) because only 101 of 103 Kobeni positives amplified with DHPS primers. Each count uses the appropriate gene-specific total from Table 1.

### Wild-type / reference encoding
- crt/k13/mdr1/cytb: not studied; nothing imputed.
- For target positions that were assayed and found monomorphic, the reference allele is emitted at variant_num=total_num: dhps:540:K (both sites), dhps:581:A (both sites). These positions were explicitly assayed (specific restriction enzymes described) and no mutant found, so full wild-type imputation is justified.
- For positions with mutants, the reference amino acid count is also recorded directly from Table 1 (e.g. dhfr:51:N, dhfr:59:C, dhfr:108:S, dhps:437:A, dhps:613:A). At codon 436 the reference is serine (dhps:436:S) which is directly reported.
- dhfr:108:threonine and dhfr:164, dhfr:16 are outside target set. 613-threonine reported as 0 in both sites (not emitted separately as no target 613:T count was present).

### Haplotype vs per-locus
Table 1 reports per-locus data. The text mentions the DHFR triple combination (51I/59R/108N) qualitatively (mutations always found in combination; one doubly-infected Kobeni isolate), but no clean per-haplotype count table over target positions is provided that reconciles to whole numbers, so per-locus data from Table 1 were used (finer, fully reconcilable). No double counting.

### 436 note
At codon 436, three variants sum: serine (wild) + alanine + phenylalanine. Aioun: 27+29+3=59 OK. Kobeni: 51+47+3=101 OK. dhps:436 phenylalanine (S->F) is not among target alleles (only S->A is listed as target for 436), so 436:F not emitted; the 436:S reference count is taken directly from Table 1 as reported.

### Geolocation
- Aioun (Aioun el Atrous), capital of Hodh El Gharbi: ~16.66N, -9.62E (town centroid).
- Kobeni, town near the Mali border in Hodh El Gharbi: ~15.9N, -9.4E (approximate town centroid).

### Temporal
Single collection year 1998; collection_day set to 1998-07-02 (year midpoint) with start/end spanning the year.

### Not used
DHFR 16 and 164 and DHPS 436-phenylalanine codons/alleles outside the target list; qualitative combination statistics not converted to counts.
