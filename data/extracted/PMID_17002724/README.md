# Extraction record — study PMID_17002724

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 9

## Decisions

## Extraction decisions

### Target markers
Paper genotyped dhfr codons 50,51,59,108 and dhps codons 436,437,540. Of these, targets are dhfr:51, dhfr:59, dhfr:108, dhps:436, dhps:437, dhps:540. dhfr codon 50 is NOT a target and is dropped from haplotype encoding. dhps:436 target is S->A (matches reported S436A).

### Haplotype vs per-locus choice
Table 4 reports allele-level haplotypes per locus (dhfr n=158; dhps n=177) with full breakdowns summing to the totals. It also reports a combined dhfr+dhps table (n=133) but only as mutation-count categories (Sensitive/Single/Double/... ) without specifying which codons — these cannot be mapped to specific target variant strings, so the combined table was NOT extracted. The per-locus haplotypes preserve linkage within each gene and are fully specified, so they were extracted. No cross-gene haplotype extracted (combined table lacks codon identity). No double counting: only the per-locus dhfr and dhps haplotype tables used.

### dhps codon 436 encoding
The dhps haplotype 3-letter code is for positions 436,437,540. Wild-type reference at 436 is S; mutant A. All haplotypes fully specify these three positions, so all target codons (436,437,540) are captured within the dhps haplotype strings.

### Wild-type / imputation
No separate wild-type imputation needed: sensitive haplotypes (dhfr CNCS n=12; dhps SAK n=53) are explicitly reported reference forms at all target positions and are included as counts. Denominators are the number of single/majority genotype infections analysable at each locus (dhfr 158, dhps 177).

### Data not used
- Combined dhfr+dhps genotype table (n=133): mutation-count categories only, no codon-level identity -> not extractable to variant strings.
- Percentages in text (e.g. 39%, 46%) are consistent with Table 4 counts; counts used directly.

### Geolocation
Single site: Divine Maitre Health Centre, Shabunda town, South Kivu, DRC. Placed at Shabunda town centroid (~ -2.667, 27.333).

### Temporal
Single survey (one site, one window). Screening 1 Apr - 13 May 2004; collection_day set to midpoint 2004-04-22.
