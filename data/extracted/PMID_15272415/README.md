# Extraction record — study PMID_15272415

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 8

## Decisions

# Extraction decisions

## Study
Single cross-sectional survey in Kidal district, northern Mali, 11-18 October 1999 (5 nomadic camps). One survey record; survey_id = study_id.

## Geolocation
Survey conducted in 5 unnamed nomadic camps in Kidal district. Placed at Kidal town/district centroid (~18.44N, 1.41E). Method: district/town centroid.

## pfcrt 76
pfcrt K76T reported directly: 45/57 mutant (79%), 11/57 wild-type K76 (19%), 1/57 mixed. Extracted all three (mutant T, wild K, mixed K/T); 45+11+1=57 = total sequenced.

## dhfr positions (108, 59, 51)
Denominator for dhfr/dhps = 22 samples in which all 3 dhfr and both dhps markers were successfully typed (the 5-marker panel). Prevalences reported as percentages only: S108N 45%, C59R 35%, N51I 30%. Converted to counts against N=22: 0.45*22=9.9->10; 0.35*22=7.7->8; 0.30*22=6.6->7. These are approximate integer allocations from rounded percentages; documented as such. The paper also reports the dhfr triple mutant (all 3) present in 20% (~4-5 samples) but this haplotype was NOT extracted separately to avoid double counting with per-locus data, and the per-locus form retains position-level detail. Wild-type not separately imputed for dhfr positions because exact mutant counts are approximate; only reported mutant frequencies extracted.

## dhps positions (437, 540)
dhps A437G detected in exactly 1 patient (stated: 3 dhfr mutations plus dhps A437G in 1 patient) -> variant_num=1, total_num=22. dhps K540E: quintuple mutant (which includes K540E) was NOT detected in any sample; since the 5-marker panel (including dhps 540) was successfully typed in these 22 samples, wild-type K540 imputed: variant_num=0 mutant / total 22 (all wild-type at 540).

## Not extractable / excluded
- Table 1 (suspected malaria clinic proportions) is not marker data.
- Quintuple and triple haplotype summary values not extracted separately (avoid double counting per-locus data).
- No target k13, mdr1, cytb, or other crt/dhps positions reported.
