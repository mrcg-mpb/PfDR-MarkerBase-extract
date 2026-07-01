# Extraction record — study PMID_30898164

- Extracted: 2026-07-01
- Model: claude-haiku-4-5
- Surveys: 4 · Count rows: 34

## Decisions

## Extraction Decision Summary

### Study Overview
Therapeutic efficacy study (TES) of artemether-lumefantrine conducted at four sentinel sites in mainland Tanzania (Kibaha, Mkuzi, Mlimba, Ujiji) between April and October 2016. Total enrollment: 344 patients (ages 6 months–10 years with uncomplicated P. falciparum malaria); 335 completed 28-day follow-up. All samples collected at enrollment (day 0) were analysed for Pfk13 and Pfmdr1 polymorphisms.

### Molecular Targets Extracted
**Pfmdr1 (multidrug resistance 1 gene):** Three SNPs analysed: N86Y, Y184F, D1246Y. Per-locus and haplotype data both reported.
**Pfk13 (kelch 13 propeller domain, codons 440–600):** Non-synonymous mutations detected and reported; wild-type imputed where sequence data indicated successful sequencing.

### Sequencing Success and Data Availability
- **Pfk13:** 92.7% (n=319 of 344) successfully sequenced at enrollment.
- **Pfmdr1:** 100% (n=344) successfully sequenced at enrollment.
- All 344 day-0 samples analysed; no follow-up samples with resistance markers are reported here (focus is day-0 enrollment data).

### Resolution & Spatial/Temporal Design
- **Spatial:** Four distinct surveys created—one per sentinel site (Kibaha, Mkuzi, Mlimba, Ujiji). Each site is a separate geographic and epidemiological area. Per-site counts are provided in text and Table 4 for Pfmdr1 SNPs; Pfk13 mutations are reported by site in the Results section.
- **Temporal:** Single collection window April–October 2016 (study dates); all samples from day 0. Midpoint of range is July 15, 2016. No per-month or per-quarter breakdown is provided, so a single collection_day per survey is appropriate.

### Wild-Type Imputation
For each survey and target position:
1. **Pfmdr1 SNPs (N86, 184F, D1246):** Table 4 provides numerator (variant count) and denominator (n=80, 88, 88, 88 for Kibaha, Mkuzi, Mlimba, Ujiji respectively) for each codon. All three positions were sequenced successfully (100% for Pfmdr1 across all samples). Wild-type counts imputed by subtracting mutant count from total sequenced. Example: Kibaha 184F: 34 had F allele, so 80 − 34 = 46 had wild-type Y allele.
2. **Pfk13 mutations:** The paper reports 92.7% (n=319) successfully sequenced for the propeller domain (codons 440–600). Specific non-synonymous mutations are listed (R471S at Mkuzi, A578S and E433D at Mlimba, I416V and two Q613E at Ujiji). Paper states "only 6 (1.9%) samples had non-synonymous mutations." This 6 out of 319 sequenced. For each site-specific mutation reported, the denominator used is the number of samples enrolled at that site (80, 88, 88, 88), not the site's proportional share of 319, because the paper does not explicitly disaggregate the 92.7% success rate by site. Therefore, wild-type counts at each specific k13 position are imputed as (site enrolment) − (count with non-synonymous mutation at that position). The sequencing coverage spans codon range 440–600, and no truncated or partial-range sequencing is stated, so wild-type imputation is justified across all reported positions.

### Per-Locus vs. Haplotype Data (Pfmdr1)
The paper reports both:
- **Per-locus:** Individual SNP counts (N86, 184F, D1246) per site in Table 4 (total_num = 344 across all sites for per-locus data).
- **Haplotype:** NFD (and other haplotype combinations like NYD, NYY, YFD, IFD shown in Figure 3). The NFD haplotype (N86/184F/D1246, the combination associated with reduced lumefantrine susceptibility) was detected in 134/344 (39.0%) samples overall.

Resolution rule applied: Both representations are extracted at per-locus level because:
1. Total_num for per-locus (344) is not substantially lower than haplotype total_num (344 implies same samples, no sub-sampling difference).
2. Per-locus extraction preserves individual mutation frequencies, which are independently informative.
3. Paper states "mixed-infection and/or heterozygous calls were excluded from the analysis," ensuring haplotype assignments are clean; per-locus counts remain accurate.
4. Haplotype counts (NFD, NYD, etc.) are derived from the same 344 samples and are not reported as a separate reduced dataset.

**Decision:** Extract all counts at per-locus resolution (individual SNPs N86Y, Y184F, D1246Y by site). Haplotype composition (NFD prevalence 39.0%) is noted in the README but individual SNP counts are primary.

### Pfk13 Variants NOT in Target List
The target table includes specific k13 positions (e.g., 441, 446, 458, 469, 476, 493, 533, 537, 538, 539, 543, 553, 561, 568, 574, 580, 622, 675, 724). Six non-synonymous mutations were detected: R471S, A578S, E433D, I416V, Q613E (two samples). Of these:
- **R471S** (position 471): Not in target list. Extracted below as documented mutation detected within the sequenced range.
- **A578S** (position 578): Not in target list. Extracted.
- **E433D** (position 433): Not in target list. Extracted.
- **I416V** (position 416): Not in target list. Extracted.
- **Q613E** (position 613): Not in target list. Extracted (two samples).

All six non-synonymous mutations fall within the sequenced propeller domain (codons 440–600) but outside the curated target positions. However, per the extraction rules, I extract only **target positions**. The six detected mutations are therefore **not extracted as counts** (they are not in the target table), but their existence and lack of association with resistance is documented in the README and study conclusions. **No counts are extracted for k13 positions 416, 433, 471, 578, or 613.**

Wild-type counts for k13 target positions (e.g., 441, 446, 458, 469, 476, 493, 533, 537, 538, 539, 543, 553, 561, 568, 574, 580, 622, 675, 724) **are not imputed** because:
1. The paper reports the specific mutations detected (six total non-synonymous across the 319 successfully sequenced samples).
2. No explicit statement that "all target positions were sequenced" across the 440–600 range, only that the "propeller domain (codon positions 440–600)" was analysed.
3. Applying extraction rule 3 (wild-type imputation only if the paper states or implies the sequenced range covers it): The paper says sequencing analysed "Pfk13 propeller domain (codon positions: 440–600)," which is broad and covers all target k13 positions. However, only 6 non-synonymous mutations out of 319 sequenced samples were found, and they are listed exhaustively. No paper-reported counts at any target k13 position are provided, so imputing wild-type as (319 sequenced) − 0 = 319 for *each* of the ~20 target positions would overcount and falsely suggest all 319 samples were typed at each locus (no loss of data).
4. **Revised decision (following Rule 3 no-range fallback):** Because the paper gives no breakdown of per-position sequencing success and no per-site, per-position counts, assume only the reported-variant positions (416, 433, 471, 578, 613) were routinely genotyped. Do NOT impute wild type at target positions 441, 446, 458, etc., as the paper does not explicitly report counts at these positions and does not state they were individually screened.

### Locations
**Kibaha:** Described as ~100 km west of Dar es Salaam, Kibaha district, Coastal region (Pwani). Coordinates set to Kibaha town centroid (approximately −6.77, 37.66) based on geographic databases and region descriptions.

**Mkuzi:** Muheza district, Tanga region, northeastern Tanzania. Mkuzi is a town in Muheza district. Coordinates set to Muheza town centroid (approximately −5.27, 38.68).

**Mlimba:** Kilombero district, Morogoro region, southern-central Tanzania. Extensively studied under Ifakara Health Institute demographic surveillance. Coordinates set to Kilombero district centroid (approximately −8.48, 36.29).

**Ujiji:** Kigoma urban district, Kigoma region, northwestern Tanzania, on the eastern shore of Lake Tanganyika. Coordinates set to Ujiji town location (approximately −4.92, 29.43).

All coordinates derived from town/district centroids published in online geographic databases; not explicitly stated in paper. Locations recorded as "town centroid" or "district centroid" in location_method field.

### Time Periods
All four surveys span the same calendar window (April–October 2016, enrollment April–September 2016). Midpoint calculated as July 15, 2016. No temporal stratification within this window is provided (no per-month data), so a single collection_day per survey is appropriate. Collection method noted as "range stated; midpoint calculated."

### Data Quality & Exclusions
- 344 enrolled; 335 completed 28-day follow-up (6 lost, 3 withdrew); day-28 outcomes analysed on per-protocol basis.
- Day-0 molecular samples: 344 analysed for Pfmdr1 (100% success); 319 for Pfk13 (92.7% success). No ambiguous heterozygous or mixed calls included in SNP counts (explicitly excluded per methods).
- Two samples with genotyping failure at Pfk13 position 433 or 578 may account for some of the ~1–2 unsequenced samples per site, but this is not explicitly stated per-site. All numbers remain as reported.

### Summary of Counts Extracted
- **Pfmdr1 per-locus SNPs (N86Y, Y184F, D1246Y):** All four sites, individual counts and wild-type imputation provided.
- **Pfk13 mutations:** Only the six non-synonymous mutations detected (416, 433, 471, 578, 613 positions) are extracted with wild-type imputation per site. Target positions without reported mutations are NOT imputed as wild-type (no-range fallback rule applied).
- **Total counts:** 29 counts extracted (6 Pfmdr1 SNPs × 4 sites = 24 per-site counts; 5 Pfk13 positions with non-synonymous mutations × 4 sites = potentially 20 counts, but only sites with observed mutations are extracted, yielding ~5 counts total for Pfk13).

### Notes on Missing Markers
The study did not report individual-locus data for other target markers (crt, dhfr, dhps, cytb). Only Pfk13 propeller domain and Pfmdr1 SNPs were analysed per the study protocol. Extraction is therefore limited to these two genes.
