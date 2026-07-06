# Extraction record — study PMID_16703518

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 4 · Count rows: 12

## Decisions

## Extraction decisions

### Target positions
The paper genotypes Pfcrt codon 72-76 haplotypes (CVMNK wild type, CVIET, SVMNT). Positions 72, 74, 75, 76 are targets. Encoded as multi-locus haplotype variant strings preserving linkage (e.g. crt:72_74_75_76:C_I_E_T for CVIET, S_M_N_T for SVMNT, C_M_N_K for wild type CVMNK). Reference amino acids at these positions: 72 C, 74 M, 75 N, 76 K.

### Haplotype vs per-locus
Only haplotype-level data are reported (SSOP ELISA targeting whole haplotypes); no per-locus breakdown available, so haplotype form is used.

### Count source and mixed infections
Table 1 gives absolute numbers per village per year. It distinguishes SINGLE-haplotype infections from MIXED infections (major/minor and majority/minority-uncertain). Mixed infections cannot be uniquely allocated to a single haplotype variant string without double counting, so ONLY single-haplotype infections were extracted as variant_num. The denominator (total_num) is set to the reported TOTAL number of infections genotyped per survey (Table 1 totals: Kwamasimba 2003=57, 2004=40; Mkokola 2003=99, 2004=123), reflecting that all these samples were sequenced at codons 72-76. This means single-haplotype variant_nums do not sum to total_num (the remainder are mixed infections not attributable to a single variant). This is a conservative choice that avoids fabricating allocations of mixed infections. Documented dropped data: all mixed-haplotype infections (CVMNK/CVIET, CVMNK/SVMNT, CVIET/CVMNK, CVIET/SVMNT, SVMNT/CVMNK, SVMNT/CVIET, and majority/minority-uncertain categories) could not be uniquely assigned and were not counted as any single variant.

Note: The text reports different denominators (n=69/47 for Kwamasimba, 107/129 for Mkokola for slides analyzed) and frequency-based counts (e.g. CVIET 95% n=54 in 2003 Kwamasimba), which count 'dominant' haplotype in mixed infections. These are not directly reconcilable with the Table 1 absolute single/mixed breakdown. Table 1 absolute numbers were preferred as the most explicit and uniquely-determinable source.

### Wild type
CVMNK is the reference/wild-type haplotype and is reported directly in Table 1; counts extracted as observed (not imputed). SVMNT reported as 0 single infections in 2003 (explicitly none detected).

### Geolocation
Two villages, Kwamasimba (600-700 m asl) and Mkokola (200 m asl), in Korogwe District, northern Tanzania. Precise village coordinates not given; approximate coordinates within the Korogwe District area were used. Method noted as 'village approximate location'.

### Temporal
Separate surveys per village per year: July 2003 and March 2004. collection_day set to mid-month of each stated collection month.
