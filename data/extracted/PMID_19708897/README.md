# Extraction record — study PMID_19708897

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 12

## Decisions

# Extraction decisions

## Study
Single site (Uige Provincial Hospital), single time window (27 Jul-12 Aug 2004) -> one survey, survey_id = study_id.

## Denominators
66 of 71 samples were fully characterized for all drug-resistance markers; the paper reports all per-locus frequencies with denominator /66. Used total_num=66 throughout.

## Per-locus vs haplotype
Table 1 gives a full 4-gene haplotype breakdown (crt76, mdr86, dhfr51/59/108, dhps436/437) over 66 isolates. However, the paper also reports clean per-locus counts in the text (all /66), and the individual target codons of interest are more useful disaggregated. The haplotype total (66) equals the per-locus total (66), so no >20% size penalty applies. Because target positions span multiple genes and the per-locus text data cover all target positions cleanly at the same N, I extracted the PER-LOCUS marginals rather than the 17-row multi-locus haplotype table, to avoid ambiguity in encoding all 17 rows and to keep target-position resolution. This avoids double counting (haplotype rows NOT separately extracted).

## crt 74/75/76
The pfcrt 74I-75E-76T mutant haplotype is reported jointly (62/66); the 4 remaining are the wild-type MNK haplotype (74M-75N-76K). Encoded these as single-gene multi-locus haplotype strings using the within-gene form (crt:74_75_76:I_E_T and crt:74_75_76:M_N_K) since all three positions are in the same gene (crt). 62 mutant + 4 wild type = 66. crt:72 wild type (C) imputed since 72 was explicitly characterized and 72S not found (all 66 wild type).

## Wild-type imputation
- crt:72:C = 66/66 (codon 72 characterized; 72S not found).
- dhps:540:K, dhps:581:A, dhps:613:A = 66/66 each (paper states these codons characterized and mutations not detected).
These positions were explicitly stated as sequenced/characterized, so wild-type imputation is justified.

## Positions NOT imputed
Other target crt positions (93,97,145,218,220,271,326,343,350,353,356,371), cytb:268, dhps:431/436 additional, k13 codons: not characterized in this paper (k13, cytb not studied; dhps:431 was in ATPase6 gene context not dhps; the paper's ATPase6 431E->K is a different gene, not dhps:431). No imputation for these.

## Data not used
- pfdhfr codon 50 (not a target position).
- pfATPase6 SNPs (243, 402, 431, 263, 623, 769, 771) - not target positions; note pfATPase6 431 is NOT dhps:431.
- Microsatellite data and the 17-row Table 1 haplotype breakdown (superseded by per-locus extraction to avoid double counting).
- mdr1:86 mixed calls: 21 of 45 mutants were mixed wt/mutant but authors classified all as mutant; followed authors' classification (variant_num=45).

## Geolocation
Uige Provincial Hospital located to Uige city centroid (~-7.6087, 15.0613), capital of Uige province, northern Angola.

## Fix applied
Previous version used cross-gene haplotype syntax (crt:74:I;crt:75:E;crt:76:T) which duplicated the gene token. Since all three positions are within the same gene, corrected to the within-gene multi-locus form crt:74_75_76:I_E_T (and M_N_K for wild type).
