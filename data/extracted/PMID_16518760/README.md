# Extraction record — study PMID_16518760

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 6 · Count rows: 96

## Decisions

# Extraction decisions - PMID 16518760 (Francis et al. 2006, JID)

## Source
All counts from Table 2 (no. (%) of patients wild type / mixed / pure mutant per site for each mutation). Six sites: Kanungu, Mubende, Jinja, Arua, Tororo, Apac.

## Target positions extracted
- crt:76 (Thr-76): C->? no, reference K->T. Extracted WT (K), mixed (K/T), pure mutant (T).
- dhfr:51 (Ile-51), dhfr:59 (Arg-59), dhfr:108 (Asn-108): reference/mutant per target table.
- dhps:437 (Gly-437), dhps:540 (Glu-540).
- dhfr:164 (Leu-164) is NOT in the curated target list, so NOT extracted (Table 2 reports it but it is out of scope).

## Mixed genotypes
Table 2 distinguishes wild type, mixed (wt + mutant alleles present), and pure mutant. Encoded pure mutant as the alt allele string, wild type as the reference allele string, and mixed as the heterozygous `ref/alt` form. All three sum to the tested total per position, so no double counting.

## Denominators (total_num)
- pfcrt 76, dhfr 51, dhfr 108: tested on 80 randomly selected samples per site (40/arm). Apac pfcrt 76 was tested on ALL samples (14+94+238=346).
- dhfr 59, dhps 437, dhps 540: tested on ALL samples. Denominators taken directly as WT+mixed+pure sums from Table 2 (Kanungu 353, Mubende 340-344, Jinja 324-325, Arua 332-340, Tororo 333, Apac 351-352). Small variation between markers at a site reflects assay success rate (99% of 8407/8450 tests successful). Used the actual per-marker sums as denominators rather than Table 1 molecular-analysis N.

## Haplotype vs per-locus
The paper reports the 'six mutations of interest' combined haplotype (all mixed/mutant; all pure mutants) in Table 2, but these are cross-gene composite counts that ASSUME dhfr 108/51 and pfcrt 76 are present (imputed) rather than jointly sequenced haplotypes. Because these composites rely on assumptions and would duplicate the per-locus data, I extracted only the per-locus counts (finer, non-imputed) and did NOT extract the composite 6-mutation rows.

## Wild-type imputation
No imputation beyond what Table 2 explicitly reports. Each position's WT count is taken directly from the table. No range-based imputation to other codons was performed (only the reported positions were assayed by PCR-RFLP).

## Temporal
Study conducted Dec 2002-May 2004; no per-site collection dates given. All six surveys share the study-wide window (start 2002-12-01, end 2004-05-31, midpoint 2003-09-15). This is coarser than ideal but the paper provides no finer per-site temporal breakdown.

## Geolocation
Sites placed at town/district centroids in Uganda (Kanungu, Mubende, Jinja, Arua, Tororo, Apac) from map (Figure 1) and known Ugandan geography. Coordinates approximate.

## Duplicate risk
Samples derive from prior published efficacy trials (refs 5,6) at the same sites - medium overlap risk with those datasets, noted for downstream de-duplication.

## Data not used
- dhfr Leu-164 (out of curated scope).
- Composite 6-mutation haplotype rows (assumption-based, would double count).
