# Extraction record — study PMID_12447777

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 5

## Decisions

## Extraction decisions

### Scope
Only curated target positions extracted: dhfr 51/59/108 and dhps 436/437/540/581. dhps 613 and codon 164 (dhfr, not a target) were checked; 164 not mutated and not a target. cytb, crt, k13, mdr1 not assessed in this paper.

### Haplotype vs per-locus
Table 1 reports DHFR as the pure triple mutant haplotype Ile51-Arg59-Asn108 and DHPS as the Ser436-Gly437-Glu540 haplotype. No separate per-locus breakdown is provided, so the multi-locus (haplotype) form is used, preserving linkage. The DHPS haplotype string encodes 436 as reference S (Ser436), consistent with the text stating the mutant combination was consistently associated with Ser436.

### Temporal / spatial resolution
Only BEFORE-treatment samples were extracted as clean prevalence surveys. After-treatment counts (2-4 wk and 2-9 wk) reflect drug SELECTION on recurrent/reinfection samples during follow-up and represent a treated, selected subpopulation over a wide follow-up window; these are not baseline community prevalences and were not extracted to avoid biased/duplicated selection-driven counts. Two before-treatment surveys created, one per village (Kwevihombo, Skimu). Only Kwevihombo and Skimu were genotyped for drug resistance (Sakale and Mbomole only had msp genotyping).

### dhps 581
Text gives 3/50 Gly581 in Skimu before treatment - extracted as dhps:581:G. The Kwevihombo before-treatment denominator for 581 was not reported separately, so no 581 count extracted for Kwevihombo. The after-treatment 581 count (2/40) not extracted (post-treatment window).

### Wild-type imputation
No wild-type imputation performed. The paper reports genotype prevalences but does not give unambiguous denominators allowing safe wild-type imputation at individual target codons beyond the reported haplotype/allele counts. The Phe436 mutant appeared in only a single post-treatment sample (not baseline), so not extracted. Note: not imputing wild type may under-represent reference alleles.

### Geolocation
Kwevihombo and Skimu are villages in the East Usambara Mountains, Muheza district, NE Tanzania. Exact coordinates not stated; both placed at approximate East Usambara locations near Muheza (~-5.1, 38.65). Coordinates are approximate village-level estimates.

### Data not used
After-treatment (selection) counts, MOI/recrudescence data (Table 2), and the single Phe436 post-treatment sample were not extracted.
