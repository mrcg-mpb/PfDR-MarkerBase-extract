# Extraction record — study PMID_11679121

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 6

## Decisions

# Extraction decisions

## Site & time
- Single site: Agogo, Ashanti region, Ghana (District/Presbyterian Mission Hospital antenatal care). One survey; survey_id = study_id.
- Geolocation: town centroid (~6.7994, -1.0806).
- Time: enrolled November/December 1998; midpoint 1998-12-01 used as collection_day.
- Sample source: antenatal care pregnant women -> clinical_anc.

## Targets extracted
Only curated targets present: crt:76, mdr1:86, dhfr:108.

## Counts and mixed alleles
- Paper reports mixed (heterozygous) calls separately (Table 2: K76+T76, N86+Y86, S108+N108) but the headline prevalences (T76 69%=118/172; Y86 66%=114/172; N108 80%=137/172) explicitly count mixed with resistant ('Assigning mixed to resistant alleles'). I encoded the resistant totals (including mixed) and the pure-wild-type remainder to avoid double counting. Because mixed calls are folded into resistant in the headline numbers, I did not additionally emit K76/T76 heterozygous strings (would double count).
- Wild-type counts derived as total (172) minus resistant total: crt K76=54, mdr1 N86=58, dhfr S108=35. These match Table 2 pure-wild-type sums for crt (37+15+2=54) and are consistent with text 'sensitive genotypes' n=58 for pfmdr1.

## Wild-type imputation
- Total sequenced N=172 for each marker (all parasitaemic isolates genotyped by PCR-RFLP at each codon). Wild-type counts reported as complement of resistant within N=172.

## No disaggregation used
- Table 2 disaggregates by CQ status (NCQ/UCQ/SCQ), which is a drug-exposure grouping, NOT a spatial or temporal breakdown. Per rules, spatial/temporal finest resolution is single site/time, so the pooled 172-isolate totals are the correct (and only) survey. CQ subgroups were not extracted as separate surveys since they do not represent distinct sites or time bins.

## Overlap note
- pfdhfr N108 data likely overlap with prior publications from the same 530-woman cohort (Mockenhaupt et al. 2000, 2001). Documented but retained as reported here.
