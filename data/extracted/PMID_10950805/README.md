# Extraction record — study PMID_10950805

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 6

## Decisions

# Extraction decisions

## Markers extracted
Only DHFR codons 51 (I), 59 (R), 108 (N) have quantitative frequencies. DHPS 436/437 mutations are mentioned as detected ('Only the Ser-436 and Gly-437 mutations were detected') but NO counts/denominators are given ('data not shown'), so no DHPS counts were extracted.

## Percentage-to-count conversions
Counts derived from reported percentages x denominators:
- Baseline n=119: 12.8% -> 15 (108 N); 4.2% -> 5 (51 I); 10.9% -> 13 (59 R).
- Breakthrough n=52: 100% -> 52 (108 N); 50% -> 26 (51 I); 90% -> 47 (59 R, 46.8 rounded).
These are estimates; the paper only gives percentages. Rounding may introduce +/-1 error.

## Wild-type imputation
NOT performed. The paper reports only mutant prevalences at the three DHFR positions and does not clearly state which range of codons was sequenced beyond these targeted mutation assays (RFLP/allele-specific PCR). Per rule 3, without a clear sequenced range, I did not impute wild-type counts. Note: this biases the dataset away from wild type since only mutant calls are recorded.

## Haplotype vs per-locus
The paper reports per-locus prevalences only (not linked haplotypes with denominators), so per-locus form used.

## Two surveys
Baseline (day 0 village-wide, n=119, community household survey) and breakthrough infections (n=52, from the prophylaxis cohort) are distinct sample groups from the same site/time window and are kept as separate surveys. These are non-overlapping sample sets (baseline vs new breakthrough infections). The 109 enrolled children and Figure 2 microsatellite data are not additional count data for target markers.

## Geolocation
Tieneguebougou described as rural village ~30 km NE of Bamako, Mali. Approximate coordinates (12.85N, -7.8E) placed NE of Bamako. Method: village description / offset from Bamako centroid.

## Temporal
Single collection year 1996, rainy season (June-October). Range set to those months, midpoint 1996-08-15.
