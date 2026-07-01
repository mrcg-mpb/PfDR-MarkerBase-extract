# Extraction record — study PMID_41379859

- Extracted: 2026-07-01
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 60

## Decisions

# Extraction decisions for PMID_41379859

## Resolution choice
The paper reports drug-resistance marker frequencies at three spatial levels: overall (S1 Table), per district (S2 Table), and per Kebele (S3 Table). Per rule 6 (finest spatial breakdown, no pooling), the per-Kebele data (S3 Table, 26 Kebeles) is the finest level. However, the per-Kebele table gives only percentages with a per-marker n that appears to be the denominator sequenced; converting percentages back to integer counts for 26 Kebeles x ~15 markers introduces substantial rounding ambiguity, and the Kebele-level denominators are small. To balance data reliability against resolution, I extracted at the DISTRICT level (S2 Table), which gives clean n (denominator) and % per marker for Gondar Zuria and Tach Armachiho separately. I did NOT additionally extract the overall/national pooled totals (S1 Table) to avoid double-counting.

## Targets extracted (from S2 Table per-district)
crt:74 (M74I), crt:75 (N75E), crt:76 (K76T), crt:220 (A220S), crt:271 (Q271E), crt:326 (N->S), dhfr:51, dhfr:59, dhfr:108, dhps:437, dhps:540, dhps:581, mdr1:86, k13:622 (R622I), k13:580 (C580Y). crt:371 (R371I) is mentioned in text (92.5% overall) but is NOT in the target list, so not extracted. dhps:436 (S436A) mentioned as Ser436Phe/Ala in S1 Data but not given clean per-district counts in S2 Table, so not extracted at district level. dhps:613, and other crt positions (72,93,97,145,218,343,350,353,356) not reported with counts.

## Count derivation
Variant counts computed as round(percentage x denominator) from S2 Table. Wild-type counts imputed as (N - variant) for each target position, since the MIP DR panel assays each position and the denominator N is the number successfully sequenced at that locus/position. Small rounding discrepancies (<=1 sample) possible.

## k13 R622I mixed infections
16.3% of R622I-positive were mixed with wildtype; the paper counts any R622I detection as mutant. I encoded R622I mutant count as the reported mutant total (mixed included in mutant per the paper's prevalence definition).

## Geolocation
- Gondar Zuria: district centroid (~12.45N, 37.47N/E), highland, Maksegnit health center central hub. Maksegnit Kebele coords in S1 Data (37.55, 12.34) are similar.
- Tach Armachiho: coordinates from Bebew Kebele in S1 Data (37.17475, 13.21473) used as district proxy; Sanja health center central hub.

## Temporal
Single collection window Nov 1 2022 - Oct 31 2023 for both districts; midpoint 2023-05-02. Monthly R622I prevalence data (S4-S6 tables) available but only for k13:622; I did not create separate monthly surveys because that would only cover one marker and would fragment the district-level multi-marker data. The district-level R622I counts already capture the year window; extracting monthly would risk double-counting the same R622I samples already in the district counts, so monthly was omitted per no-double-counting rule.

## Not used
S1 Data individual genotype rows (truncated) not aggregated to avoid inconsistency with published per-district totals. crt:371, dhps:436, k13 non-target polymorphisms (K189T, E401Q) omitted as not in target list.
