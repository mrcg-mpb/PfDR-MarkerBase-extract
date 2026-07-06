# Extraction record — study PMID_17093247

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 1

## Decisions

## Extraction decisions

### Target markers found
Only PfCRT codon 76 (crt:76) was assayed among the curated target positions. The paper reports the K76T molecular marker for chloroquine resistance.

### Counts
- 'Assays for the T76 molecular marker for chloroquine resistance in PfCRT were successfully performed on 199 of the 210 filter-paper samples... All samples ... had the wild-type K76 PfCRT genotype.' Thus 199/199 wild-type K76 (crt:76:K), 0 mutant. Encoded the wild-type count only (variant_num = total_num = 199). No mutant count is emitted since it is zero, but the wild-type count fully conveys the frequency.

### Wild-type imputation
Not an imputation — the paper explicitly states all 199 typed samples were wild-type K76. Denominator N=199 is the number successfully assayed at codon 76.

### Spatial
Single site: Blantyre Malaria Project research clinic adjacent to Ndirande District Health Centre, a township on the outskirts of Blantyre, Malawi. Placed at the Ndirande/Blantyre township centroid (~-15.767, 35.05).

### Temporal
Single time window: enrollment May-November 2005 (follow-up through December 2005). One survey; collection_day set to midpoint (~2005-08-15) of the enrollment window. Since one site x one window, survey_id = study_id.

### Data not used
Other target markers (k13, dhfr, dhps, mdr1, cytb, other crt codons) were not assessed. Selected samples underwent DNA sequencing around codon 76 only; no additional target-position genotype counts reported.
